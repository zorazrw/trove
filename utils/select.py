"""Selection Heuristics for Multuple Solution/Tools Candidates."""

import ast 
from utils.code import unwrap_code

def get_ast_depth(code: str) -> int:
    root = ast.parse(code)
    total_depth = 0

    def depth_ast(root): 
        return 1 + max((depth_ast(child) for child in ast.iter_child_nodes(root)), default = 0)
    
    for node in root.body:
        if isinstance(node, ast.FunctionDef):
            continue
        if isinstance(node, ast.Assign):
            if isinstance(node.value, ast.Constant):
                continue
            elif len(node.targets) == 1 and isinstance(node.targets[0], ast.Name) and node.targets[0].id == 'df':
                continue
        depth = depth_ast(node)
        total_depth += depth
    return total_depth


def select_best_solution(response_list: list[dict], is_test: bool = True) -> int:
    """Select the best solution among multiple predictions.
    - is_correct/is_success: prefer correct responses over wrong ones
    - answer agreement: prefer majority answer
    - trajectory length: prefer shorted trajectory
    """
    def get_true_responses(response_list: list[dict], key: str) -> list[int]:
        return [i for i,r in enumerate(response_list) if r[key]]

    if not is_test:
        correct_indices = get_true_responses(response_list, key="is_correct")
        if len(correct_indices) == 0:
            correct_indices = get_true_responses(response_list, key="is_success")
    else:
        correct_indices = get_true_responses(response_list, key="is_success")
    if len(correct_indices) == 0: return 0

    # find majority answer
    model_answers_dict = {}
    for sidx in correct_indices:
        dres = response_list[sidx]
        for ans in dres["model_answers"]:
            if ans not in model_answers_dict:
                model_answers_dict[ans] = []
            model_answers_dict[ans].append(sidx)
    if len(model_answers_dict) == 0:
        return correct_indices[0]
    majority_answer, majority_count = "", 0
    for answer, indices in model_answers_dict.items():
        if len(indices) > majority_count:
            majority_answer = answer
            majority_count = len(indices)
    majority_response_list = [
        (sidx, response_list[sidx]) 
        for sidx in model_answers_dict[majority_answer]
    ]
    
    # find the response with the shortest trajectory
    length_list = []
    for _, dres in majority_response_list:
        try:
            dres_length = get_ast_depth(unwrap_code(dres["solution"]))
        except:
            dres_length = 100
        length_list.append(dres_length)
    index = length_list.index(min(length_list))
    return majority_response_list[index][0]
