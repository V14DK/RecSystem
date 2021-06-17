from django.http import JsonResponse
from neo4api.models import *
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json

def index(request):
    return render(request, 'neo4api\\templates\index.html')

def getAllPersons(request):
    if request.method == 'GET':
        persons  = Person.nodes.all()
        response = []
        for person in persons:
            obj = {'name': person.name}
            response.append(obj)
        return JsonResponse(response, safe=False)

def getAllMovies(request):
    if request.method == 'GET':
        movies = Movie.nodes.all()
        response = []
        for movie in movies:
            obj = {'title': movie.title}
            response.append(obj)
        return JsonResponse(response, safe=False)

def getCategories(request):
    if request.method == 'GET':
        categories = Category.nodes.all()
        response = []
        for category in categories:
            obj = {'title': category.name}
            response.append(obj)
        return JsonResponse(response, safe=False)
    
def getTypes(request):
    if request.method == 'GET':
        types = Type.nodes.all()
        response = []
        for type in types:
            obj = {'type': type.type}
            response.append(obj)
        return JsonResponse(response, safe=False)
        
#@csrf_exempt
#def connectPaM(request):
#    if request.method == 'PUT':
#        json_data = json.loads(request.body)
#        name = json_data['name']
#        title = json_data['title']
#        try:
#            person = Person.nodes.get(name=name)
#            movie = Movie.nodes.get(title=title)
#            res = person.movie.connect(movie)
#            response = {"result": res}
#            return JsonResponse(response, safe=False)
#       except:
#            response = {"error": "Error occurred"}
#            return JsonResponse(response, safe=False)