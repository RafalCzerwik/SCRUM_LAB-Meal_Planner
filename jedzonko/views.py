from datetime import datetime

from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.http import Http404, HttpResponseRedirect
import random

from jedzonko.models import Plan, Recipe, RecipePlan, DayName, Page


class IndexView(View):
    """
    View for rendering the home page.

    Methods:
    - get(self, request): Handles GET requests for the home page.
    """
    def get(self, request):
        recipes_list = list(Recipe.objects.all())
        random.shuffle(recipes_list)
        carousel = recipes_list[:3]
        carousel_with_index = [(index, recipe) for index, recipe in enumerate(carousel)]

        plans_count = Plan.objects.count()

        ctx = {
            "actual_date": datetime.now(),
            "carousel_with_index": carousel_with_index,
            "plans_list": plans_count,
            "index": True
        }

        return render(request, "index.html", ctx)


class DashboardView(View):
    """
    View for rendering the dashboard page.

    Methods:
    - get(self, request): Handles GET requests for the dashboard page.
    """
    def get(self, request):
        try:
            latest_plan = Plan.objects.latest('created')
        except Plan.DoesNotExist:
            raise Http404("No plans found")

        days_of_week = [day.value for day in DayName]
        recipe_plans = {day: RecipePlan.objects.filter(plan=latest_plan, day_name=day).order_by('meal_order')
                        for day in days_of_week}

        plans_count = Plan.objects.count()
        recipes_count = Recipe.objects.count()

        context = {
            "list_plans": plans_count,
            "list_recipes": recipes_count,
            'plan': latest_plan,
            'recipe_plans': recipe_plans
        }

        return render(request, "dashboard.html", context)


