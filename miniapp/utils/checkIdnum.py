def check_id_data(n):
    if len(str(n)) != 18:
        return False
    else:
        var = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]
        var_id = ['1', '0', 'x', '9', '8', '7', '6', '5', '4', '3', '2']
        n = str(n)
        sum = 0
        for i in range(0, 17):
            sum += int(n[i]) * var[i]
        sum %= 11
        if (var_id[sum]) == str(n[17]):
            return True
        else:
            return False
