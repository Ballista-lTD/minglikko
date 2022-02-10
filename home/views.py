from django.contrib.auth.decorators import login_required
from django.shortcuts import render

rules = ["maryadak ullathu ullath pole parayanam", "maryadak ullathu ullath pole parayanam", 'kooooooooooooooi']


@login_required(login_url='/')
def index(request):
    context1 = {'rules': rules}
    return render(request, template_name='index.html', context=context1)
