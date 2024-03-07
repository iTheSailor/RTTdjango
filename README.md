# RTTdjango
 RepoToText full django

# Steps to Reproduce #
#   -   -   -   -   -   -   -
#   - Creating the Project  -
#   -   -   -   -   -   -   -
/$> `poetry init`  -follow the guided init, you can install dependencies here or do them later. this creates the pyproject.toml (installed pygithub, beautifulsoup4, django, django-cors-headers*, djangorestframework*, *not required for a pure django app necessary if you ever decide to split the frontend for another framework)

/$> `poetry install` -installs all the packages and their dependencies

/$> `poetry run django-admin startproject RTTDjango` -creates the RTTDjango project

At this point, if you CD into the project folder that is created, and run `poetry run manage.py runserver` you should be able to go to the adress in your terminal message (127.0.0.1:8000 by default) and see the installation success page. 

You should notice that inside the main RTTDjango directory(we'll refer to it as ROOT), where manage.py is located, there is another RTTDjango folder. If ROOT wasnt specified, RTTDjango will always be referring to this folder. This houses the inner workings of your project. important to note that you will want to put your .env file here as well.

In Django, your project ROOT folder acts as the cell walls, and your inner project folder acts as the nucleus, dictating how things are handled with in the cell. The rest of the functionality is carried out by your "apps," and are created with the `startapp` parameter of django-admin. We'll create the app "Parser" to house our functionalities:

/$> `poetry run django-admin startapp Parser`


# Configuring Settings

Inside RTTDjango, go to settings.py- this is where your configs live. 

#   # .env file

At the top, import os. You can refer to your .env file by calling it with os.getenv(`variable`)

Your SECRET_KEY can now be put into the .env and called with `SECRET_KEY=os.getenv('SECRET_KEY')`, if you defined it as such in there. It's good practice to do it with all sensitive information like DB parameters and etc.

#   # INSTALLED_APPS

Many Django-related packages are actually just applications written in Django. As such, they need Django requires them to be declared in the INSTALLED_APPS parameter, where you can already see some of the apps that come out of the box. Not every app will need this, and not every app will be referred to in the same way that they were installed. for example, `djangorestframework` that you install in the command line will need to be declared as `rest_framework` in the settings file. This will take time to get used to, just refer to docs when you get stuck.

Much like packages, the apps we create need to be listed here too. list `Parser` in quotes at the bottom of the list, and dont forget to add the comma.

#   # STATIC_FILES

After STATIC_URL, add STATIC_FILES = os.path.join(BASE_DIR, 'static')


#   #   # Other

there are other parameters that you will want to get familiar with, such as `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`, `ALLOWED_HOSTS` so on and so forth, but those you'll pick up as you work with Django. 


# Configuring Routing

#   # urls.py

the urls.py files in Django are your routers. Your project comes with one, but you will want to create one in your apps as well, so we'll create a new file named urls.py in Parser