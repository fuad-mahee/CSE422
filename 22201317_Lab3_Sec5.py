#Task1
import random
class TreeNode:
    def __init__(self, depth):
        self.depth = depth
        self.children = []
        self.value = None
def build_game_tree(node, max_depth, branch_fact):
    if node.depth == max_depth:
        node.value = random.choice([-1, 1])
    else:
        for _ in range(branch_fact):
            child = TreeNode(node.depth + 1)
            node.children.append(child)
            build_game_tree(child, max_depth, branch_fact)
def alpha_beta_pruning(node, alpha, beta, max_player):
    if node.value is not None:
        return node.value
    if max_player:
        return maximize(node, alpha, beta)
    else:
        return minimize(node, alpha, beta)
def maximize(node, alpha, beta):
    max_value = float('-inf')
    for child in node.children:
        val = alpha_beta_pruning(child, alpha, beta, False)
        max_value = max(max_value, val)
        alpha = max(alpha, val)
        if beta <= alpha:
            break  
    return max_value
def minimize(node, alpha, beta):
    min_value = float('inf')
    for child in node.children:
        val = alpha_beta_pruning(child, alpha, beta, True)
        min_value = min(min_value, val)
        beta = min(beta, val)
        if beta <= alpha:
            break  
    return min_value
def simulate_game(start_player):
    total_rounds = 3
    rounds_played = 0
    round_winners = []
    scores = { -1: 0, 1: 0 }  
    curr_player = start_player
    for i in range(total_rounds):
        root = TreeNode(0)
        root.values=start_player
        build_game_tree(root, 5, 2)
        result = alpha_beta_pruning(root, float('-inf'), float('inf'), True)
        scores[result] += 1
        if result == -1:
            winner = "Scorpion"
        else:
            winner = "Sub-Zero"
        round_winners.append(winner)
        curr_player = 1 - curr_player
        rounds_played += 1
    if scores[-1] > scores[1]:
        game_winner = "Scorpion"
    else:
        game_winner = "Sub-Zero"
    with open("output.txt", "w") as f:
        f.write(f"Game Winner: {game_winner}\n")
        f.write(f"Total Rounds Played: {rounds_played}\n")
        for idx, winner in enumerate(round_winners, 1):
            f.write(f"Winner of Round {idx}: {winner}\n")
with open("input.txt", "r") as f:
    start = int(f.read().strip())
simulate_game(start)
#Task2
class TreeNode:
    def __init__(self, depth):
        self.depth = depth
        self.children = []
        self.value = None
def build_game_tree(node, max_depth, branch_factor, leaf_values, leaf_index):
    if node.depth == max_depth:
        node.value = leaf_values[leaf_index[0]]
        leaf_index[0] += 1
    else:
        for _ in range(branch_factor):
            child = TreeNode(node.depth + 1)
            node.children.append(child)
            build_game_tree(child, max_depth, branch_factor, leaf_values, leaf_index)
def alpha_beta_pruning(node, alpha, beta, max_player):
    if node.value is not None:
        return node.value
    if max_player:
        return maximize(node, alpha, beta)
    else:
        return minimize(node, alpha, beta)
def maximize(node, alpha, beta):
    max_value = float('-inf')
    for child in node.children:
        val = alpha_beta_pruning(child, alpha, beta, False)
        max_value = max(max_value, val)
        alpha = max(alpha, val)
        if beta <= alpha:
            break  
    return max_value
def minimize(node, alpha, beta):
    min_value = float('inf')
    for child in node.children:
        val = alpha_beta_pruning(child, alpha, beta, True)
        min_value = min(min_value, val)
        beta = min(beta, val)
        if beta <= alpha:
            break  
    return min_value
def alpha_beta_pruning_dark_magic(node, alpha, beta):
    if node.value is not None:
        return node.value, []
    max_value = float('-inf')
    best_path = []
    for child in node.children:
        val, path = alpha_beta_pruning_dark_magic(child, alpha, beta)
        if val > max_value:
            max_value = val
            best_path = path
            direction = 'left' if node.children.index(child) == 0 else 'right'
        alpha = max(alpha, val)
        if beta <= alpha:
            break
    return max_value, [direction] + best_path
def pacman_game(cost):
    leaf_values = [3, 6, 2, 3, 7, 1, 2, 0]
    max_depth = 3
    branch_factor = 2
    root_normal = TreeNode(0)
    leaf_index = [0]
    build_game_tree(root_normal, max_depth, branch_factor, leaf_values, leaf_index)
    normal_value = alpha_beta_pruning(root_normal, float('-inf'), float('inf'), True)
    dark_magic_value, path = alpha_beta_pruning_dark_magic(root_normal, float('-inf'), float('inf'))
    dark_magic_value -= cost 
    with open("output.txt", "w") as output_file:
        if normal_value >= dark_magic_value:
            output_file.write(f"The minimax value is {normal_value}. Pacman does not use dark magic\n")
        else:
            direction = path[0] if path else 'left'
            output_file.write(f"The new minimax value is {dark_magic_value}. Pacman goes {direction} and uses dark magic\n")
with open("input.txt", "r") as f:
    cost = int(f.read().strip())
pacman_game(cost)