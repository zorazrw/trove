"""Parsing Tools."""

# %% Basics
def extract_code_pieces(text: str) -> list[str]:
    """Extract code pieces from a text string.
    Args:
        text: str, model prediciton text.
    Rets:
        code_pieces: list[str], code pieces in the text.
    """
    code_pieces = []
    while "```python" in text:
        st_idx = text.index("```python") + 10
        # end_idx = text.index("```", st_idx)
        if "```" in text[st_idx:]:
            end_idx = text.index("```", st_idx)
        else: 
            end_idx = len(text)
        code_pieces.append(text[st_idx:end_idx].strip())
        text = text[end_idx+3:].strip()
    return code_pieces


def wrap_code(code: str) -> str:
    """Wrap the input code with markdown python identifiers."""
    if "``python" in code: return code
    return f"```python\n{code}\n```"


def unwrap_code(text: str) -> str:
    """Unwrap a code block."""
    if "```python" in text:
        sidx = text.index("```python") + 10

        if "```" in text[sidx:]:
            eidx = text.index("```", sidx)
        else:
            eidx = len(text)
        return text[sidx:eidx].strip()
    else: 
        return text.strip()


def clean_import(code_pieces: list[str]) -> list[str]:
    cleaned_pieces = []
    for code in code_pieces:
        code_lines = code.split('\n')
        clean_lines = []
        for cline in code_lines:
            if ("import" in cline) and ("toolbox" in cline):
                continue
            clean_lines.append(cline)
        cleaned_pieces.append('\n'.join(clean_lines))
    return cleaned_pieces


# %% Function Tools
def is_def_line(line: str) -> bool:
    """Check if the line string is a function definition line.
    E.g., 'def check_exists(item) -> bool:'
    """
    return all([(symbol in line) for symbol in ['def', '(', ')', ':']])


def get_function_docstr(function: str) -> str:
    """Get the docstring of a tool function."""
    if '"""' not in function: return ""
    docstr_start = function.index('"""') + 3
    if "Args:" in function[docstr_start: ]:
        docstr_end = function.index('Args:', docstr_start)
    else: 
        docstr_end = function.index('"""', docstr_start)
    return function[docstr_start: docstr_end].strip()


def get_function_name(function: str) -> str: 
    """Get the function name of the tool."""
    assert "def" in function
    def_index = function.index("def") + 3
    end_index = function.index('(', def_index)
    return function[def_index: end_index].strip()
    

def get_function_signature(function: str) -> str:
    """Get function signature of the tool."""
    assert "def" in function
    def_index = function.index("def") + 3
    mid_index = function.index(')', def_index)
    sig_end_index = function.index(':', mid_index)
    return function[def_index: sig_end_index].strip()


def parse_function_tools(code_lines: list[str], def_indices: list[int]) -> list[dict]:
    """Parse all function tools in the code chunk."""
    tools_list = []

    prefix = "\n".join(code_lines[:def_indices[0]])
    for i,d in enumerate(def_indices):
        if i == len(def_indices) - 1:
            function = "\n".join(code_lines[d: ])
        else:
            function = "\n".join(code_lines[d: def_indices[i+1]])

        try:
            func_dict = {
                "docstr": get_function_docstr(function),
                "name": get_function_name(function), 
                "signature": get_function_signature(function),
                "function": prefix + '\n' + function,
                "type": "function",
            }
            tools_list.append(func_dict)
        except:
            continue
    return tools_list


# %% Import Tools

def is_import_line(line: str) -> bool:
    """Check if the line string is an import expressiom.
    E.g., 'import os', 'from os import path'
    """
    return "import" in line


def parse_library_functions(code: str) -> list[str]:
    """Parse individual functions in the import expression."""
    assert '\n' not in code
    if ',' in code:
        if code.startswith("import"): # "import math, random"
            sidx = code.index("import") + 6
            lib_list = code[sidx: ].strip().split(',')
            lib_list = [lib.strip() for lib in lib_list if lib.strip() != ""]
            tool_dict_list = []
            for lib in lib_list:
                if " as" in lib:
                    eidx = lib.index(" as")
                else:
                    eidx = len(lib)
                tool_dict = {
                    "name": lib[: eidx].strip(),
                    "docstr": code.strip(),
                    "signature": code.strip(),
                    "function": code.strip(),
                    "type": "import",
                }
                tool_dict_list.append(tool_dict)
                return tool_dict_list
        elif code.startswith("from"): # "from sympy import solve, symbols"
            assert "import" in code
            sidx = code.index("import")
            library = code[5: sidx].strip()
            func_list = code[sidx+6: ].strip().split(',')
            func_list = [func.strip() for func in func_list if func.strip() != ""]
            return [
                {
                    "name": f"{library}.{func}",
                    "docstr": f"from {library} import {func}",
                    "signature": f"from {library} import {func}",
                    "function": f"from {library} import {func}",
                    "type": "import",
                }
                for func in func_list
            ]
        else:
            print(code)
            return []
    else:
        if code.startswith("import"): # "import math", "import numpy as np", "import sympy.solve"
            sidx = code.index("import") + 6
            if " as" in code[sidx: ]:
                eidx = code.index(" as", sidx)
            else:
                eidx = len(code)
            lib_func = code[sidx: eidx].strip()
            return [{
                "name": lib_func,
                "docstr": code.strip(),
                "signature": code.strip(),
                "function": code.strip(),
                "type": "import",
            }]
        elif code.startswith("from"): # "from sympy import solve"
            assert "import" in code
            sidx = code.index("import")
            library = code[5: sidx].strip()
            func = code[sidx+6: ].strip()
            return [{
                "name": f"{library}.{func}",
                "docstr": code.strip(),
                "signature": code.strip(),
                "function": code.strip(),
                "type": "import",
            }]
        else:
            print(code)
            return []


