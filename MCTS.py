from math import sqrt, log
import numpy as np
import random
import copy
import datetime
import sys

sys.setrecursionlimit(10000)


class Node:

    def __init__(self, parent_node, checker_board, color):
        self.parent_node = parent_node
        self.checker_board = checker_board  # 一个二维数组，-1为黑，0为未落子，1为白。为np array
        self.color = color  # color的逻辑仍需修改

    unfolding = False
    value = 0
    visit_number = 0
    unfolding = False
    child_list = None

    def b_w_number(self):  # 返回棋盘上的黑白子数目,顺序为黑、空点、白
        black_number = 0
        write_number = 0
        space_number = 0
        for i in range(0, 8):
            for j in range(0, 8):
                if self.checker_board[i][j] == 1:
                    write_number += 1
                elif self.checker_board[i][j] == -1:
                    black_number += 1
                else:
                    space_number += 1
        return [black_number, space_number, write_number]

    def is_terminate(self):  # 返回是否为终局结点，若为终局，则会得出输赢，更新value
        terminate = False
        black = self.b_w_number()[0]
        space = self.b_w_number()[1]
        write = self.b_w_number()[2]
        if black == 0:
            terminate = True
            self.value = 1
        if write == 0:
            terminate = True
            self.value = -1
        if space == 0:
            terminate = True
            if black > write:
                self.value = -1
            elif write > black:
                self.value = 1
            else:
                self.value = 0
        return terminate

    def win_or_lose(self):
        black = self.b_w_number()[0]
        write = self.b_w_number()[2]
        if black > write:
            return -1
        elif black < write:
            return 1
        else:
            return 0


def ucb1(node, c, all_visit_number):  # 解决n=0的问题
    i = 0
    max_ucb1 = -9999999
    max_pos = 0

    for a in node.child_list:
        if a.visit_number != 0:
            ave_value = a.value / a.visit_number
            if node.color == -1:
                ucb1_value = c * sqrt(2 * log(all_visit_number) / a.visit_number) + ave_value
            else:
                ucb1_value = -(c * sqrt(2 * log(all_visit_number) / a.visit_number) + ave_value)
        else:
            ucb1_value = 10000
        if ucb1_value > max_ucb1:
            max_pos = i
            max_ucb1 = ucb1_value
        i += 1

    return node.child_list[max_pos]


def valid_location(node):  # 返回node的下一步所有可能落点，即所有的孩子
    valid_node = []
    possible_node = Node(parent_node=node, checker_board=node.checker_board, color=-node.color)
    possible_coordinates = []
    if possible_node.color == -1:
        we_color = -1
        en_color = 1
    else:
        we_color = 1
        en_color = -1
    for i in range(0, 8):
        for j in range(0, 8):
            global_valid = False
            change_coordinate = []
            if possible_node.checker_board[i][j] == 0:  # 对8*8的棋盘进行遍历，若其为0，则开始以(i,j)为中心进行落点的搜索
                for k in range(0, j - 1):  # 检查水平向左方向上的所有可能的落点
                    if possible_node.checker_board[i][k] == we_color:
                        valid = True
                        for l in range(k + 1, j):
                            if possible_node.checker_board[i][l] != en_color:
                                valid = False
                        if valid:
                            global_valid = True
                            for l in range(k + 1, j):
                                change_coordinate.append([i, l])
                for k in range(j + 2, 8):  # 水平向右
                    if possible_node.checker_board[i][k] == we_color:
                        valid = True
                        for l in range(j + 1, k):
                            if possible_node.checker_board[i][l] != en_color:
                                valid = False
                        if valid:
                            global_valid = True
                            for l in range(j + 1, k):
                                change_coordinate.append([i, l])
                for k in range(0, i - 1):  # 竖直向上
                    if possible_node.checker_board[k][j] == we_color:
                        valid = True
                        for l in range(k + 1, i):
                            if possible_node.checker_board[l][j] != en_color:
                                valid = False
                        if valid:
                            global_valid = True
                            for l in range(k + 1, i):
                                change_coordinate.append([l, j])
                for k in range(i + 2, 8):  # 竖直向下
                    if possible_node.checker_board[k][j] == we_color:
                        valid = True
                        for l in range(i + 1, k):
                            if possible_node.checker_board[l][j] != en_color:
                                valid = False
                        if valid:
                            global_valid = True
                            for l in range(i + 1, k):
                                change_coordinate.append([l, j])
                for k in range(2, min(i, j) + 1):  # 西北方向
                    if possible_node.checker_board[i - k][j - k] == we_color:
                        valid = True
                        for l in range(1, k):
                            if possible_node.checker_board[i - l][j - l] != en_color:
                                valid = False
                        if valid:
                            global_valid = True
                            for l in range(1, k):
                                change_coordinate.append([i - l, j - l])
                for k in range(2, min(i, 7 - j) + 1):  # 东北方向
                    if possible_node.checker_board[i - k][j + k] == we_color:
                        valid = True
                        for l in range(1, k):
                            if possible_node.checker_board[i - l][j + l] != en_color:
                                valid = False
                        if valid:
                            global_valid = True
                            for l in range(1, k):
                                change_coordinate.append([i - l, j + l])
                for k in range(2, min(7 - i, 7 - j) + 1):  # 东南方向
                    if possible_node.checker_board[i + k][j + k] == we_color:
                        valid = True
                        for l in range(1, k):
                            if possible_node.checker_board[i + l][j + l] != en_color:
                                valid = False
                        if valid:
                            global_valid = True
                            for l in range(1, k):
                                change_coordinate.append([i + l, j + l])
                for k in range(2, min(7 - i, j) + 1):  # 西南方向
                    if possible_node.checker_board[i + k][j - k] == we_color:
                        valid = True
                        for l in range(1, k):
                            if possible_node.checker_board[i + l][j - l] != en_color:
                                valid = False
                        if valid:
                            global_valid = True
                            for l in range(1, k):
                                change_coordinate.append([i + l, j - l])
                if global_valid:
                    possible_coordinates.append([i, j])
                    child_node = Node(parent_node=node, checker_board=copy.deepcopy(node.checker_board),
                                      color=-node.color)
                    child_node.checker_board[i][j] = we_color
                    for b in change_coordinate:
                        child_node.checker_board[b[0], b[1]] = we_color
                    valid_node.append(child_node)
    return [valid_node, possible_coordinates]


