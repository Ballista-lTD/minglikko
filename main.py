import json
import sys

sys.setrecursionlimit(360000)

pairs = []


def get_match(user: str, users, seen: list):
    current_user = users[user]

    for next_user in current_user["prio_list"]:
        if next_user not in users or next_user in seen:
            continue

        seen.append(next_user)

        for partner in users[next_user]["prio_list"]:
            if partner == user:
                return user, next_user
            else:
                a, b = get_match(next_user, users, seen)
                if a and b:
                    continue

                return user, next_user
    return None, None


def get_priority(user1, user2, users):
    user1_list = users[user1]['prio_list']
    user2_prio_in_user1 = user1_list.index(user2)

    return user2_prio_in_user1


count = 0


def check_stability(pair, users, data):
    global count
    user1 = pair[0]
    user2 = pair[1]

    user1_list = users[user1]['prio_list']
    user2_list = users[user2]['prio_list']
    user2_prio_in_user1 = get_priority(user1, user2, users)
    user1_prio_in_user2 = get_priority(user2, user1, users)

    user1_list = user1_list[0:user2_prio_in_user1]
    user2_list = user2_list[0:user1_prio_in_user2]
    flag = False
    for i in user1_list:
        i_current_prio = data[i][1]
        i_prio = get_priority(i, user1, users)
        if i_prio < i_current_prio:
            print(f'I fucked up the pairing for ({i},{data[i][0]}) and ({user1},{user2})')
            flag = True

    for i in user2_list:
        i_current_prio = data[i][1]
        i_prio = get_priority(i, user2, users)
        if i_prio < i_current_prio:
            print(f'I fucked up the pairing for ({i},{data[i][0]}) and ({user1},{user2})')
            flag = True
    if flag:
        count += 1


def main():
    users = json.load(open("./data_dict.json"))
    user_names = set(users.keys())

    for user in user_names:

        if user not in users:
            continue

        a, b = get_match(user, users, [])

        if not a or not b:
            print("Lonely ", user)
            continue

        pairs.append((a, b))

        del users[a]
        del users[b]
    users = json.load(open("./data_dict.json"))

    data = {}
    for pair in pairs:
        data[pair[0]] = (pair[1], users[pair[0]]['prio_list'].index(pair[1]))
        data[pair[1]] = (pair[0], users[pair[1]]['prio_list'].index(pair[0]))
    for pair in pairs:
        check_stability(pair, users, data)


if __name__ == "__main__":
    main()
