# RTTdjango
 RepoToText full django

## Steps to Reproduce 

###   If you are just working off of the existing repo  

/$> `poetry install` ###SKIP TO ->

   
###   - Creating the Project  -
   

/$> `poetry init`  -follow the guided init, you can install dependencies here or do them later. this creates the pyproject.toml (installed pygithub, beautifulsoup4, django, django-cors-headers*, djangorestframework*, *not required for a pure django app necessary if you ever decide to split the frontend for another framework)

/$> `poetry install` -installs all the packages and their dependencies

/$> `poetry run django-admin startproject RTTDjango` -creates the RTTDjango project

-> ###HERE

At this point, if you CD into the project folder that is created, and run `poetry run python ./manage.py (just manage.py on windows) runserver` you should be able to go to the adress in your terminal message (127.0.0.1:8000 by default) and see the installation success page. 

You should notice that inside the main RTTDjango directory(we'll refer to it as ROOT), where manage.py is located, there is another RTTDjango folder. If ROOT wasnt specified, RTTDjango will always be referring to this folder. This houses the inner workings of your project. important to note that you will want to put your .env file here as well.

In Django, your project ROOT folder acts as the cell walls, and your inner project folder acts as the nucleus, dictating how things are handled with in the cell. The rest of the functionality is carried out by your "apps," and are created with the `startapp` parameter of django-admin. We'll create the app "Parser" to house our functionalities:

/$> `poetry run django-admin startapp Parser`


# Configuring Settings

Inside RTTDjango, go to settings.py- this is where your configs live. 

## .env file

At the top, import os. You can refer to your .env file by calling it with os.getenv(`variable`)

Your SECRET_KEY can now be put into the .env and called with `SECRET_KEY=os.getenv('SECRET_KEY')`, if you defined it as such in there. It's good practice to do it with all sensitive information like DB parameters and etc.

## INSTALLED_APPS

Many Django-related packages are actually just applications written in Django. As such, they need Django requires them to be declared in the INSTALLED_APPS parameter, where you can already see some of the apps that come out of the box. Not every app will need this, and not every app will be referred to in the same way that they were installed. for example, `djangorestframework` that you install in the command line will need to be declared as `rest_framework` in the settings file. This will take time to get used to, just refer to docs when you get stuck.

Much like packages, the apps we create need to be listed here too. list `Parser` in quotes at the bottom of the list, and dont forget to add the comma.

## TEMPLATES

In the TEMPLATES = [] parameter, change the value of DIRS to [os.path.join(BASE_DIR, "templates")]

## STATIC_FILES

After STATIC_URL, add:

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

### Other

there are other parameters that you will want to get familiar with, such as `CORS_ALLOWED_ORIGINS`, `CSRF_TRUSTED_ORIGINS`, `ALLOWED_HOSTS` so on and so forth, but those you'll pick up as you work with Django. 
##iguring Routing

### urls.py

the urls.py files in Django are your routers. Your project comes with one, but you will want to create one in your apps as well, so we'll create a new file named urls.py in Parser and add the following:

```
from django.urls import path
from . import views

urlpatterns=[
    path('', views.main, name='main'),
]
```

we are importing the django utility path that works like Router in React, and importing the views file from our current directory (Parser), and calling the parser function 'main' at the path '' with the name of 'main'. now we create the view. you usually want to do this before the route, but fuck it, we ball.

#   # views.py

views already has our inital import, render- so we will do a basic view that gives us main.html, which we will create in a bit, and an index view that lets us render our template.

```
def index(request):
    return render(request, 'Parser/index.html')
def main(request):
    return render(request, 'Parser/main.html')
```

#   # templates

In the templates setting earlier, we told django that it needs to look with in the BASE_DIR/templates to find our templates to render. If it cannot find it in the BASE_DIR (our ROOT), since APP_DIRS is set to true by default, it will also look into the app folders for a templates directory. 

It is generally good convention (or just a habit i picked up over time) to create a structure like `app> templates> app> example.html` so that you can keep your templates with their respective app that renders them. another school of thought is to do `templates> app> example.html` in the root directory, and it has its merits, but i like to minimize scrolling in big projects. 

so in the Parser app, we will create a templates> Parser> directory to house our templates, index.html and main.html-

for the sake of brevity i grabbed a template from bootstrap5, downloaded the js and css files (which i placed in ROOT/static/css and /js respectively). the logic is from the STATIC part in settings, if it needs more explaining we can go over it later.

django uses jinja2 for its rendering of templates, and at the top of index.html, there is the tag {% load static %} which tells django to load the static files. this includes:

the static directory in root css: 
```
<link href="{% static 'css/bootstrap.min.css' %}" rel="stylesheet">
<link href="{% static 'css/sticky-footer-navbar.css' %}" rel="stylesheet">
```

the js:

```
<script src="{% static 'js/bootstrap.bundle.js' %}" defer></script>
```

and anything else you might want to store in the static folders. for global things, i like to use the root static directory, but for localized css or js, i would create a static folder within the app, and follow the same filing convention from there as we did with templates. so like `app> static> app> js/css/etc> files`.

when i want to render a js file in that way, the only difference would be adding the app in the href:

```
<script src="{% static 'app/js/bootstrap.bundle.js' %}" defer></script>
```

also in the <main> component in index.html, youll see {% block content %} {% endblock %}. this is because everything we create from here on out will start with an {% extends 'Parser/index.html' %} and populate inside of the <main> component. you can nest these further as well by passing block content tags with in htmls to load partials in as needed. 

i've created a hello world page in the main.html that will show you how it works. 

apart from that, you probably see the unapplied migrations error when you runserver, to clear that up you can do 

/$> `poetry run python ./manage.py (or just manage.py on windows) makemigrations`
this will create migration files for any new models you created, in this case none since all that is in wait are the stock models django comes with

/$> `poetry run python ./manage.py migrate`
this will migrate all of the models from makemigrate into the db and create tables for them accordingly. django comes with sqlite3 built in, so its pretty handy to get started quick. 
