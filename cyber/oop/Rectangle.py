import Shape
import Square


class Rectangle(Shape):
    def __init__(self, width, height, color='blue'):
        super().__init__(color)
        self.width = width
        self.height = height


    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

    def __add__(self, other):
        if isinstance(other, Rectangle):
            new_width = self.width + other.width
            new_height = self.height + other.height
            return Rectangle(new_width, new_height, self.color)

