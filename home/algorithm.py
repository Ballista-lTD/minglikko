import random
from pprint import pprint

from django.db.models import Q

from authentication.models import Tokens


def give_random_priority():
    tkns = Tokens.objects.filter().exclude(total=0)
    print(tkns.count())
    for tkn in tkns.all():
        ls = [tk.name for tk in Tokens.objects.all().exclude(total=0).filter(~Q(user=tkn.user))]
        random.shuffle(ls)
        tkn.priority_list = ls
        tkn.save()
        print(tkn.priority_list)


total = tkns = Tokens.objects.all().exclude(total=0).count()


def create_list(ls=1):
    tkns = Tokens.objects.all().exclude(total=0)
    applications = {}

    for tkn in tkns.all():
        prio = {}
        for i in range(len(tkn.priority_list)):
            prio[tkn.priority_list[i]] = i + 1
        if ls == 1:
            applications[tkn.name] = {"prio_list": tkn.priority_list, "accepted": 0}
        else:
            applications[tkn.name] = {"prio_list": prio, "accepted_from": ''}

        return applications


def validate_data(users: dict):
    for user in users:
        if len(set(users[user]['prio_list'])) != total - 1:
            print(user)
            print(len(users[user]['prio_list']), total)

        print(user, end=' = ')
        for next_user in users[user]['prio_list']:
            if next_user not in users:
                print(next_user, end=', ')
        print()


def it():
    accepted = {}
    users = create_list(1)
    clone = create_list(2)

    posts: dict[list] = {}

    for user in users:
        posts[user] = []
    stop = False
    while not stop:
        stop = True
        for user in users:
            user_data = users[user]
            if not user_data['accepted']:
                next_user = user_data['prio_list'].pop(0)
                next_user_info = clone[next_user]
                if not next_user_info['accepted_from']:
                    clone[next_user]['accepted_from'] = user
                    users[user]['accepted'] = 1
                else:
                    old_user = next_user_info['accepted_from']
                    old_user_prio = next_user_info['prio_list'][old_user]
                    new_user_prio = next_user_info['prio_list'][user]
                    if new_user_prio < old_user_prio:
                        clone[next_user]['accepted_from'] = user
                        users[user]['accepted'] = 1
                        user[old_user]['accepted'] = 0
                    stop = False
    return clone
#
# print(it())
