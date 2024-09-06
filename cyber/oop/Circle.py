import Shape
import math

class Circle(Shape):
    """
    A class representing a circle, inheriting from the Shape class.

    Attributes:
    -----------
    radius : float
        The radius of the circle.
    color : str
        The color of the circle.
    """

    def __init__(self, radius, color):
        """
        Initializes a Circle object with a given radius and color.

        Parameters:
        -----------
        radius : float
            The radius of the circle.
        color : str
            The color of the circle.
        """
        super().__init__(color)
        assert isinstance(radius, (int, float)) and radius > 0, "Radius must be a positive number."
        self.radius = radius

    def area(self):
        """
        Calculates the area of the circle.

        Returns:
        --------
        float
            The area of the circle, calculated as π * radius^2.
        """
        area = math.pi * self.radius * self.radius
        assert area > 0, "The area should be positive."
        return area

    def perimeter(self):
        """
        Calculates the perimeter (circumference) of the circle.

        Returns:
        --------
        float
            The perimeter of the circle, calculated as 2 * π * radius.
        """
        perimeter = 2 * math.pi * self.radius
        assert perimeter > 0, "The perimeter should be positive."
        return perimeter


# בדיקות עם assert
# Test 1: Initialize circle and check radius and color
circle = Circle(5, "blue")
assert circle.radius == 5, "The radius is incorrect."
assert circle.color == "blue", "The color is incorrect."

# Test 2: Check area calculation
circle_area = circle.area()
assert isinstance(circle_area, (int, float)) and circle_area > 0, "The area calculation is incorrect."

# Test 3: Check perimeter calculation
circle_perimeter = circle.perimeter()
assert isinstance(circle_perimeter, (int, float)) and circle_perimeter > 0, "The perimeter calculation is incorrect."

print("All Circle assertions passed!")

