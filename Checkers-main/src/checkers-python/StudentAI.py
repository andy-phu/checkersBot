import copy
import math
from random import randint
import random
from BoardClasses import Move
from BoardClasses import Board
import pdb
import logging
logging.basicConfig(level=logging.DEBUG, filename='myapp.log', filemode='w',
                    format='%(name)s - %(levelname)s - %(message)s')


#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.
class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
        self.tree = Node(state = self.board, player_just_moved = self.color)
        
    def get_move(self,move):
        if len(move) != 0: 
            self.board.make_move(move, self.opponent[self.color])
        else:
            self.color = 1

        
        move = self.mcts_search(self.tree.state)
        self.board.make_move(move, self.color)

        return move



    def mcts_search(self, current_state):
        root_node = Node(state=current_state)

        for _ in range(1000):
            # test, move = self.move_king()
            # if test == True:
            #     return move
            # Selection
            leaf = self.select(root_node)

            # logging.info("leaf: %s", leaf)

            # Expansion
            child = self.expand(leaf)

            # Simulation
            result = self.simulate(child)

            #Backpropagation
            while child is not None:
                child.update(result)
                child = child.parent

        best_child = root_node.best_child() 
        logging.info("best_child: %s", best_child.move)
        return best_child.move
    
    def select(self, node):
        while node.children:
            # Calculate UCB1 values for all children
            max_value = float('-inf')
            selected_child = None
            for child in node.children:
                if child.visits == 0:
                    continue
                ucbvalue = (child.wins / child.visits) + 1.41 * math.sqrt(2 * math.log(node.visits) / child.visits)
                if ucbvalue > max_value:
                    max_value = ucbvalue
                    selected_child = child


            # Select the child node with the maximum UCB1 value
            
            node = selected_child

        # logging.info("selected leaf: %s", node)
        # logging.info("selected leaf: %s", node.children)
        return node


    def expand(self, node):
        if node.state.is_win("W") == self.color or node.state.is_win("B") == self.color:
            return node
        # temp_player = 1
        if node.parent == None or node.parent.player_just_moved == 2:
            temp_player = 1
        else:
            temp_player = 2
        # logging.info("temp player: %s", temp_player)
        # logging.info("temp player: %d going inside moves array: %s", temp_player, str(node.state.get_all_possible_moves(temp_player)))
        if not node.state.get_all_possible_moves(temp_player):
            # logging.info("node: %s", node)
            return node
        for moves in node.state.get_all_possible_moves(temp_player):
            for move in moves:  # Expand multiple untried moves
                new_state = copy.deepcopy(node.state)
                new_state.make_move(move, temp_player)  # Make the move in the new state
                new_node = Node(move = move, parent = node, state = new_state, player_just_moved = 2 if temp_player == 1 else 1)
                # logging.info("new child: %s", new_node)
                node.children.append(new_node)

        # logging.info("selected child: %s", node)
        answer = random.choice(node.children)
        # logging.info("random.choice(node.children): %s", answer)
        return answer



    def simulate(self, node):
        sim_state = copy.deepcopy(node.state)
        curr_player = node.player_just_moved

        while sim_state.is_win("W") == 0 and sim_state.is_win("B") == 0:
            possible_moves = [move for moves in sim_state.get_all_possible_moves(curr_player) for move in moves]

            if not possible_moves:
                break

            random_move = random.choice(possible_moves)

            sim_state.make_move(random_move, curr_player)
            curr_player = self.opponent[curr_player]

        if sim_state.is_win("W") == self.color or sim_state.is_win("B") == self.color:
            # logging.info("here")
            return 1
        # else:
        #     return 0
        score = self.curr_board_score(curr_player)
        if score > 0:
            # logging.info("here")
            return 1
        else:
            return 0
        

    def curr_board_score(self, curr_player):
        white_kings = 0
        black_kings = 0
        for c in range(self.col):
            for r in range(self.row):
                current_piece = self.board.board[c][r]
                if current_piece is not None:
                    if current_piece.get_color() == self.color:
                        if current_piece.is_king:
                            white_kings += 1
                    elif current_piece.get_color() == self.opponent[self.color]:
                        if current_piece.is_king:
                            black_kings += 1
        if curr_player == self.color:
            return self.board.black_count - self.board.white_count + (white_kings * 0.5 - black_kings * 0.5)
        else:
            return self.board.white_count - self.board.black_count + (black_kings * 0.5 - white_kings * 0.5)
        
    # def move_king(self):
    #     for c in range(self.col):
    #         for r in range(self.row):
    #             current_piece = self.board.board[c][r]
    #             if current_piece is not None:
    #                 if current_piece.get_color() == self.color:
    #                     if current_piece.is_king:
    #                         if c-1 >= 0 and r - 1 >= 0:
    #                             return True, [(c,r), (c - 1, r - 1)]
    #                         elif c + 1 <= self.col and r - 1 <= self.row:
    #                             return True, [(c,r), (c + 1, r + 1)]
    #     return False, []
        

class Node:
    def __init__(self, move=None, parent=None, state=None, player_just_moved=None):
        self.move = move
        self.parent = parent
        self.state = state
        self.children = []
        self.tried = []
        self.wins = 0
        self.visits = 0
        # self.untried_moves = [move for moves in state.get_all_possible_moves(player_just_moved) for move in moves]
        self.player_just_moved = player_just_moved
        

    def select_child(self):
        if not self.children:
            return None  

        ucb_values = []
        for child in self.children:
            if child.visits == 0:
                ucb_values.append(float('inf'))
            else:
                ucb_values.append(
                    (child.wins / child.visits) +
                    1.41 * math.sqrt(math.log(self.visits) / child.visits)
                )

        selected_index = ucb_values.index(max(ucb_values))

        return self.children[selected_index]


    def update(self, result):
        self.visits += 1 
        self.wins += result


    def best_child(self):
        most_visited = None
        max_visits = float('-inf')

        for child in self.children:
            if child.visits > max_visits:
                most_visited = child
                max_visits = child.visits

        return most_visited

  