def selection(node, all_visit_number):
    current_node = node
    while not current_node.is_terminate():
        if current_node.child_list:
            current_node = ucb1(current_node, 2, all_visit_number)
        else:
            break
    return current_node


def expansion(node):
    a = valid_location(node)
    flag = True
    if a[0]:
        node.child_list = a[0]
    else:
        flag = False
        child_node = Node(parent_node=node, checker_board=node.checker_board, color=-node.color)
        node.child_list = []
        node.child_list.append(child_node)
    node.unfolding = True
    return flag


def simulation(node, all_visit_number):
    current_node = node
    i = 0
    flag = True
    while not current_node.is_terminate():
        if i < 64:
            if not current_node.unfolding:
                expansion(current_node)
                next_node = current_node.child_list[random.randrange(0, len(current_node.child_list))]
                current_node = next_node
                i += 1
        else:
            flag = False
            break
    back_propagation(current_node, node, all_visit_number)
    return flag


def back_propagation(value_node, start_node, all_visit_number):  # 为何回溯更新不是从终局结点开始，而是从select_end开始
    value_node.value = value_node.win_or_lose()
    current_node = start_node
    while current_node is not None:
        current_node.visit_number = current_node.visit_number + 1
        all_visit_number += 1
        current_node.value += value_node.value
        parent_node = current_node.parent_node
        current_node = parent_node


def ini_root():
    ini_checker = np.zeros([8, 8], dtype=int)
    ini_checker[3][3] = 1
    ini_checker[4][4] = 1
    ini_checker[3][4] = -1
    ini_checker[4][3] = -1
    print(ini_checker)
    root = Node(None, ini_checker, 1)
    return root


def choose_better(node, all_visit_number):
    select_end = node
    for i in range(0, 200):
        select_end = selection(node, all_visit_number)
        simulation(select_end, all_visit_number)
    return ucb1(node, 2, all_visit_number)


def main():
    start_time = datetime.datetime.now()
    root = ini_root()
    all_visit_number = 1
    current_node = root
    next_node = None
    while not current_node.is_terminate():
        next_node = choose_better(current_node, all_visit_number)
        current_node = next_node
        print(current_node.checker_board)
        if current_node.child_list:
            if len(current_node.child_list) == 1:
                parent_node = current_node.parent_node
                grandfather_node = parent_node.parent_node
                if np.allclose(parent_node.checker_board, grandfather_node.checker_board):
                    print("双方均已无子可落")
                    break
    print(current_node.win_or_lose())
    end_time = datetime.datetime.now()
    print(f"开始时间：{start_time}")
    print(f"结束时间：{end_time}")


def human_ai():
    root = ini_root()
    current_node = root
    all_visit_number = 1
    i = 0
    next_node = None
    while not current_node.is_terminate():
        if (i % 2 == 0):
            next_node = choose_better(current_node, all_visit_number)
            current_node = next_node
            print(next_node.checker_board)
        else:
            a = valid_location(current_node)
            flag = expansion(current_node)
            if flag:
                print(a[1])
                choose_number = int(input("请输入要落子位置的序号"))
                next_node = current_node.child_list[choose_number - 1]
            else:
                parent_node = current_node.parent_node
                grandfather_node = parent_node.parent.node
                if current_node.checker_board != grandfather_node.checker_board:
                    print("该轮次您无子可落")
                else:
                    print(f"双方均已无子可落，游戏结果为:{current_node.win_or_lose()}")

            current_node = next_node
        i += 1
    print(current_node.win_or_lose())


choose = int(input("你是想和机器对战（0）还是让机器自己对战（1）？"))
if choose == 0:
    human_ai()
else:
    main()