class LogInView(View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/main/')
        else:
            return render(request, 'login.html',
                          {'error_message': 'Incorrect username por password. Please try again.'})


class RegisterView(View):
    def get(self, request):
        return render(request, 'registration.html')


class RecipeListView(View):
    """
    View for rendering the recipe list page.

    Methods:
    - get(self, request): Handles GET requests for the recipe list page.
    """
    def get(self, request):
        show_special_menu_item = True

        all_recipes = Recipe.objects.all().order_by('-vote', '-created')
        paginator = Paginator(all_recipes, 2)  # must be 50

        page = request.GET.get('page')
        try:
            recipes = paginator.page(page)
        except PageNotAnInteger:
            recipes = paginator.page(1)
        except EmptyPage:
            recipes = paginator.page(paginator.num_pages)

        context = {
            "show_special_menu_item": show_special_menu_item,
            "recipes": recipes,
            "paginator": paginator
        }

        return render(request, 'app-recipes.html', context)


class AddRecipeView(View):
    """
    View for adding a new recipe.

    Methods:
    - get(self, request): Handles GET requests for the add recipe page.
    - post(self, request): Handles POST requests for adding a new recipe.
    """
    def get(self, request):
        return render(request, "app-add-recipe.html")

    def post(self, request):
        recipe_name = request.POST.get('recipe_name')
        description = request.POST.get('description')
        preparation_time = request.POST.get('preparation_time')
        ingredients = request.POST.get('ingredients')
        how_to_prepare = request.POST.get('how_to_prepare')
        new_recipe = Recipe(name=recipe_name,
                            description=description,
                            preparation_time=preparation_time,
                            ingredients=ingredients,
                            how_to_prepare=how_to_prepare
                            )

        if not (recipe_name and description and ingredients and how_to_prepare and preparation_time):
            error_message = "Wypełnij poprawnie wszystkie pola"
            context = {"recipe": new_recipe, "error_message": error_message}
            return render(request, "app-add-recipe.html", context)
        else:
            new_recipe = Recipe(name=recipe_name,
                                description=description,
                                preparation_time=preparation_time,
                                ingredients=ingredients,
                                how_to_prepare=how_to_prepare
                                )
            new_recipe.save()
            return redirect('recipe_list')


class RecipeDetailsView(View):
    """
    View for rendering recipe details and handling voting.

    Methods:
    - get(self, request, id): Handles GET requests for displaying recipe details.
    - post(self, request, id): Handles POST requests for voting on a recipe.
    """
    def get(self, request, id):
        recipe = Recipe.objects.filter(id=id)
        show_special_menu_item = True
        context = {"show_special_menu_item": show_special_menu_item, 'id': id, 'recipe': recipe[0]}
        return render(request, "app-recipe-details.html", context)

    def post(self, request, id):
        vote = int(request.POST.get('vote'))
        recipe = Recipe.objects.get(id=id)
        recipe.vote += vote
        recipe.save()
        show_special_menu_item = True
        context = {"show_special_menu_item": show_special_menu_item, 'id': id, 'recipe': recipe}
        return render(request, "app-recipe-details.html", context)


class RecipeModifyView(View):
    """
    View for modifying a recipe.

    Methods:
    - get(self, request, id): Handles GET requests for displaying the recipe modification form.
    - post(self, request, id): Handles POST requests for modifying a recipe.
    """
    def get(self, request, id):
        recipe = get_object_or_404(Recipe, id=id)
        context = {"recipe": recipe}
        return render(request, "app-edit-recipe.html", context)

    def post(self, request, id):
        recipe_name = request.POST.get('recipe_name')
        description = request.POST.get('description')
        preparation_time = request.POST.get('preparation_time')
        ingredients = request.POST.get('ingredients')
        how_to_prepare = request.POST.get('how_to_prepare')
        new_recipe = Recipe(name=recipe_name,
                            description=description,
                            preparation_time=preparation_time,
                            ingredients=ingredients,
                            how_to_prepare=how_to_prepare
                            )

        if not (recipe_name and description and ingredients and how_to_prepare and preparation_time):
            error_message = "Wypełnij poprawnie wszystkie pola"
            context = {"recipe": new_recipe, "error_message": error_message}
            return render(request, "app-edit-recipe.html", context)
        else:
            new_recipe = Recipe(name=recipe_name,
                                description=description,
                                preparation_time=preparation_time,
                                ingredients=ingredients,
                                how_to_prepare=how_to_prepare
                                )
            new_recipe.save()
            return redirect('recipe_list')


class AddPlanView(View):
    """
    View for adding a new meal plan.

    Methods:
    - get(self, request): Handles GET requests for the add meal plan page.
    - post(self, request): Handles POST requests for adding a new meal plan.
    """
    def get(self, request):
        return render(request, "app-add-schedules.html")

    def post(self, request):

        recipe_name = request.POST.get('name')
        recipe_description = request.POST.get('description')

        if not recipe_name and not recipe_description:
            error_message = 'Wypełnij oba pola'
        elif not recipe_name:
            error_message = 'Wypełnij nazwę planu'
        elif not recipe_description:
            error_message = 'Wypełnij opis planu'
        else:
            new_plan = Plan(name=recipe_name, description=recipe_description)
            new_plan.save()

            return redirect('plan_details', id=new_plan.id)

        return render(request, 'app-add-schedules.html', {'error_message': error_message})


class AddRecipeToPlanView(View):
    """
    View for adding a recipe to a meal plan.

    Methods:
    - get(self, request): Handles GET requests for the add recipe to plan page.
    - post(self, request): Handles POST requests for adding a recipe to a meal plan.
    """
    def get(self, request):
        plans = Plan.objects.all()
        recipes = Recipe.objects.all()
        days = [(day.value, day.display_name()) for day in DayName]

        return render(request, "app-schedules-meal-recipe.html", {'plans': plans,
                                                                  'recipes': recipes,
                                                                  'days': days})

    def post(self, request):
        if request.method == "POST":
            recipe = request.POST.get('recipie')
            plan = request.POST.get('choosePlan')
            meal_name = request.POST.get('name')
            meal_order = request.POST.get('number')
            day_name = request.POST.get('day')

            plan = Plan.objects.get(pk=plan)
            recipe = Recipe.objects.get(pk=recipe)

            recipe_plan = RecipePlan(recipe=recipe,
                                     plan=plan,
                                     meal_name=meal_name,
                                     meal_order=meal_order,
                                     day_name=day_name
                                     )
            recipe_plan.save()

            return redirect('plan_details', id=plan.id)

        return render(request, 'app-schedules-meal-recipe.html')

    def post(self, request, error_message=None):

        if request.method == "POST":
            recipe = request.POST.get('recipie')
            plan = request.POST.get('choosePlan')
            meal_name = request.POST.get('name')
            meal_order = request.POST.get('number')
            day_name = request.POST.get('day')
            error_message = ''

            return redirect('plan/add-recipe')

        return render(request, 'app-schedules-meal-recipe.html', {'error_message': error_message})


class PlanListView(View):
    """
    View for rendering the list of meal plans.

    Methods:
    - get(self, request): Handles GET requests for the meal plan list page.
    """
    def get(self, request):
        show_special_menu_item = True

        all_plans = Plan.objects.all().order_by('name')
        paginator = Paginator(all_plans, 3)  # must be 50

        page = request.GET.get('page')
        try:
            plans = paginator.page(page)
        except PageNotAnInteger:
            plans = paginator.page(1)
        except EmptyPage:
            plans = paginator.page(paginator.num_pages)

        context = {
            "show_special_menu_item": show_special_menu_item,
            "plans": plans,
            "paginator": paginator
        }
        return render(request, 'app-schedules.html', context)


class PlanDetailsView(View):
    """
    View for rendering meal plan details.

    Methods:
    - get(self, request, id): Handles GET requests for displaying meal plan details.
    """
    def get(self, request, id):
        show_special_menu_item = True
        plan = get_object_or_404(Plan, pk=id)
        days = [day.value for day in DayName]
        meals = RecipePlan.objects.filter(plan=plan).order_by('meal_order')

        context = {"plan": plan, "days": days, "meals": meals, "show_special_menu_item": show_special_menu_item}

        return render(request, 'app-details-schedules.html', context)
