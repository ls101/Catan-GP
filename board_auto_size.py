def board(n):
    # Initialize list; will be a nested list.
    b = []
    # Add sub-lists with incremented size; start at the number argument
    # and proceed for that many times.
    for x in range(n):
        b.append([0] * (n+x))
    # Starting with the length of the last sub-list, and ending with the
    # length of the argument. range ends at one-before, and with step
    # being -1, all values of x will be one more than required.  Hence
    # the x-1 in the append argument.
    for x in range((len(b[n-1])), n, -1):
        b.append([0] * (x-1))
    # The list is now a hexagon with equal sides.

    # Insert a tuple containing the index numbers; for testing/viewing
    # purposes.
    for i in range(len(b)):
        for j in range(len(b[i])):
            b[i][j] = (i, j)

    return b


def get_neighbor(b):
    # Loop through the nested lists.
    for i in range(len(b)):
        for j in range(len(b[i])):
            # Left neighbors: first element doesn't have one.
            left_n = b[i][j-1] if not j == 0 else None
            # Right neighbor, for all but the last elements in the lists.
            right_n = b[i][j+1] if not j == len(b[i])-1 else None
            # Add top/bottom neighbors:
            # __pass__

            # Print, for testing purposes.
            print('Element: {0}, at left: {1}, at right: {2}\n'.format(
                b[i][j], left_n, right_n
            ))


def main():
    print(board(3))
    print()
    get_neighbor(board(3))


if __name__ == '__main__':
    main()
