
# intersection information
# Will be used as arguments for the Intersection object
# Since the first intersection on the diagram is #1, the fisrt element
# here is None. The index number for each element matches the indentifying
# number on the diagram.
#
# The elements in each item are:
# The identifying number; this is the same as the index number
# The edges connected to each intersection (a tuple)
# The port - if any
# Neighbors, as in: which intersections are on the opposite end of the
# edges connected to this intersection (a tuple)
# The terrains (resources) to which this intersection is connected (a tuple)
#
# All values are integers, as they refer to the index number for the items,
# which are all stored in lists. Or dictoinaries, with integers as keys.

# In short:
# identifying number, edges, port (or None), neighbors, resource identifyer
intersections = [
    None,
    [1, (0, 1, 7), 8, (0, 2, 9), (1,)],
    [2, (0, 2, 1), 8, (0, 1, 3), (1,)],
    [3, (2, 3, 8), None, (2, 4, 11), (1, 2)],
    [4, (0, 4, 3), 0, (0, 3, 5), (2,)],
    [5, (4, 5, 9), 0, (4, 6, 13), (2, 3)],
    [6, (0, 6, 5), None, (0, 5, 7), (3,)],
    [7, (6, 0, 10), None, (6, 15, 0), (3,)],
    [8, (0, 11, 19), 7, (18, 9, 0), (4,)],
    [9, (7, 12, 11), None, (1, 8, 10), (1, 4)],
    [10, (12, 13, 20), None, (9, 11, 20), (1, 4, 5)],
    [11, (8, 14, 13), None, (10, 3, 12), (1, 2, 5)],
    [12, (14, 15, 21), None, (11, 13, 22), (2, 5, 6)],
    [13, (9, 16, 15), None, (5, 12, 14), (2, 3, 6)],
    [14, (16, 17, 22), None, (13, 15, 24), (3, 6, 7)],
    [15, (10, 18, 17), 1, (7, 14, 16), (3, 7)],
    [16, (18, 0, 23), 1, (15, 26, 0), (7,)],
    [17, (0, 24, 34), None, (18, 28, 0), (8,)],
    [18, (19, 25, 24), 7, (8, 17, 19), (4, 8)],
    [19, (25, 26, 35), None, (18, 20, 30), (4, 8, 9)],
    [20, (20, 27, 26), None, (10, 19, 21), (4, 5, 9)],
    [21, (27, 28, 36), None, (20, 22, 32), (5, 9, 10)],
    [22, (21, 29, 28), None, (12, 21, 23), (5, 6, 10)],
    [23, (29, 30, 37), None, (22, 24, 34), (10, 11, 6)],
    [24, (22, 31, 30), None, (23, 14, 25), (6, 7, 11)],
    [25, (31, 32, 38), None, (24, 26, 36), (7, 11, 12)],
    [26, (23, 33, 32), None, (16, 25, 27), (7, 12)],
    [27, (33, 0, 39), 2, (26, 38, 0), (12,)],
    [28, (34, 40, 0), None, (17, 29), (8,)],
    [29, (40, 41, 50), 6, (28, 30, 50), (8, 13)],
    [30, (35, 42, 41), None, (19, 29, 31), (8, 9, 13)],
    [31, (42, 43, 51), None, (30, 32, 41), (9, 13, 14)],
    [32, (36, 44, 43), None, (21, 31, 33), (9, 10, 14)],
    [33, (44, 45, 52), None, (32, 34, 43), (10, 14, 15)],
    [34, (37, 46, 45), None, (23, 33, 35), (10, 11, 15)],
    [35, (46, 47, 53), None, (34, 36, 45), (11, 15, 16)],
    [36, (38, 48, 47), None, (25, 35, 37), (11, 12, 16)],
    [37, (48, 49, 54), None, (36, 38, 47), (12, 16)],
    [38, (39, 0, 49), 2, (37, 27), (12,)],
    [39, (50, 55, 0), 6, (29, 40), (13,)],
    [40, (55, 56, 63), None, (39, 41, 48), (13, 17)],
    [41, (51, 57, 56), None, (31, 40, 42), (13, 14, 17)],
    [42, (57, 58, 64), None, (41, 43, 50), (14, 17, 18)],
    [43, (52, 59, 58), None, (33, 42, 44), (14, 15, 18)],
    [44, (59, 60, 65), None, (43, 45, 52), (15, 18, 19)],
    [45, (53, 61, 60), None, (35, 44, 46), (15, 16, 19)],
    [46, (61, 62, 66), 3, (45, 47, 54), (16, 19)],
    [47, (54, 0, 62), 3, (46, 37, 0), (16,)],
    [48, (63, 67, 0), 5, (40, 49, 0), (17,)],
    [49, (67, 68, 0), 5, (48, 50, 0), (17,)],
    [50, (64, 69, 68), None, (42, 49, 51), (17, 18)],
    [51, (69, 70, 0), 4, (50, 52, 0), (18,)],
    [52, (65, 71, 70), 4, (44, 51, 53), (18, 19)],
    [53, (71, 72, 0), None, (52, 54, 0), (19,)],
    [54, (66, 0, 72), None, (53, 46), (19,)]
]

edges of each terrain from top left corner
terrain_edges = {
        1: [1, 2, 3, 11, 10, 9],
        2: [3, 4, 5, 13, 12, 11],
        3: [5, 6, 7, 15, 14, 13],
        4: [8, 9, 10, 20, 19, 18],
        5: [10, 11, 12, 22, 21, 20],
        6: [12, 13, 14, 24, 23, 22],
        7: [14, 15, 16, 26, 25, 24],
        8: [17, 18, 19, 30, 29, 28],
        9: [19, 20, 21, 32, 31, 30],
        10: [21, 22, 23, 34, 33, 32],
        11: [23, 24, 25, 36, 35, 34],
        12: [25, 26, 27, 38, 37, 36],
        13: [29, 30, 31, 41, 40, 39],
        14: [31, 32, 33, 43, 42, 41],
        15: [33, 34, 35, 45, 44, 43],
        16: [35, 36, 37, 47, 46, 45],
        17: [40, 41, 42, 50, 49, 48],
        18: [42, 43, 44, 52, 51, 50],
        19: [44, 45, 46, 54, 53, 52],

    }




