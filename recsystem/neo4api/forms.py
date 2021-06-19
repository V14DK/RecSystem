from django import forms
from .models import *
import neomodel

def doTuple(type):
    if type == Type:
        data = [n.type for n in type.nodes.all()]
    elif type == Category:
        data = [n.name for n in type.nodes.all()]
    elif type == Movie:
        data = [n.title for n in type.nodes.all()]
    else:
        predata, meta = neomodel.db.cypher_query(query='''MATCH (a:Person)-[:ACTED_IN]->(:Movie)
                                                return a.name limit 100''')
        data = []
        for arr in predata:
            for item in arr:
                data.append(item)
    res = {}
    res['None'] = ''
    for i in range(len(data)):
        res[data[i]] = data[i]
    return tuple((k, v) for k, v in res.items())
 
class settingsForm(forms.Form):
    type = forms.ChoiceField(choices = doTuple(Type), label='Тип')
    category = forms.ChoiceField(choices = doTuple(Category),label='Жанр')
    actor = forms.ChoiceField(choices = doTuple(Person), label='Актер')

class recommendationsForm(forms.Form):
    movie = forms.ChoiceField(choices = doTuple(Movie), label='Фильм')