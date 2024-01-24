"""Answer Evaluation Utilities."""

import re
from utils.parse import clean_solution

# %% Lexical Evaluation

import string
from collections import Counter

def normalize_text(text: str) -> str:
    """Normalize text with lowercasing, removing articles, and punctuation."""

    def remove_articles(text: str) -> str:
        return re.sub(r"\b(a|an|the)\b", " ", text)

    def white_space_fix(text: str) -> str:
        return " ".join(text.split())

    def remove_punc(text: str) -> str:
        exclude = set(string.punctuation)
        return "".join(ch for ch in text if ch not in exclude)

    def lower(text: str) -> str:
        return text.lower()

    return white_space_fix(remove_articles(lower(text)))



def calc_unigram_f1(text: str, answers: list[str], field: str = "f1") -> float:
    """Calculate unigram f1 score between the text and reference answers."""
    norm_pred = normalize_text(text)
    norm_answers = [normalize_text(ans) for ans in answers]
    common_tokens = [
        Counter(norm_pred) & Counter(norm_ans) for norm_ans in norm_answers
    ]
    num_same = [sum(common.values()) for common in common_tokens]

    score_list = []
    for i, num in enumerate(num_same):
        if num == 0:
            score_list.append(0.0)
        else:
            p = 1.0 * num / len(norm_pred)
            r = 1.0 * num / len(norm_answers[i])
            f1 = 2 * p * r / (p + r)
            if field == "precision":
                score_list.append(p)
            elif field == "recall":
                score_list.append(r)
            elif field == "f1":
                score_list.append(f1)
            else:
                raise ValueError(f"Unknown field: {field}")
    return max(score_list)


# %% End Answer Evaluation

def is_exec_correct_number(
    is_success: bool,
    model_output: str, 
    answer: float,
    return_answers: bool = False, 
) -> bool:
    """Check if the execution result exactly matches the answer value."""
    if not is_success:
        return (False, []) if return_answers else False
    model_answers = re.findall(r'-?\d+\.?\d*', model_output)
    model_answers = [float(ans) for ans in model_answers]
    if len(model_answers) == 0:
        return (False, model_answers) if return_answers else False
    model_answer = model_answers[0]
    any_correct = round(model_answer,2) == round(answer,2)
    return (any_correct, model_answers) if return_answers else any_correct


def is_exec_correct_text(
    is_success: bool,
    model_output: str, 
    answer: str | list[str],
    return_answers: bool = False, 
) -> bool | tuple[bool, list[str]]:
    """Check if the execution result exactly matches the answer value."""
    if not is_success:
        return (False, []) if return_answers else False
    if isinstance(answer, str):
        answer = [answer]
    answer = [a.strip().lower() for a in answer]
    model_pred = model_output.strip().lower().replace('–', '-')  # for wtq
    any_correct = any([(ans == model_pred) for ans in answer])
    return (any_correct, [model_pred]) if return_answers else any_correct


def is_exec_correct_bool(
    is_success: bool,
    model_output: str,
    answer: str | dict | list[str],
    return_answers: bool = False,
) -> bool | tuple[bool, list[str]]:
    """Align true/false boolean execution results with yes/no annotations."""
    if not is_success:
        return (False, []) if return_answers else False
    model_output = model_output.strip().lower()
    if model_output == "true":
        if any([(a.lower().strip() == "yes") for a in answer]):
            return (True, [model_output]) if return_answers else True
    if model_output == "false":
        if any([(a.lower().strip() == "no") for a in answer]):
            return (True, [model_output]) if return_answers else True
    return (False, [model_output]) if return_answers else False


def is_exec_correct(
    is_success: bool,
    model_output: str, 
    answer: list[any],
    return_answers: bool = False, 
) -> bool | tuple[bool, list[str]]:
    """Check if the execution result exactly matches the answer value."""
    if not is_success:
        return (False, []) if return_answers else False
    ans_model_answers = [model_output]
    if isinstance(answer, str):   # for hitab
        answer = [answer]
    if isinstance(answer, dict):  # for gqa (is this correct??)
        answer = list(answer.values())
    for ans in answer:
        if isinstance(ans, float):
            ans_any_correct, ans_model_answers = is_exec_correct_number(is_success, model_output, ans, return_answers=True)
            if ans_any_correct:
                return (ans_any_correct, ans_model_answers) if return_answers else ans_any_correct
        else:
            ans = str(ans)
            ans_any_correct, ans_model_answers = is_exec_correct_text(is_success, model_output, ans, return_answers=True)
            if ans_any_correct:
                return (ans_any_correct, ans_model_answers) if return_answers else ans_any_correct
    return (False, ans_model_answers) if return_answers else False

    

