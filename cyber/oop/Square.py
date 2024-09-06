import Shape


class Square(Shape):
    """
    A class representing a square, inheriting from the Shape class.

    Attributes:
    -----------
    width : float
        The width of the square.
    height : float
        The height of the square.
    color : str
        The color of the square (default is 'blue').
    """

    def __init__(self, width, height, color='blue'):
        """
        Initializes a Square object with a given width, height, and color.

        Parameters:
        -----------
        width : float
            The width of the square.
        height : float
            The height of the square.
        color : str, optional
            The color of the square (default is 'blue').
        """
        super().__init__(color)
        assert isinstance(width, (int, float)) and width > 0, "Width must be a positive number."
        assert isinstance(height, (int, float)) and height > 0, "Height must be a positive number."
        self.width = width
        self.height = height

    def area(self):
        """
        Calculates the area of the square.

        Returns:
        --------
        float
            The area of the square, calculated as width * height.
        """
        area = self.width * self.height
        assert area > 0, "The area should be positive."
        return area

    def perimeter(self):
        """
        Calculates the perimeter of the square.

        Returns:
        --------
        float
            The perimeter of the square, calculated as 2 * (width + height).
        """
        perimeter = 2 * (self.width + self.height)
        assert perimeter > 0, "The perimeter should be positive."
        return perimeter

    def __add__(self, other):
        """
        Adds two Square objects together and returns a new Square object.

        Parameters:
        -----------
        other : Square
            The other square to add.

        Returns:
        --------
        Square
            A new Square object with the combined area and perimeter of the two squares.
        """
        assert isinstance(other, Square), "The object being added must be a Square."
        new_width = self.width + other.width
        new_height = self.height + other.height
        return Square(new_width, new_height, self.color)


# בדיקות עם assert
# Test 1: Initialize square and check width, height, and color
square1 = Square(5, 5, "red")
assert square1.width == 5, "The width is incorrect."
assert square1.height == 5, "The height is incorrect."
assert square1.color == "red", "The color is incorrect."

# Test 2: Check area calculation
square_area = square1.area()
assert isinstance(square_area, (int, float)) and square_area == 25, "The area calculation is incorrect."

# Test 3: Check perimeter calculation
square_perimeter = square1.perimeter()
assert isinstance(square_perimeter, (int, float)) and square_perimeter == 20, "The perimeter calculation is incorrect."

# Test 4: Add two squares together and check the result
square2 = Square(3, 3, "blue")
combined_square = square1 + square2
assert combined_square.width == 8, "The combined width is incorrect."
assert combined_square.height == 8, "The combined height is incorrect."
assert combined_square.color == "red", "The color of the combined square should match the first square."

print("All Square assertions passed!")
