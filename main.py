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


def check_stability(pair, pairs, users):
    priority = users[pair[0]]["prio_list"]
    priority = priority[:priority.index(pairs[1])-1]

    for user in priority:



def main():
    users = json.load(open("./data_dict.json"))

    userNames = set(users.keys())

    for user in userNames:

        if user not in users:
            continue

        a, b = get_match(user, users, [])

        if not a or not b:
            print("Lonely ", user)
            continue

        pairs.append((a, b))

        del users[a]
        del users[b]

    print(pairs)
    print(len(pairs))

    for pair in pairs:
        for pair2 in pairs:
            if pair != pair2 and (pair[0] in pair2 or pair[1] in pair2):
                print(pair, pair2)


if __name__ == "__main__":
    main()
