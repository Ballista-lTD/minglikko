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
                                  "accepted_from": None, "prio_list": tkn.priority_list}

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

    stop = False
    while not stop:
        stop = True
        for user in users:
            user_data = users[user]
            if not user_data['accepted']:
                next_user = user_data['prio_list'].pop(0)
                next_user_info = users[next_user]
                if not next_user_info['accepted_from']:
                    users[next_user]['accepted_from'] = user
                    users[next_user]['accepted'] = 1
                    users[user]['accepted_from'] = next_user
                    users[user]['accepted'] = 1
                else:
                    old_user = next_user_info['accepted_from']
                    old_user_prio = next_user_info['prio_dict'][old_user]
                    new_user_prio = next_user_info['prio_dict'][user]
                    if new_user_prio < old_user_prio:
                        users[next_user]['accepted_from'] = user
                        users[user]['accepted_from'] = next_user
                        users[user]['accepted'] = 1
                        users[next_user]['accepted'] = 1
                        users[old_user]['accepted'] = 0
                        users[old_user]['accepted_from'] = None
                    stop = False
            else:
                next_user = user_data['prio_list'][0]
                old_user = user_data['accepted_from']
                next_user_prio = user_data['prio_dict'][next_user]
                old_user_prio = user_data['prio_dict'][old_user]
                if next_user_prio < old_user_prio:
                    next_user_info = users[next_user]

                    if not next_user_info['accepted_from']:
                        users[user]['accepted_from'] = next_user
                        users[next_user]['accepted_from'] = user
                        users[user]['accepted'] = 1
                        users[next_user]['accepted'] = 1
                        users[old_user]['accepted'] = 0
                        users[old_user]['accepted_from'] = None
                        user_data['prio_list'].pop(0)
                        stop = False

                    else:
                        new_old_user = next_user_info['accepted_from']
                        new_old_user_prio = next_user_info['prio_dict'][new_old_user]
                        new_new_user_prio = next_user_info['prio_dict'][user]
                        if new_new_user_prio < new_old_user_prio:
                            users[user]['accepted_from'] = next_user
                            users[user]['accepted'] = 1
                            users[next_user]['accepted'] = 1
                            users[next_user]['accepted_from'] = user
                            users[old_user]['accepted'] = 0
                            users[old_user]['accepted_from'] = None
                            users[new_old_user]['accepted'] = 0
                            users[new_old_user]['accepted_from'] = None
                            user_data['prio_list'].pop(0)
                            stop = False

    return users


def clear_chat_friends():
    for tkn in Tokens.objects.all():
        tkn.chat_friends.set([])
        tkn.save()


def get_data():
    # give_random_priority()
    clear_chat_friends()
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
            if dt != data[data[dt]]:
                count_invalid += 1
            lst.extend([dt, data[dt]])
    final_list = {}
    for dt in data:
        if data[dt]:
            final_list[dt] = data[dt]
    for dt in data:
        print(f"({dt},{data[dt]}),({data[dt], data[data[dt]]}) ")

    # print(
    #     f"Total not paired = {set(final) - set(lst)} \n invalid pairs = {count_invalid} \n{count_empty =} ")
    return data


def perform_algorithm():
    data_1 = get_data()
    # data_2 = get_data()
    count = 0
    # for d1 in data_1:
    #
    #     if data_1[d1] != data_2[d1]:
    #         print(f"data_1[{d1}] =  {data_1[d1]},data_2[{d1}] = {data_2[d1]}")
    #         count += 1
    print(f"total number of invalids = {count}")
    for tkn in data_1:
        Tokens.objects.get(name=tkn).set_chat_friends(data_1[tkn])


perform_algorithm()
