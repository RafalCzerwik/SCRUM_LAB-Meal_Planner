"""scrumlab URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from jedzonko.views import (
    IndexView,
    DashboardView,
    RecipeModifyView,
    AddRecipeView,
    RecipeListView,
    RecipeDetailsView,
    AddRecipeToPlanView,
    AddPlanView,
    PlanListView,
    PlanDetailsView,
    LogInView,
    RegisterView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('main/', DashboardView.as_view(), name='dashboard'),
    path('login/', LogInView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('recipe/<int:id>/', RecipeDetailsView.as_view(), name='recipe_details'),
    path('recipe/list/', RecipeListView.as_view(), name='recipe_list'),
    path('recipe/add/', AddRecipeView.as_view(), name='add_recipe'),
    path('recipe/modify/<int:id>/', RecipeModifyView.as_view(), name='modify_recipe'),
    path('plan/add/', AddPlanView.as_view(), name='add_plan'),
    path('plan/add-recipe/', AddRecipeToPlanView.as_view(), name='add_recipe_to_plan'),
    path('plan/list/', PlanListView.as_view(), name='plan_list'),
    path('plan/<int:id>/', PlanDetailsView.as_view(), name='plan_details'),
]