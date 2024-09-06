import random
from Shape import *
import Circle
from Circle import *
from Rectangle import *
from Square import *


class ShapeContainer:
    """
        A container class for managing a collection of shapes (Circle, Square, Rectangle).
        This class allows generating random shapes, calculating their total areas,
        total perimeters, and counting shapes by color.
    """
    Colors = ["pink", "blue", "purple", "red", "black", "orange"]
    Range_side_length = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    Shapes = [[type(Circle), type(Rectangle), type(Square)]]

    def generate(self, x):
        """
            Generates 'x' random shapes with random colors and dimensions.

            Parameters:
            x (int): The number of shapes to generate.
         """
        self.Shapes.clear()
        for i in range(x):
            the_shape = random.choice(ShapeContainer.Shapes)
            the_color = random.choice(ShapeContainer.Colors)
            if the_shape == type(Circle):
                the_side = random.choice(ShapeContainer.Range_side_length)
                self.Shapes.append(Circle.Circle(the_side, the_color))
            elif the_shape == type(Square):
                the_side = random.choice(ShapeContainer.Range_side_length)
                self.Shapes.append(Square.Square(the_side, the_color))
            if the_shape == type(Rectangle):
                the_side = random.choice(ShapeContainer.Range_side_length)
                the_other_side = random.choice(ShapeContainer.Range_side_length)
                self.Shapes.append(Rectangle.Rectangle(the_side, the_other_side, the_color))

    def SumAreas(self):
        """
            Calculates the total area of all shapes in the container.

            Returns:
            float: The sum of the areas of all shapes.
        """
        sum_surface = 0
        for i in self.Shapes:
            surface = Rectangle.Rectangle.area()
            if Shape == type(Circle):
                surface = Circle.Circle.area()
            sum_surface += surface
        return sum_surface

    def sump(self):
        """
            Calculates the total perimeter of all shapes in the container.

            Returns:
            float: The sum of the perimeters of all shapes.
        """
        sum_p = 0
        for i in self.Shapes:
            p = Rectangle.Rectangle.perimeter()
            if Shape == type(Circle):
                p = Circle.Circle.perimeter()
            sum_p += p
        return sum_p

    def count_colors(self):
        """
            Counts the number of shapes of each color in the container.

            Returns:
            dict: A dictionary where keys are colors and values are the number of shapes for that color.
        """
        count = dict.formkeys(ShapeContainer.Colors, 0)
        for i in self.Shapes:
            count[Shape.Shape.return_color()] += 1
        return count


