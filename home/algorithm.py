import random
from pprint import pprint

from authentication.models import Tokens

total = Tokens.objects.all().exclude(total=0).count()

final = [tk.name for tk in Tokens.objects.exclude(total=0)]


def give_random_priority():
    print(f"{total = }")
    tkns = Tokens.objects.filter().exclude(total=0)
    print(tkns.count())
    count = 0
    for tkn in tkns:
        count += 1
        ls = list(set(final) - set(tkn.priority_list))
        ls.remove(tkn.name)
        random.shuffle(ls)
        print(len(ls))
        tkn.priority_list.extend(ls)
        tkn.save()
        print(len(tkn.priority_list), len(ls))
    print(f"{count = }")


def print_stats():
    data = {}
    tkns = Tokens.objects.filter().exclude(total=0)
    print(tkns.count())
    for tkn in tkns.all():
        if len(tkn.priority_list) in data.values():
            data[len(tkn.priority_list)] += 1
        else:
            data[len(tkn.priority_list)] = 1
    pprint(data)


def create_list(ls=1):
    tkns = Tokens.objects.all().exclude(total=0)
    applications = {}
    for tkn in tkns.all():
        prio = {}
        for i in range(len(tkn.priority_list)):
            prio[tkn.priority_list[i]] = i + 1

        applications[tkn.name] = {"prio_list": tkn.priority_list if ls else prio, "accepted": False,
                                  "accepted_from": ''}

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
        print('\n\n')


def it():
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
                if not next_user_info['accepted']:
                    clone[next_user]['accepted_from'] = user
                    users[user]['accepted'] = True
                    users[next_user]['accepted'] = True
                else:
                    old_user = next_user_info['accepted_from']
                    old_user_prio = next_user_info['prio_list'][old_user]
                    new_user_prio = next_user_info['prio_list'][user]
                    if new_user_prio < old_user_prio:
                        clone[next_user]['accepted_from'] = user
                        users[user]['accepted'] = True
                        users[next_user]['accepted'] = True
                        users[old_user]['accepted'] = False
                        clone[old_user]['accepted'] = False

                stop = False
    return clone


def perform_algorithm():
    give_random_priority()
    result = it()
    data = {}

    for res in result:
        data[res] = result[res]['accepted_from']

    count_invalid = 0
    count_empty = 0
    lst = []
    for dt in data:
        if data[dt] == '':
            count_empty += 1
        else:
            lst.extend([dt, data[dt]])
    final_list = {}
    for dt in data:
        if data[dt] != '':
            final_list[dt] = data[dt]

    for tkn in final_list:
        token = Tokens.objects.get(name=tkn)
        token.set_partner(final_list[tkn])

    print(f"Total valid pairs {len(lst)}\n invalid pairs = {count_invalid} \n{count_empty =} ")

