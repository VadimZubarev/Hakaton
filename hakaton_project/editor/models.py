from django.db import models

class Formula(models.Model):
    """
    Represents a mathematical formula with a name and text.

    Attributes:
        name (CharField): The name of the formula, limited to 255 characters.
        formula_text (TextField): The text representation of the formula.

    Methods:
        __str__(): Returns the name of the formula or the first 50 characters of the formula text.
    """
    name = models.CharField(max_length=255)
    formula_text = models.TextField()

    def __str__(self):
        return self.name or self.formula_text[:50]