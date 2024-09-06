import Shape

class Rectangle(Shape):
    """
    A class representing a rectangle, inheriting from the Shape class.

    Attributes:
    -----------
    width : float
        The width of the rectangle.
    height : float
        The height of the rectangle.
    color : str
        The color of the rectangle (default is 'blue').
    """

    def __init__(self, width, height, color='blue'):
        """
        Initializes a Rectangle object with a given width, height, and color.

        Parameters:
        -----------
        width : float
            The width of the rectangle.
        height : float
            The height of the rectangle.
        color : str, optional
            The color of the rectangle (default is 'blue').
        """
        super().__init__(color)
        assert isinstance(width, (int, float)) and width > 0, "Width must be a positive number."
        assert isinstance(height, (int, float)) and height > 0, "Height must be a positive number."
        self.width = width
        self.height = height

    def area(self):
        """
        Calculates the area of the rectangle.

        Returns:
        --------
        float
            The area of the rectangle, calculated as width * height.
        """
        area = self.width * self.height
        assert area > 0, "The area should be positive."
        return area

    def perimeter(self):
        """
        Calculates the perimeter of the rectangle.

        Returns:
        --------
        float
            The perimeter of the rectangle, calculated as 2 * (width + height).
        """
        perimeter = 2 * (self.width + self.height)
        assert perimeter > 0, "The perimeter should be positive."
        return perimeter

    def __add__(self, other):
        """
        Adds two Rectangle objects together and returns a new Rectangle object
        with the combined width and height.

        Parameters:
        -----------
        other : Rectangle
            The other rectangle to add.

        Returns:
        --------
        Rectangle
            A new Rectangle object with the combined width and height.
        """
        assert isinstance(other, Rectangle), "The object being added must be a Rectangle."
        new_width = self.width + other.width
        new_height = self.height + other.height
        return Rectangle(new_width, new_height, self.color)


# בדיקות עם assert
# Test 1: Initialize rectangle and check width, height, and color
rect1 = Rectangle(4, 6, "green")
assert rect1.width == 4, "The width is incorrect."
assert rect1.height == 6, "The height is incorrect."
assert rect1.color == "green", "The color is incorrect."

# Test 2: Check area calculation
rect_area = rect1.area()
assert isinstance(rect_area, (int, float)) and rect_area == 24, "The area calculation is incorrect."

# Test 3: Check perimeter calculation
rect_perimeter = rect1.perimeter()
assert isinstance(rect_perimeter, (int, float)) and rect_perimeter == 20, "The perimeter calculation is incorrect."

# Test 4: Add two rectangles together and check the result
rect2 = Rectangle(3, 5, "blue")
combined_rect = rect1 + rect2
assert combined_rect.width == 7, "The combined width is incorrect."
assert combined_rect.height == 11, "The combined height is incorrect."
assert combined_rect.color == "green", "The color of the combined rectangle should match the first rectangle."

print("All Rectangle assertions passed!")
