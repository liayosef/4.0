class Shape:
    def __init__(self, color):
        """
        Initializes a Shape object with a given color.

        Parameters:
        color (str): The color of the shape.
        """
        self.surface = 0
        self.p = 0
        self.color = color

    def get_color(self, color):
        """
        Sets the color of the shape.

        Parameters:
        color (str): The new color to set.
        """
        self.color = color

    def return_color(self, color):
        """
        Returns the current color of the shape.

        Parameters:
        color (str): The current color of the shape.

        Returns:
        str: The color of the shape.
        """
        return self.color

    def return_surface(self):
        """
        Returns the surface area of the shape.
        This method is a placeholder and should be overridden by subclasses.

        Returns:
        float: The surface area of the shape.
        """
        return self.surface

    def return_p(self):
        """
        Returns the perimeter of the shape.
        This method is a placeholder and should be overridden by subclasses.

        Returns:
        float: The perimeter of the shape.
        """
        return self.p

