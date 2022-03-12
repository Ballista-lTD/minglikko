import json
from collections import OrderedDict
from datetime import datetime

import matplotlib.pyplot as plt

user = {
}


def get_users():
    with open('data_dict.json', 'r') as f:
        users = json.loads(f.read())
        return OrderedDict(users)


def get_data(num):
    users = get_users()
    applications = {}
    to_remove = list(users.keys())[num:]
    # print(to_remove)
    j = 0
    for i in users:
        if j == num:
            break

        applications[i] = users[i]
        applications[i]['prio_dict'] = {}
        applications[i]['prio_list'] = list(set(applications[i]['prio_list']) - set(to_remove))
        for prio in applications[i]['prio_list']:
            applications[i]['prio_dict'][prio] = list(applications[i]['prio_list']).index(prio)
        j += 1
    return applications


def it(users):
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

    ls = []
    for user in users:
        ls.append((user, users[user]['accepted_from']))
    return ls


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


def on3(users):
    pairs = []
    user_names = set(users.keys())

    for user in user_names:

        if user not in users:
            continue

        a, b = get_match(user, users, [])

        if not a or not b:
            # print("Lonely ", user)
            continue

        pairs.append((a, b))

        del users[a]
        del users[b]
    return pairs


# def main():
#     final_data = {'optimal': {}, 'recursive': {}}
#     for i in range(10, 400, 2):
#         users = get_data(i)
#         initial_time = datetime.now()
#         it(users)
#         final_time = (datetime.now() - initial_time).microseconds
#         final_data['optimal'][i] = final_time
#         initial_time = datetime.now()
#         on3(users)
#         final_time = (datetime.now() - initial_time).microseconds
#         final_data['recursive'][i] = final_time
#     with open('timing.py', 'a') as f:
#         f.write(f"{final_data  = }")
# final_data = {
#     'optimal': {10: 0, 12: 0, 14: 985, 16: 0, 18: 0, 20: 0, 22: 0, 24: 0, 26: 0, 28: 1006, 30: 0, 32: 1000, 34: 0,
#                 36: 0, 38: 993, 40: 1015, 42: 1029, 44: 1000, 46: 984, 48: 3000, 50: 2001, 52: 999, 54: 999, 56: 1000,
#                 58: 1988, 60: 1009, 62: 1988, 64: 1993, 66: 2026, 68: 3028, 70: 1993, 72: 3974, 74: 1923, 76: 3023,
#                 78: 2993, 80: 3998, 82: 3967, 84: 3998, 86: 3986, 88: 4046, 90: 4973, 92: 4000, 94: 4995, 96: 4972,
#                 98: 5977, 100: 5015, 102: 6001, 104: 6004, 106: 5984, 108: 6985, 110: 7999, 112: 5999, 114: 6998,
#                 116: 6999, 118: 7964, 120: 6984, 122: 11018, 124: 10007, 126: 7964, 128: 7971, 130: 8026, 132: 12024,
#                 134: 18984, 136: 10999, 138: 10031, 140: 10001, 142: 13986, 144: 11000, 146: 9998, 148: 13988, 150: 0,
#                 152: 15636, 154: 11997, 156: 12001, 158: 12999, 160: 12998, 162: 14997, 164: 14999, 166: 14001,
#                 168: 15032, 170: 16035, 172: 15038, 174: 14998, 176: 15996, 178: 17001, 180: 16998, 182: 18000,
#                 184: 19000, 186: 19034, 188: 18996, 190: 18944, 192: 20024, 194: 22000, 196: 22018, 198: 22001,
#                 200: 23970, 202: 21997, 204: 24993, 206: 24950, 208: 26995, 210: 25980, 212: 26973, 214: 27990,
#                 216: 31283, 218: 15628, 220: 28036, 222: 28050, 224: 27028, 226: 46881, 228: 31287, 230: 31255,
#                 232: 31965, 234: 30986, 236: 33000, 238: 33002, 240: 34998, 242: 36999, 244: 36000, 246: 35966,
#                 248: 36001, 250: 40001, 252: 37999, 254: 38001, 256: 38000, 258: 45997, 260: 42000, 262: 46848,
#                 264: 41980, 266: 46999, 268: 46874, 270: 51989, 272: 44002, 274: 32889, 276: 48999, 278: 44002,
#                 280: 46881, 282: 55007, 284: 46863, 286: 50978, 288: 50034, 290: 51965, 292: 54996, 294: 54002,
#                 296: 62501, 298: 66996, 300: 69001, 302: 94967, 304: 56983, 306: 57037, 308: 46847, 310: 52999,
#                 312: 56000, 314: 59001, 316: 58002, 318: 58005, 320: 92997, 322: 62507, 324: 63034, 326: 64999,
#                 328: 62048, 330: 61965, 332: 63000, 334: 68964, 336: 69996, 338: 69000, 340: 76033, 342: 73997,
#                 344: 75038, 346: 77032, 348: 148994, 350: 82984, 352: 78128, 354: 109831, 356: 94267, 358: 93750,
#                 360: 93753, 362: 109375, 364: 78081, 366: 109377, 368: 78161, 370: 109363, 372: 93750, 374: 96002,
#                 376: 100004, 378: 94967, 380: 103001, 382: 99032, 384: 112993, 386: 102003, 388: 98997, 390: 120002,
#                 392: 106000, 394: 106038, 396: 109000, 398: 107036},
#     'recursive': {10: 0, 12: 0, 14: 0, 16: 0, 18: 0, 20: 995, 22: 0, 24: 1002, 26: 1024, 28: 0, 30: 1000, 32: 999,
#                   34: 1990, 36: 2032, 38: 1999, 40: 1998, 42: 2993, 44: 2999, 46: 3002, 48: 5001, 50: 6000, 52: 6000,
#                   54: 6015, 56: 8972, 58: 8969, 60: 9005, 62: 9000, 64: 8985, 66: 9014, 68: 15973, 70: 10011, 72: 18001,
#                   74: 14040, 76: 16999, 78: 22997, 80: 32970, 82: 33034, 84: 34002, 86: 47963, 88: 43987, 90: 45002,
#                   92: 43999, 94: 49005, 96: 57999, 98: 72033, 100: 77976, 102: 86967, 104: 74014, 106: 75002,
#                   108: 93999, 110: 91004, 112: 101033, 114: 105002, 116: 108033, 118: 141002, 120: 158999, 122: 159998,
#                   124: 146999, 126: 161037, 128: 173034, 130: 200001, 132: 195981, 134: 273993, 136: 250033,
#                   138: 237972, 140: 242999, 142: 251014, 144: 262964, 146: 287981, 148: 300039, 150: 296875,
#                   152: 338303, 154: 315038, 156: 346997, 158: 406001, 160: 368998, 162: 407003, 164: 416964,
#                   166: 486000, 168: 454002, 170: 459967, 172: 467962, 174: 499966, 176: 611998, 178: 498963,
#                   180: 476997, 182: 516001, 184: 504001, 186: 603001, 188: 659032, 190: 668001, 192: 628968,
#                   194: 629997, 196: 720985, 198: 786968, 200: 769028, 202: 844003, 204: 816998, 206: 891997,
#                   208: 919972, 210: 917000,}}
final_data = {
    'optimal': {10: 0, 12: 0, 14: 985, 16: 0, 18: 0, 20: 0, 22: 0, 24: 0, 26: 0, 28: 1006, 30: 0, 32: 1000, 34: 0,
                36: 0, 38: 993, 40: 1015, 42: 1029, 44: 1000, 46: 984, 48: 3000, 50: 2001, 52: 999, 54: 999, 56: 1000,
                58: 1988, 60: 1009, 62: 1988, 64: 1993, 66: 2026, 68: 3028, 70: 1993, 72: 3974, 74: 1923, 76: 3023,
                78: 2993, 80: 3998, 82: 3967, 84: 3998, 86: 3986, 88: 4046, 90: 4973, 92: 4000, 94: 4995, 96: 4972,
                98: 5977, 100: 5015, 102: 6001, 104: 6004, 106: 5984, 108: 6985, 110: 7999, 112: 5999, 114: 6998,
                116: 6999, 118: 7964, 120: 6984, 122: 11018, 124: 10007, 126: 7964, 128: 7971, 130: 8026, 132: 12024,
                134: 18984, 136: 10999, 138: 10031, 140: 10001, 142: 13986, 144: 11000, 146: 9998, 148: 13988, 150: 14988,
                152: 15636, 154: 11997, 156: 12001, 158: 12999, 160: 12998, 162: 14997, 164: 14999, 166: 14001,
                168: 15032, 170: 16035, 172: 15038, 174: 14998, 176: 15996, 178: 17001, 180: 16998, 182: 18000,
                184: 19000, 186: 19034, 188: 18996, 190: 18944, 192: 20024, 194: 22000, 196: 22018, 198: 22001,
                200: 23970, 202: 21997, 204: 24993, 206: 24950, 208: 26995, 210: 25980, },
    'recursive': {10: 0, 12: 0, 14: 0, 16: 0, 18: 0, 20: 995, 22: 0, 24: 1002, 26: 1024, 28: 0, 30: 1000, 32: 999,
                  34: 1990, 36: 2032, 38: 1999, 40: 1998, 42: 2993, 44: 2999, 46: 3002, 48: 5001, 50: 6000, 52: 6000,
                  54: 6015, 56: 8972, 58: 8969, 60: 9005, 62: 9000, 64: 8985, 66: 9014, 68: 15973, 70: 10011, 72: 18001,
                  74: 14040, 76: 16999, 78: 22997, 80: 32970, 82: 33034, 84: 34002, 86: 47963, 88: 43987, 90: 45002,
                  92: 43999, 94: 49005, 96: 57999, 98: 72033, 100: 77976, 102: 86967, 104: 74014, 106: 75002,
                  108: 93999, 110: 91004, 112: 101033, 114: 105002, 116: 108033, 118: 141002, 120: 158999, 122: 159998,
                  124: 146999, 126: 161037, 128: 173034, 130: 200001, 132: 195981, 134: 273993, 136: 250033,
                  138: 237972, 140: 242999, 142: 251014, 144: 262964, 146: 287981, 148: 300039, 150: 296875,
                  152: 338303, 154: 315038, 156: 346997, 158: 406001, 160: 368998, 162: 407003, 164: 416964,
                  166: 486000, 168: 454002, 170: 459967, 172: 467962, 174: 499966, 176: 611998, 178: 498963,
                  180: 476997, 182: 516001, 184: 504001, 186: 603001, 188: 659032, 190: 668001, 192: 628968,
                  194: 629997, 196: 720985, 198: 786968, 200: 769028, 202: 844003, 204: 816998, 206: 891997,
                  208: 919972, 210: 917000,}}


def main():
    y = [x / 1000 for x in final_data['optimal'].values()]
    plt.plot(final_data['optimal'].keys(), y)
    plt.xlabel("Num of entities")  # add X-axis label
    plt.ylabel("time")  # add Y-axis label
    plt.title("Optimal")  # add title
    plt.show()
    y = [x / 1000 for x in final_data['recursive'].values()]

    plt.plot(final_data['recursive'].keys(), y)
    plt.xlabel("Num of entities")  # add X-axis label
    plt.ylabel("time")  # add Y-axis label
    plt.title("Recursive")  # add title
    plt.show()


if __name__ == "__main__":
    main()

