# SCRUM_LAB-Meal_Planner (Plan Your Meal)

This project was developed as part of a Scrum Lab exercise, written in Python using the Django framework. It is a collaborative effort created in a single sprint, providing an opportunity for team members to experience real-life programming scenarios.

## Features

- Create and manage meal plans with associated recipes.
- View, add, modify, and delete recipes.
- Plan your weekly meals with ease.
- User-friendly interface for an optimal user experience.

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RafalCzerwik/SCRUM_LAB-Meal_Planner.git


2. **Navigate to the project directory:**

    ```bash
    cd scrum-lab-meal-planner

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt

4. **Configure the database:**

- Open **settings.py** in the **meal_planner** directory.
- Modify the **DATABASES** setting to match your database configuration.

    ```python
    #  setting.py

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_database_name',
            'USER': 'your_database_user',
            'PASSWORD': 'your_database_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```
    Alternatively, you can create a **local_settings.py** file in the same directory as **settings.py** and include your database configuration there:

    ```python
    #  local_settings.py

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'your_database_name',
            'USER': 'your_database_user',
            'PASSWORD': 'your_database_password',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```
    Ensure that you add **local_settings.py** to your **.gitignore** file to avoid sharing sensitive information.

5. **Apply migrations:**

    ```bash
    python manage.py migrate

6. **Run the development server:**

    ```bash
    python manage.py runserver

7. **Visit http://localhost:8000 in your browser to access the application.**

## Contributing
Contributions are welcome! Feel free to open issues or pull requests.

## License
This project is not licensed. You are free to use, modify, and distribute it without any restrictions.