import math

def evaluate(path):
    total_cost = sum(cost for _, cost in path)
    return -total_cost  # maximize negative cost = minimize distance


def alpha_beta(graph, node, goal, depth, alpha, beta, maximizing, path):

    if depth == 0 or node == goal:
        return evaluate(path), path

    if maximizing:
        max_eval = -math.inf
        best_path = []

        for neighbor, cost in graph.get(node, []):
            new_path = path + [(neighbor, cost)]

            eval_score, _ = alpha_beta(
                graph, neighbor, goal, depth - 1,
                alpha, beta, False, new_path
            )

            if eval_score > max_eval:
                max_eval = eval_score
                best_path = new_path

            alpha = max(alpha, eval_score)

            if beta <= alpha:
                break  # PRUNE

        return max_eval, best_path

    else:
        min_eval = math.inf
        best_path = []

        for neighbor, cost in graph.get(node, []):
            new_path = path + [(neighbor, cost)]

            eval_score, _ = alpha_beta(
                graph, neighbor, goal, depth - 1,
                alpha, beta, True, new_path
            )

            if eval_score < min_eval:
                min_eval = eval_score
                best_path = new_path

            beta = min(beta, eval_score)

            if beta <= alpha:
                break  # PRUNE

        return min_eval, best_path