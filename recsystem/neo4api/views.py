from django.http.response import HttpResponse
import neomodel
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from .forms import *
from py2neo import Graph
import numpy
import pandas

def arr2arr(preres):
    responce = []
    for arr in preres:
        for item in arr:
            responce.append(item)
    return responce

def index(request):
    if request.method == "POST":
        type = request.POST.get('type')
        category = request.POST.get('category')
        actor = request.POST.get('actor')
        if type == 'None' and category == 'None' and actor == 'None':
            responce = [m.title for m in Movie.nodes.all()[:100]]
            return HttpResponse('<h2>Результат:</h2> {}'.format(responce) )

        if category == 'None' and actor == 'None':
            preres, meta =neomodel.db.cypher_query(query='''MATCH (t:Type) WHERE t.name = '{}'
                                                        MATCH (m:Movie)-[:TYPED_AS]->(t)
                                                        return m.title limit 20'''.format(type))
            return HttpResponse('<h2>Результат:</h2> {}'.format(arr2arr(preres)))

        if type == 'None' and actor == 'None':
            preres, meta =neomodel.db.cypher_query(query='''MATCH (c:Category) WHERE c.name = '{}'
                                                        MATCH (m:Movie)-[:IN_CATEGORY]->(c)
                                                        return m.title limit 20'''.format(category))
            return HttpResponse('<h2>Результат:</h2> {}'.format(arr2arr(preres)))

        if type == 'None' and category == 'None':
            preres, meta =neomodel.db.cypher_query(query='''MATCH (a:Person) WHERE a.name = '{}'
                                                        MATCH (a)-[:ACTED_IN]->(m:Movie)
                                                        return m.title limit 20'''.format(actor))
            return HttpResponse('<h2>Результат:</h2> {}'.format(arr2arr(preres)))
        
        if type == 'None':
            preres, meta =neomodel.db.cypher_query(query='''MATCH (c:Category) WHERE c.name = '{}'
                                                        MATCH (a:Person) WHERE a.name = '{}'
                                                        MATCH (a)-[:ACTED_IN]->(m:Movie)-[:IN_CATEGORY]->(c)
                                                        return m.title limit 20'''.format(category, actor))
            return HttpResponse('<h2>Результат:</h2> {}'.format(arr2arr(preres)))

        if category == 'None':
            preres, meta =neomodel.db.cypher_query(query='''MATCH (t:Type) WHERE t.name = '{}'
                                                        MATCH (a:Person) WHERE a.name = '{}'
                                                        MATCH (a)-[:ACTED_IN]->(m:Movie)-[:TYPED_AS]->(t)
                                                        return m.title limit 20'''.format(type, actor))
            return HttpResponse('<h2>Результат:</h2> {}'.format(arr2arr(preres)))

        if actor == 'None':
            preres, meta =neomodel.db.cypher_query(query='''MATCH (t:Type) WHERE t.type = '{}'
                                                        MATCH (c:Category) WHERE c.name = '{}'
                                                        MATCH (c)<-[:IN_CATEGORY]-(m:Movie)-[:TYPED_AS]->(t)
                                                        return m.title limit 20'''.format(type, category))
            return HttpResponse('<h2>Результат:</h2> {}'.format(arr2arr(preres)))
        
        preres, meta =neomodel.db.cypher_query(query='''MATCH (t:Type) WHERE t.type = '{}'
                                                        MATCH (c:Category) WHERE c.name = '{}'
                                                        MATCH (a:Person) WHERE a.name = '{}'
                                                        MATCH (c)<-[:IN_CATEGORY]-(m:Movie)-[:TYPED_AS]->(t),
                                                        (a)-[:ACTED_IN]->(m)
                                                        return m.title limit 20'''.format(type, category, actor))
        return HttpResponse('<h2>Результат:</h2> {}'.format(arr2arr(preres)))
    
    else:
        form = settingsForm()
        return render(request, "neo4api\\templates\index.html", context={"form": form})

def getRecommendations(request):
    if request.method == 'POST':
        movie = request.POST.get('movie')
        request_link_prediction_movie = """
                                        MATCH (a:Movie {title:$ptitle} )-[*2]-(b:Movie)
                                        WHERE a <> b
                                        WITH DISTINCT a,b
                                        RETURN b.title as recommendation
                                        ORDER BY gds.alpha.linkprediction.adamicAdar(a, b) DESC
                                        LIMIT 25
                                        """
        graph = Graph("bolt://localhost:7687", auth=("neo4j", "123454321"))
        responce = list(graph.run(request_link_prediction_movie, ptitle = movie).to_data_frame()['recommendation'])
        return HttpResponse('<h2>Рекомендации:</h2> {}'.format(responce))
    else:
        form = recommendationsForm()
        return render(request, "neo4api\\templates\index.html", context={"form": form})