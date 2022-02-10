from django.contrib.auth.decorators import login_required
from django.shortcuts import render

rules = ["maryadak ullathu ullath pole parayanam", "maryadak ullathu ullath pole parayanam", 'kooooooooooooooi']

questions = ['Ningalk ethra budhi ind', 'ningalk ichiri kannil chora indo ', 'ningal ethra dayalu anh']


@login_required(login_url='/')
def index(request):
    if request.method == 'POST':
        tkn = request.user.tokens
        intelligence = request.POST['intelligence']
        strength = request.POST['strength']
        beauty = request.POST['beauty']
        charisma = request.POST['charisma']
        wealth = request.POST['wealth']
        will_help_poor = request.POST['will_help_poor']
        religiousity = request.POST['religiousity']
        liberal = request.POST['liberal']
        total = sum([intelligence, strength, beauty, charisma, wealth, will_help_poor, religiousity, liberal])
        if total > 20:
            tkn.intelligence = intelligence
            tkn.strength = strength
            tkn.beauty = beauty
            tkn.charisma = charisma
            tkn.wealth = wealth
            tkn.will_help_poor = will_help_poor
            tkn.religiousity = religiousity
            tkn.liberal = liberal
            tkn.save()
        context1 = {'rules': rules, 'questions': questions, 'submitted': request.user.tokens.total,
                    'error': "Total must be less than 20"}
        return render(request, template_name='index.html', context=context1)
    else:
        context1 = {'rules': rules, 'questions': questions, 'submitted': request.user.tokens.total}
        return render(request, template_name='index.html', context=context1)
