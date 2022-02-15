import random
from pprint import pprint

from authentication.models import Tokens

total = Tokens.objects.all().exclude(total=0).count()

final = [tk.name for tk in Tokens.objects.exclude(total=0)]


def give_random_priority():
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


def create_list():
    tkns = Tokens.objects.all().exclude(total=0)
    applications = {}
    for tkn in tkns.all():
        prio = {}
        for i in range(len(tkn.priority_list)):
            prio[tkn.priority_list[i]] = i

        applications[tkn.name] = {"prio_dict": prio, "accepted": False,
                                  "accepted_from": None, "prio_list": tkn.priority_list, "proposals": []}

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
    users = create_list()
    posts: dict[list] = {}

    for user in users:
        posts[user] = []
    stop = False
    while not stop:

        stop = True
        for user in users:

            sender = users[user]
            if not sender['accepted_from'] and len(sender['prio_list']):
                print(len(sender['prio_list']), end='\n\n')
                users[sender['prio_list'].pop()]['proposals'].append(user)
                stop = False

        for user in users:
            receiver = users[user]

            if len(receiver['proposals']):
                rank, the_name = -1, ""

                for name in receiver['proposals']:
                    if receiver['prio_dict'][name] > rank:
                        rank = receiver['prio_dict'][name]
                        print(the_name)
                        the_name = name

                receiver['proposals'] = []

                if receiver['accepted_from']:
                    if receiver['prio_dict'][receiver['accepted_from']] > rank:
                        break_up = receiver['accepted_from']
                        receiver['accepted_from'] = the_name
                        users[break_up]['accepted_from'] = None
                    else:
                        pass
                else:
                    print(the_name)
                    receiver['accepted_from'] = the_name

    return users


def clear_partners():
    for tkn in Tokens.objects.all():
        tkn.partner = None
        tkn.save()


def perform_algorithm():
    give_random_priority()
    clear_partners()
    result = it()
    data = {}

    # print(result)

    for res in result:
        data[res] = result[res]['accepted_from']
    print(data)
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
        if data[dt]:

            final_list[dt] = data[dt]

    for tkn in final_list:
        print(tkn)
        token = Tokens.objects.get(name=tkn)
        token.set_partner(final_list[tkn])

    print(
        f"Total valids {Tokens.objects.exclude(partner=None).count()}\n invalid pairs = {count_invalid} \n{count_empty =} ")


perform_algorithm()
