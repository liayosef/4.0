
class Shape:

    def __init__(self, color):
        self.surface = 0
        self.p = 0
        self.color = color

    def get_color(self, color):
        self.color = color

    def return_color(self, color):
        return self.color

    def return_surface(self):
        return self.surface

    def return_p(self):
        return self.p
