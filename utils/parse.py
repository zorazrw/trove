"""Parse Model Responses."""

from utils import parse_tools

def parse_model_response(
    response: str, solution_first: bool = True,
) -> dict[str, str]:
    # split 'tools' and 'solution' sections
    if solution_first:
        if not response.startswith("**Solution**"):
            response = "**Solution**\n" + response
    else:  # tool_first
        if not response.startswith("**Tools**"):
            response = "**Tools**\n" + response
    response_lines = response.split("\n")  # list[str]

    if solution_first:
        solution_index, tools_index = 0, len(response_lines)
    else:
        tools_index, solution_first = 0, len(response_lines)
    for i, l in enumerate(response_lines):
        if l.startswith("**Tools**"):
            tools_index = i
        elif l.startswith("**Solution**"):
            solution_index = i

    if tools_index < solution_index:
        tool_resp = '\n'.join(response_lines[tools_index+1: solution_index])
        solution_resp = '\n'.join(response_lines[solution_index+1:])
    else:
        tool_resp = '\n'.join(response_lines[tools_index+1:])
        solution_resp = '\n'.join(
            response_lines[solution_index+1: tools_index]
        )

    # 'solution' post-processing
    solution_resp = solution_resp.strip()  # (text) + ```python\n(code)```

    # 'tools' post-processing
    tool_dict_list = parse_tools(tool_resp.strip())  # list[dict]

    return {
        "response": response,        # str
        "solution": solution_resp,   # str
        "function": tool_dict_list,     # list[dict]
    }


def extract_llama_response(output_text: str, input_text: str) -> str:
    output_text = output_text[len(input_text):].strip()
    if "**Question" in output_text:
        end_index = output_text.index("**Question")
        output_text = output_text[:end_index].strip()
    if "## Example" in output_text:
        end_index = output_text.index("## Example")
        output_text = output_text[:end_index].strip()
    return output_text


def clean_solution(solution: str) -> str:
    from utils.code import is_import_line
    sol_lines = solution.split('\n')
    sol_lines = [sl for sl in sol_lines if not is_import_line(sl)]
    return '\n'.join(sol_lines)
