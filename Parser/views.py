from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'Parser/index.html') 
def main(request):
    return render(request, 'Parser/main.html') 