def parse_import_tools(code_or_lines: str | list[str]) -> list[dict]:
    if code_or_lines is None: return []
    if isinstance(code_or_lines, str):
        code_lines = code_or_lines.split('\n')
    else:
        code_lines = code_or_lines
    code_lines = [cl.strip() for cl in code_lines if ("import" in cl)]

    tool_list = []
    for cline in code_lines:
        tool_list.extend(parse_library_functions(cline))
    return tool_list



# %% Tool Parsing

def parse_tools_in_chunk(code_chunk: str) -> list[dict]:
    """Parse all tools in one wrapped code chunk.
    - if a function definition is found, it's an ADD/EDIT tool
    - if only import statements are found, it's an IMPORT tool
    - otherwise, not a valid tool
    """
    code_lines = code_chunk.split("\n")
    # if definition line is found
    def_indices = [i for i,l in enumerate(code_lines) if is_def_line(l)]
    if len(def_indices) > 0:
        tools_list = parse_function_tools(code_lines, def_indices)

    # if all lines are import statements
    else:
        code_lines = [l for l in code_lines if is_import_line(l)]
        if len(code_lines) > 0:
            tools_list = parse_import_tools(code_lines)
        else:
            tools_list = []

    return tools_list



def parse_tools(text: str) -> list[dict[str, str]]:
    """Parse all tools in the text piece.
    - ADD/EDIT tools, involves 'def' clause in code chunk
    - IMPORT tools, all valid lines are 'import' clauses
    """
    code_pieces = extract_code_pieces(text)  
    # ```python``` wrapped chunks, can contain multiple functions

    tool_dicts = []
    for code_chunk in code_pieces:
        chunk_tool_dicts = parse_tools_in_chunk(code_chunk)
        tool_dicts.extend(chunk_tool_dicts)
    return tool_dicts




# %% Toolbox

DELIMITER = "# %%"

def load_toolbox(
    toolbox_path: str, 
    delimiter: str = DELIMITER,
) -> dict[str, dict[str, str]]:
    """Load toolbox from a .py file."""
    toolbox = {}

    docstr = ""
    tool_type = ""
    curr_tool_lines = []

    for tline in open(toolbox_path, 'r').readlines():
        if tline.startswith(delimiter):
            # add previous tool to toolbox, if any
            if len(curr_tool_lines) > 0:
                def_indices = [i for i,l in enumerate(curr_tool_lines) if is_def_line(l)]
                if len(def_indices) > 0:
                    tool_dicts = parse_function_tools(curr_tool_lines, def_indices)
                    assert len(tool_dicts) == 1
                    toolbox[tool_dicts[0]["name"]] = tool_dicts[0]
                else:
                    tool_dicts = parse_import_tools(curr_tool_lines)
                    assert len(tool_dicts) == 1
                    toolbox[tool_dicts[0]["name"]] = tool_dicts[0]

            # initiate new tool
            docstr = tline.lstrip(delimiter).strip()
            curr_tool_lines = []
        else: 
            curr_tool_lines.append(tline)

    # add the last tool
    if len(curr_tool_lines) > 0:
        def_indices = [i for i,l in enumerate(curr_tool_lines) if is_def_line(l)]
        if len(def_indices) > 0:
            tool_dicts = parse_function_tools(curr_tool_lines, def_indices)
            assert len(tool_dicts) == 1
            toolbox[tool_dicts[0]["name"]] = tool_dicts[0]
        else:
            tool_dicts = parse_import_tools(curr_tool_lines)
            assert len(tool_dicts) == 1
            toolbox[tool_dicts[0]["name"]] = tool_dicts[0]

    for tool_name, tool_dict in toolbox.items():
        toolbox[tool_name].update({"frequency": 0, "indices": []})
    return toolbox



def format_toolbox(toolbox: dict[str, dict[str, str]], topk: int = 10) -> str:
    name_freq_list = [(name, d["frequency"]) for name,d in toolbox.items()]
    name_freq_list = sorted(name_freq_list, key=lambda x: -x[1])

    toolbox_str_list = []
    for tool_name,_ in name_freq_list[: topk]:
        tool_dict = toolbox[tool_name]
        tool_str = f"# {tool_dict['docstr']}\n{tool_dict['signature']}"
        toolbox_str_list.append(wrap_code(tool_str))
    return '\n'.join(toolbox_str_list)


def dump_toolbox(
    toolbox: dict[str, dict[str, str]], 
    toolbox_path: str, 
    delimiter: str = DELIMITER,
) -> None:
    with open(toolbox_path, 'w') as fw:
        for tool_dict in toolbox.values():
            fw.write(f"{delimiter} {tool_dict['docstr']} ({tool_dict['type']})\n")
            fw.write(tool_dict['function'] + '\n\n\n')
