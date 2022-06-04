def solution(dimensions, your_position, trainer_position, distance):
    # Your code here
    distance_square = distance * distance

    def in_circle(x, y):
        return (x * x + y * y) <= distance_square

    def coordinate2angle(t):
        x, y = t
        if x == 0 or y == 0:
            if x == 0 and y == 0:
                return (0, 0)
            elif x == 0:
                if y < 0:
                    return (0, -1)
                else:
                    return (0, 1)
            else:
                if x < 0:
                    return (-1, 0)
                else:
                    return (1, 0)
        else:

            def gcd(a, b):
                if a < b:
                    a, b = b, a
                r = a % b
                while r != 0:
                    a, b = b, r
                    r = a % b
                return b

            tmp = gcd(abs(x), abs(y))
            return (int(x / tmp), int(y / tmp))

    def get_square_distance(t):
        return t[0] * t[0] + t[1] * t[1]

    # find the left top corner square by square in a expand way in the mirror space
    def find_corners(index):

        def index2list(index):
            lis = list()
            for i in range((index + 1) * 2):
                lis.append(i - index - 1)
            return lis

        def get_all_combinations(index):
            outside = index2list(index)
            if index > 0:
                inside = index2list(index - 1)
            combinations = list()
            for i in outside:
                check_j = False
                if  index != 0 and i >= inside[0] and i <= inside[-1]:
                    check_j = True
                for j in outside:
                    if check_j and j >= inside[0] and j <= inside[-1]:
                        continue
                    else:
                        combinations.append((i, j))
            return combinations

        combinations = get_all_combinations(index)
        corners = list()
        for t in combinations:
            corners.append((your_position[0] + 2 * dimensions[0] * t[0],
                            your_position[1] + 2 * dimensions[1] * t[1]))
        return corners

    target_moves = [[trainer_position[0], trainer_position[1]],
                    [-trainer_position[0], trainer_position[1]],
                    [trainer_position[0], -trainer_position[1]],
                    [-trainer_position[0], -trainer_position[1]]]
    self_moves = [[your_position[0], your_position[1]],
                  [-your_position[0], your_position[1]],
                  [your_position[0], -your_position[1]],
                  [-your_position[0], -your_position[1]]]

    def get_points_from_corners(corners, moves):
        lis = list()
        for corner in corners:
            x_c, y_c = corner
            for move in moves:
                x_m, y_m = move
                x_p = x_c + x_m
                y_p = y_c + y_m
                if in_circle(x_p, y_p):
                    lis.append((x_p, y_p))
        return lis

    target_angles = set()
    
    self_angles = set()
    self_angles2distances = dict()
    idx = 0
    while True:
        corners = find_corners(idx)
        targets = get_points_from_corners(corners, target_moves)
        if len(targets) == 0:
            return len(target_angles)
        selfs = get_points_from_corners(corners, self_moves)
        for myself in selfs:
            temp_angle = coordinate2angle(myself)
            if temp_angle in self_angles:
                self_angles2distances[temp_angle].append(get_square_distance(myself))
                # print(len(self_angles[temp_angle]))
            else:
                self_angles.add(temp_angle)
                self_angles2distances[temp_angle] = [get_square_distance(myself)]

        for target in targets:
            target_angle = coordinate2angle(target)
            ignore_this_angle = False
            if target_angle in self_angles:
                this_distance = get_square_distance(target)
                for distance in self_angles2distances[target_angle]:
                    if distance < this_distance:  # hit myself
                        ignore_this_angle = True
                        break

            if ignore_this_angle:
                continue
            else:
                target_angles.add(target_angle)

        idx += 1


def test():
    print(solution([3, 2], [1, 1], [2, 1], 4), 7)
    print(solution([2, 5], [1, 2], [1, 4], 11), 27)
    print(solution([23, 10], [6, 4], [3, 2], 23), 8)
    print(solution([1250, 1250], [1000, 1000], [500, 400], 10000), 196)
    print(solution([10, 10], [4, 4], [3, 3], 5000), 739323)
    print(solution([3, 2], [1, 1], [2, 1], 7), 19)
    print(solution([2, 3], [1, 1], [1, 2], 4), 7)
    print(solution([3, 4], [1, 2], [2, 1], 7), 10)
    print(solution([4, 4], [2, 2], [3, 1], 6), 7)
    print(solution([300, 275], [150, 150], [180, 100], 500), 9)
    print(solution([3, 4], [1, 1], [2, 2], 500), 54243)


test()
