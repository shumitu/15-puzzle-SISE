
def string_mean(result):
    sum_of_str = [0 for i in range(len(result))]
    no_of_elems = [0 for i in range(len(result))]
    averages = [0 for i in range(len(result))]
    for i in range(len(result)):
        for j in range(len(result[i])):
            sum_of_str[i] += len(result[i][j][0])
            no_of_elems[i] += 1

    for i in range(len(sum_of_str)):
        averages[i] = sum_of_str[i] / no_of_elems[i]

    return averages

def main():

    a = [[("adadda", 2131, 1313, 131),("adadddaddaa", 2131, 1313, 131)],[("addddddddddadda", 2131, 1313, 131), ("adadda", 2131, 1313, 131), ("ada", 2131, 1313, 131)]]

    print(a[0][0][0])
    print(len(a[0][0][0]))
    b = string_mean(a)
    print(b)


if __name__ == "__main__":
    main()