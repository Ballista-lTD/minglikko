from django.contrib.auth.decorators import login_required
from django.shortcuts import render

rules = ["maryadak ullathu ullath pole parayanam", "maryadak ullathu ullath pole parayanam", 'kooooooooooooooi']

questions = ['Ningalk ethra budhi ind', 'ningalk ichiri kannil chora indo ', 'ningal ethra dayalu anh']


@login_required(login_url='/')
def index(request):
    if request.method == 'POST':
        tkn = request.user.tokens
        tkn.intelligence = request.POST['intelligence']
        tkn.strength = request.POST['strength']
        tkn.beauty = request.POST['beauty']
        tkn.charisma = request.POST['charisma']
        tkn.wealth = request.POST['wealth']
        tkn.will_help_poor = request.POST['will_help_poor']
        tkn.religiousity = request.POST['religiousity']
        tkn.liberal = request.POST['liberal']
        tkn.save()
    else:
        context1 = {'rules': rules, 'questions': questions, 'submitted': request.user.tokens.total}
        return render(request, template_name='index.html', context=context1)
