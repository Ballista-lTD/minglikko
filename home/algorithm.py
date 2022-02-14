from pprint import pprint

from authentication.models import Tokens

matrix = []
tkns = list(Tokens.objects.filter(total__gt=0).order_by('id'))
token_num = len(tkns)
rows = token_num
for tkn_i in range(rows):
    ls = []
    for tkn_j in range(rows):
        try:
            from_weight = tkns[tkn_i].priority_list.index(tkns[tkn_j].name)
        except (KeyError, ValueError):
            from_weight = 0
        try:
            to_weight = tkns[tkn_j].priority_list.index(tkns[tkn_i].name)
        except (KeyError, ValueError):
            to_weight = 0
        ls.append(token_num - from_weight)
    matrix.append(ls)
pprint(matrix)