EVAL_FUNC = {
    "math": is_exec_correct_number,
    "tabmwp": is_exec_correct_number,
    "wtq": is_exec_correct_text,
    "hitab": is_exec_correct,
    "gqa": is_exec_correct,
}


# %% Dataset Prediction Evaluation

import ast 

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


from utils.code import *

def calc_correctness(results_list: list[dict | list[dict]], epsilon: float = 1e-10) -> float:
    """Report the overall correctness of predictions."""
    correct_list = []
    for res in results_list:
        if isinstance(res, list):
            if len(res) > 1:
                print("Warning: multiple predictions for one example. Using the first one.")
            res = res[0]
        if ("response" in res) and isinstance(res["response"], dict):
            res = res["response"]
        
        correct_list.append(res["is_correct"])
    return sum(correct_list) / (len(correct_list) + epsilon)



def calc_num_actions(results_list: list[dict | list[dict]]) -> float:
    """Report the number of actions, by AST depth."""
    depth_list = []
    for res in results_list:
        if isinstance(res, list):
            if len(res) > 1:
                print("Warning: multiple predictions for one example. Using the first one.")
            res = res[0]
        if ("response" in res) and isinstance(res["response"], dict):
            res = res["response"]
        
        try:
            depth = get_ast_depth(unwrap_code(clean_solution(res["solution"])))
            depth_list.append(depth)
        except:
            continue
    return sum(depth_list) / len(depth_list)


def count_toolbox(results_list: list[dict | list[dict]], print_toolbox: bool = False) -> dict:
    """Count the total number of unique tools."""
    funcset, func_dict = set(), {}
    nameset, name_dict = set(), {}
    for i,res in enumerate(results_list):
        if isinstance(res, list):
            if len(res) > 1:
                print("Warning: multiple predictions for one example. Using the first one.")
            res = res[0]
        if ("response" in res) and isinstance(res["response"], dict):
            res = res["response"]
        if not res["is_success"]: continue
        
        for tool_dict in res["function"]:
            # name wise
            if tool_dict["name"].startswith("toolbox."):
                tool_name = tool_dict["name"][8:].strip()
            else:
                tool_name = tool_dict["name"]
            clean_ressol = clean_solution(res["solution"])
            if ('.' in tool_name) and tool_name.split('.')[-1] not in clean_ressol:
                continue
            if ('.' not in tool_name) and (tool_name not in clean_ressol): continue
            nameset.add(tool_name)
            if tool_name not in name_dict: name_dict[tool_name] = []
            name_dict[tool_name].append(i)
            # function wise
            funcset.add(tool_dict["function"])
            if tool_dict["function"] not in func_dict: func_dict[tool_dict["function"]] = []
            func_dict[tool_dict["function"]].append(i)
    if print_toolbox:
        name_and_count = [(name,len(indices)) for name,indices in name_dict.items()]
        name_and_count = sorted(name_and_count, key=lambda x:-x[1])
        for name, count in name_and_count:
            print(name)
        for name, count in name_and_count:
            print(count)
    return len(funcset), len(nameset)
        

def report_metrics(results_list, verbose: bool = False):
    avg_correct = calc_correctness(results_list)
    print(f"Average Correct: {avg_correct:.4f}")
    avg_num_act = calc_num_actions(results_list)
    print(f"Average Number of Actions: {avg_num_act:.2f}")
    toolbox_size = count_toolbox(results_list, print_toolbox=verbose)
    print(f"Toolbox Size: {toolbox_size}")


# %% Evaluation Pipeline

import argparse
from utils.io import load_json_file

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--results_path", type=str, required=True)
    parser.add_argument("--max_num_examples", type=int, default=None)
    parser.add_argument("--indices", type=int, nargs='+', default=None)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    print("Verbose Mode: ", args.verbose)
    
    results_list = load_json_file(args.results_path)
    if "best" in results_list[0]:
        results_list = [res["best"] for res in results_list]
    if isinstance(results_list[0], list):
        results_list = [res[0] for res in results_list]

    if args.max_num_examples is not None:
        results_list = results_list[: args.max_num_examples]
    report_metrics(results_list, args.verbose)
    print('=' * 20, '\n')
