set_a = {4, 5, 6, 7, 8, 9, 10}
size_a = 7
set_b = {1, 2, 3}
size_b = 3


def average(set):
    ave = 0
    if len(set):
        ave = sum(set) / len(set)
    return ave


def move(set_a, set_b):
    list_a = list(set_a)
    list_a = sorted(list_a)
    count = 0
    flag = True

    while flag:
        elem = 0
        if (len(set_a) > 0):
            for i in set_a:
                if i < average(set_a) and i > average(set_b):
                    elem = i
                    break
            else:
                flag = False
            if flag:
                set_a.remove(elem)
                set_b.add(elem)
                count = count + 1
        else:
            flag = False
    return count


a = move(set_a, set_b)
print(a)

# m,n = input().split()
# set_a = {int(x) for x in input().split()}
# set_b = {int(x) for x in input().split()}
# result = move(set_a,set_b)
# print(result)
