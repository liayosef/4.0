from http.server import HTTPServer, BaseHTTPRequestHandler
import socket

PORT = 80  # פורט סטנדרטי ל-HTTP

BLOCKED_TEMPLATE = """<!DOCTYPE html>
<html lang="he" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>אתר חסום</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #ffebee 0%, #f44336 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
            color: #333;
        }
        .blocked-container {
            background-color: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
            padding: 50px;
            text-align: center;
            max-width: 600px;
            margin: 20px;
        }
        .blocked-icon {
            width: 100px;
            height: 100px;
            background-color: #f44336;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 20px;
            font-size: 48px;
            color: white;
        }
        .blocked-title {
            color: #c62828;
            font-size: 36px;
            margin-bottom: 15px;
        }
        .blocked-subtitle {
            color: #666;
            font-size: 18px;
            margin-bottom: 30px;
        }
        .blocked-domain {
            background-color: #fff3e0;
            border: 2px solid #ff9800;
            border-radius: 8px;
            padding: 10px;
            margin-bottom: 30px;
            font-weight: bold;
            word-wrap: break-word;
        }
        .back-btn {
            background-color: #f44336;
            color: white;
            border: none;
            border-radius: 8px;
            padding: 12px 30px;
            font-size: 16px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
        }
        .back-btn:hover {
            background-color: #d32f2f;
        }
    </style>
</head>
<body>
    <div class="blocked-container">
        <div class="blocked-icon">🚫</div>
        <h1 class="blocked-title">אתר חסום</h1>
        <h2 class="blocked-subtitle">הגישה לאתר זה נחסמה על ידי המערכת</h2>
        <div class="blocked-domain">האתר: {domain}</div>
        <p>לקבלת גישה, פנה להורים או למנהל המערכת.</p>
        <a href="javascript:history.back()" class="back-btn">חזור אחורה</a>
    </div>
</body>
</html>"""


class BlockPageHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()

        # מציאת הדומיין שנחסם
        requested_domain = self.headers.get('Host', 'לא ידוע')

        # הצגת דף החסימה
        block_page = BLOCKED_TEMPLATE.format(domain=requested_domain)
        self.wfile.write(block_page.encode('utf-8'))

    def log_message(self, format, *args):
        """לוג מותאם אישית"""
        print(f"[BLOCK] בקשה מ-{self.client_address[0]}: {args[0]}")


def get_local_ip():
    """מציאת כתובת IP מקומית"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"


def run_block_server(port=PORT):
    """הפעלת שרת דף החסימה"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, BlockPageHandler)

    print(f"[*] שרת דף החסימה פועל על http://localhost:{port}")
    print("[*] לחץ Ctrl+C כדי לעצור")

    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\n[*] עצירת שרת החסימה")
        httpd.server_close()
    except Exception as e:
        print(f"[!] שגיאה: {e}")


if __name__ == '__main__':
    try:
        run_block_server()
    except PermissionError:
        print("[!] שגיאת הרשאות: לא ניתן להאזין לפורט 80")
        print("[*] מנסה להשתמש בפורט 8080 במקום...")
        run_block_server(8080)