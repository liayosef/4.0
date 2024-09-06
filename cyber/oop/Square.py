import Shape



class Square(Shape):
    def __init__(self, width, height, color='blue'):
        super().__init__(color)
        self.width = width
        self.height = width


    def area(self):
        return self.width * self.height


    def perimeter(self):
        return 2 * (self.width + self.height)



   def __add__(self, other):
        if isinstance(other, Square):
            new_side_length = self.side_length + other.side_length
            return Square(new_side_length, self.color)

