import copy
import random
import time
import math
# Node Class
class Node:

    # Constructor
    def __init__(self, board, player):
        self.board = board
        self.player = player
        self.children = []
        self.best_child = None
        self.score = 0

    def __str__(self):
        result = self.board.__str__()
        result += "\nThis node has " + str(len(self.children)) + " children"
        result += "\nThis node has a score of " + str(self.score) + "\nNext Turn will be player by " + self.player
        return result

    def index_of_best_child(self):
        if self.best_child == None:
            return -1
        for i in range(len(self.children)):
            if self.children[i] == self.best_child:
                return i
        return -1
    # adds a child
    def add_child(self, node):
        self.children.append(node)

    # prints board
    def print_board(self):
        print(" 012")
        for row in range(len(self.board)):
            row_str = str(row)
            for col in range(len(self.board[0])):
                row_str += self.board[row][col]
            print(row_str)
        print()

    # check if either player has won or tied, returns a tuple of the player who won, and a boolean
    # representing if the game is done
    def check_win(self):
        count = 0
        # horizontal victory and vertical victory
        for i in range(len(self.board)):
            # horizontal victory
            if self.board[i][0] != '-' and (self.board[i][0] == self.board[i][1] and self.board[i][1] \
                    == self.board[i][2]):
                return self.board[i][0], True
            # vertical victory
            if self.board[0][i] != '-' and (self.board[0][i] == self.board[1][i] and self.board[1][i] \
                    == self.board[2][i]):
                return self.board[0][i], True
            # diagonal victories
            if self.board[0][0] != '-' and (self.board[0][0] == self.board[1][1] == self.board[2][2]):
                return self.board[0][0], True
            if self.board[2][0] != '-' and (self.board[2][0] == self.board[1][1] == self.board[0][2]):
                return self.board[2][0], True
            for j in range(len(self.board[0])):
                if self.board[i][j] != '-':
                    count += 1
        # tie condition
        if count == 9:
            return None, True
        # game not over
        return None, False

    def set_best_child(self):
        game_result = self.check_win()
        # base case
        if game_result[1]:
            if game_result[0] == "O":
                self.score = 10
                return
            elif game_result[0] == "X":
                self.score = -10
                return
            else:
                self.score = 0
                return
                #print("tie set")
        # run recursive function through all children before second part for non end game nodes
        for child in self.children:
            child.set_best_child()

        if self.player == "O":
            maxValue = -math.inf
            best_child = None
            for child in self.children:
                if child.score > maxValue:
                    maxValue = child.score
                    best_child = child
            self.score = maxValue
            self.best_child = best_child

        elif self.player == "X":
            self.score = math.inf
            minValue = self.score
            best_child = None
            for child in self.children:
                if child.score < minValue:
                    minValue = child.score
                    best_child = child
            self.score = minValue
            self.best_child = best_child

    def boardEqual(self, board):
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] != board[i][j]:
                    return False
        return True

    def search_nodes(self, board):
        nodeList = []
        if self.boardEqual(board):
            nodeList.append(self)
        for child in self.children:
            child.search_nodes(board)
        if len(nodeList) != 0:
            return nodeList[0]
        return None

# Tree Class
class Tree:
    def __init__(self, root):
        self.root = root
        self.build_tree(self.root)
        self.root.set_best_child()


    def build_tree(self, node):
        if node.check_win()[1]:
            return
        for row in range(len(node.board)):
            for col in range(len(node.board[0])):
                if node.board[row][col] == '-':
                    new_board = copy.deepcopy(node.board)
                    new_board[row][col] = node.player
                    next_player = ""
                    if node.player == "X":
                        next_player = "O"
                    if node.player == "O":
                        next_player = "X"
                    new_node = Node(new_board, next_player)
                    self.build_tree(new_node)
                    node.add_child(new_node)


def playGame():
    print("Welcome to the Tic Tac Toe AI Game, where you can play Tic Tac Toe against an unbeatable AI. "
        "You will be player 'X' and the computer with be player 'O'.")
    time.sleep(1)
    empty_board = []
    for i in range(3):
        empty_board.append([])
        for j in range(3):
            empty_board[i].append("-")
    turn = random.randint(0,1)
    root = None
    if turn == 0:
        print('\nYou will be Going First\nPlease Wait While The AI Loads\n')
        root = Node(empty_board, "X")
    elif turn == 1:
        print('\nYou will be Going Second\nPlease Wait while the AI Loads\n')
        root = Node(empty_board, "O")
    tree = Tree(root)
    root.print_board()
    current = root
    winner = None
    gameOver = False
    if turn == 1:
        root.best_child.print_board()
        current = root.best_child
    while True:
        while True:
            row = int(input("What row would you like to place your X: "))
            col = int(input("What col would you like to place your X: "))
            if row < 0 or row > 2 or col < 0 or col > 2:
                print("Invalid Row or Column selected. Please Enter Again")
            else:
                break
        for child in current.children:
            if child.board[row][col] == current.player:
                current = child
                break
        current.print_board()
        winner, gameOver = current.check_win()
        if gameOver:
            break
        print("\nAI's Turn")
        time.sleep(1)
        current = current.best_child
        current.print_board()
        winner, gameOver = current.check_win()
        if gameOver:
            break
    if winner == "O":
        print("\nComputer Won! Better Luck Next Time!")
    elif winner == "X":
        print("\nYou Won! Congratulation! This should not be Possible")
    else:
        print("\nYou Tied")




playGame()

'''empty_board = []
for i in range(3):
    empty_board.append([])
    for j in range(3):
        empty_board[i].append("-")
root = Node(empty_board, 'X')

tree = Tree(root)

x_win = [['X', 'X', 'X'],
         ['O', 'O', 'O'],
         ['-', '-', '-']]
# lastNode = tree.root.search_nodes(x_win)
# print(root.best_child.best_child.best_child.best_child.best_child.best_child)
#print(root.children[0].children[2].children[0].children[1].children[0])
#print(root.children[0].children[2].children[0].children[1])
#print(root.children[0].children[2].children[0])
#print(root.children[0].children[2])
#print(root.children[0])
#for child in root.children:
 #   print(child)'''















