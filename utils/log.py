"""Utility Functions for Logging into Markdown Files."""
from utils.code import wrap_code


def write_prompt(
    fw_log, 
    prompt: str, 
    toolbox_preview: str, 
    index: int | str, 
    solution_first: bool = True,
):
    curr_ex_start = prompt.rindex("**Question**")
    sub_prompt = prompt[curr_ex_start: ].rstrip()
    if solution_first:
        keyword_prompt = "**Solution**"
    else:
        keyword_prompt = "**Tools**"
    sub_prompt = sub_prompt.rstrip(keyword_prompt).rstrip()

    text_chunks = [f"## Example {index}"]
    if toolbox_preview != "":
        text_chunks.extend(["**Toolbox**", toolbox_preview, ""])
    text_chunks.append(sub_prompt.replace('\n**', '\n\n**'))
    
    fw_log.write('\n'.join(text_chunks) + '\n\n')


def write_exec_result(
    fw_log, 
    exec_dict: dict[str, bool | str | list[str]],
    index: int = 0,
):
    fw_log.write('\n'.join([
        f"**{index}-th Execution Result**",
        f"- Is Execution Success: {exec_dict['is_success']}",
        f"- Model Output:",
        "```", 
        f"{exec_dict['exec_output']}"
        "\n```",
        f"- Model Answer: {exec_dict['model_answers']}",
        f"- Annotated Answer(s): {exec_dict['answer']}",
        f"- Is Answer Correct: {exec_dict['is_correct']}",     
    ]) + '\n\n')



def write_solution_and_tools(fw_log, res: dict, toolbox: dict, update_toolbox: bool, index: int = 0):
    fw_log.write('\n'.join([f"{index}-th **Solution**", res["solution"]]) + '\n\n')

    tool_str_list, action_str_list = [], []
    for tool_dict in res["function"]:
        tool_str_list.append(wrap_code(tool_dict["function"]))

        if tool_dict["type"] == "import":
            action = "IMPORT"
            tool_repr = tool_dict["signature"]
        elif tool_dict["name"] in toolbox:
            action = "EDIT"
            tool_repr = tool_dict["name"]
        else:
            action = "ADD"
            tool_repr = tool_dict["signature"]
        action_str_list.append('```\n' + f"{action} | {tool_repr}" + '\n```')

        if update_toolbox:
            toolbox[tool_dict["name"]] = tool_dict
            
    fw_log.write('\n'.join([f"**{index}-th Tools**"] + tool_str_list) + '\n\n')
    fw_log.write('\n'.join([f"**{index}-th Actions**"] + action_str_list) + '\n\n')



def auto_decide_path(
    args, fields: list[str] = ["log", "library"]
) -> str:
    """Automatically determine the log path."""
    import os

    # results
    results_dir = os.path.join(
        f"output_{args.model_name}", args.task_name, "results",
        f"{args.max_num_examples}ex", args.suffix,
    )
    os.makedirs(results_dir, exist_ok=True)
    log_dir = os.path.join(
        f"output_{args.model_name}", args.task_name, "log",
        f"{args.max_num_examples}ex", args.suffix,
    )
    os.makedirs(log_dir, exist_ok=True)

    if args.run_index is None:
        log_path_list = [
            lp for lp in os.listdir(log_dir)
            if (lp.startswith("run") and lp.endswith(".md"))
        ]
        if len(log_path_list) > 0:
            run_index_list = [lp[len("run"): -len(".md")] for lp in log_path_list]
            run_index_list = [int(ri) for ri in run_index_list]
            args.run_index = max(run_index_list) + 1
        else:
            args.run_index = 0
    updated_name = f"run{args.run_index}.json"
    args.output_results_path = os.path.join(results_dir, updated_name)
    print(f"Output Results Path: {args.output_results_path}")

    # logging
    if "log" in fields:
        log_name = f"run{args.run_index}.md"
        args.output_log_path = os.path.join(log_dir, log_name)
        print(f"Log Path: {args.output_log_path}")

    # library
    if "library" in fields:
        library_dir = os.path.join(
            f"output_{args.model_name}", args.task_name, "library",
            f"{args.max_num_examples}ex", args.suffix,
        )
        os.makedirs(library_dir, exist_ok=True)
        library_name = f"run{args.run_index}.json"
        args.output_library_path = os.path.join(library_dir, library_name)
        print(f"Output Toolbox Path: {args.output_library_path}")

    return args
