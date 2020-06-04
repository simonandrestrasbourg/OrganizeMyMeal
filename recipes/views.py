from django.shortcuts import render


def index(request):
    """ Index page """
    context = {}
    return render(request, 'recipes/index.html', context)
