import math


vars_dict = {}
rename_dict = {}

next_val = 0


def set_next(var):
    global next_val
    next_val += 1
    vars_dict[var] = next_val


def get_dict(var):
    rn = rename_dict.get(var, var)
    return vars_dict.get(rn, rn)


def solution(arr1, arr2):
    if len(arr1) != len(arr2):
        return False
    for a, b in zip(arr1, arr2):
        if a.isnumeric():
            a = int(a)
        else:
            a = get_dict(a)
        if b.isnumeric():
            b = int(b)
        else:
            b = get_dict(b)

        if isinstance(a, int) and isinstance(b, int):
            if a != b:
                return False
            continue
        if isinstance(a, int):
            vars_dict[b] = a
            continue
        if isinstance(b, int):
            vars_dict[a] = b
            continue
        rename_dict[a] = b

    return True


if __name__ == '__main__':
    input()
    first_array = input()
    second_array = input()
    if solution(first_array.split(), second_array.split()):
        print('YES')
    else:
        print('NO')
