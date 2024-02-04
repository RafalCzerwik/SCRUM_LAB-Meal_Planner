from django.utils import timezone
from django.db import models
from enum import Enum
from django.utils.text import slugify


# Create your models here.

class Recipe(models.Model):
    """
    Model representing a recipe.

    Attributes:
    - name (CharField): The name of the recipe.
    - ingredients (TextField): Ingredients needed for the recipe.
    - description (TextField): Description of the recipe.
    - created (DateTimeField): Date and time when the recipe was created.
    - updated (DateTimeField): Date and time when the recipe was last updated.
    - preparation_time (IntegerField): Time required to prepare the recipe.
    - vote (IntegerField): Number of votes received for the recipe.
    - how_to_prepare (TextField): Instructions on how to prepare the recipe.

    Example usage:
    >>> recipe = Recipe(name='Spaghetti Bolognese', ingredients='Pasta, Meat, Tomatoes', description='Classic Italian dish', preparation_time=30)
    >>> recipe.save()
    """
    name = models.CharField(max_length=255)
    ingredients = models.TextField()
    description = models.TextField()
    created = models.DateTimeField(default=timezone.now, editable=False)
    updated = models.DateTimeField(default=timezone.now, editable=False)
    preparation_time = models.IntegerField()
    vote = models.IntegerField(default=0)
    how_to_prepare = models.TextField(default="I don't know how to prepare it")


class Plan(models.Model):
    """
    Model representing a meal plan.

    Attributes:
    - id (AutoField): Primary key.
    - name (CharField): The name of the meal plan.
    - description (TextField): Description of the meal plan.
    - created (DateTimeField): Date and time when the meal plan was created.

    Methods:
    - __str__(): Method returning a readable representation of the object.

    Example usage:
    >>> plan = Plan(name='Weekly Plan', description='A plan for the entire week')
    >>> plan.save()
    >>> print(plan)
    Weekly Plan
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name


class DayName(Enum):
    """
    Enum representing the names of days in a week.
    """
    MON = 'Poniedziałek'
    TUE = 'Wtorek'
    WED = 'Środa'
    THU = 'Czwartek'
    FRI = 'Piątek'
    SAT = 'Sobota'
    SUN = 'Niedziela'

    def display_name(self):
        return {
            self.MON: 'Poniedziałek',
            self.TUE: 'Wtorek',
            self.WED: 'Środa',
            self.THU: 'Czwartek',
            self.FRI: 'Piątek',
            self.SAT: 'Sobota',
            self.SUN: 'Niedziela',
        }[self]


class RecipePlan(models.Model):
    """
    Model representing a recipe in a meal plan.

    Attributes:
    - recipe (ForeignKey): Foreign key to the Recipe model, specifying the recipe.
    - plan (ForeignKey): Foreign key to the Plan model, specifying the meal plan.
    - meal_name (CharField): Name of the meal in the plan.
    - meal_order (IntegerField): Order of the meal in the plan.
    - day_name (CharField): Name of the day the meal is planned, with choices from DayName enum.

    Methods:
    - __str__(): Method returning a readable representation of the object.

    Example usage:
    >>> recipe = Recipe.objects.get(name='Spaghetti Bolognese')
    >>> plan = Plan.objects.get(name='Weekly Plan')
    >>> recipe_plan = RecipePlan(recipe=recipe, plan=plan, meal_name='Dinner', meal_order=1, day_name=DayName.MON)
    >>> recipe_plan.save()
    >>> print(recipe_plan)
    Weekly Plan
    """
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=255)
    meal_order = models.IntegerField()
    day_name = models.CharField(
        max_length=20,
        choices=[(day.name, day.value) for day in DayName],
        default=DayName.MON.value)

    def __str__(self):
        return self.plan.name


class Page(models.Model):
    """
    Model representing a generic page.

    Attributes:
    - title (CharField): The title of the page, unique.
    - description (TextField): Description of the page.
    - slug (SlugField): Slugified version of the title, unique.

    Methods:
    - save(self, *args, **kwargs): Custom save method to set the slug based on the title.
    - __str__(): Method returning a readable representation of the object.

    Example usage:
    >>> page = Page(title='About Us', description='Information about our company')
    >>> page.save()
    >>> print(page)
    About Us
    """
    title = models.CharField(max_length=255, unique=True, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    slug = models.SlugField(unique=True, null=False, blank=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)

    def __str__(self):
        return self.title
