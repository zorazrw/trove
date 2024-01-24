"""Utility Function to Create Prompts."""

import os
import json
import pandas as pd
import numpy as np
from utils.io import load_json_file
from utils.eval import calc_unigram_f1


# %% MATH
def get_math_prompt_args(example: dict) -> dict[str, str]:
    """Create prompt render arguments for MATH examples.
    i.e., {"question": str}
    """
    return {"question": example["question"]}


# %% TabMWP
def format_tabmwp_table_markdown(table: str) -> str:
    table_lines = table.split('\n')
    rows_index = None
    for i, l in enumerate(table_lines):
        if '|' in l:
            rows_index = i
            break
    table_rows = table_lines[rows_index:]
    table_md_rows = []
    table_md_rows.append('| ' + table_rows[0] + ' |')
    num_columns = len(table_rows[0].split('|'))
    table_md_rows.append('| ' + ' --- |' * num_columns)
    for row in table_rows[1:]:
        table_md_rows.append('| ' + row + ' |')
    return '\n'.join(table_lines[: rows_index] + table_md_rows)


def get_tabmwp_prompt_args(example: dict) -> dict[str, str]:
    """Create prompt render arguments for TabMWP examples.
    i.e., {"question": str, "table" str}
    """
    return {
        "question": example["question"],
        "table": format_tabmwp_table_markdown(example["table"]),
    }


# %% WTQ
def serialize_wtq_table_markdown(table: dict) -> str:
    table_rows = []
    table_rows.append('| ' + ' | '.join(table["header"]) + ' |')
    table_rows.append('| ' + ' --- |' * len(table["header"]))
    for trow in table["rows"]:
        table_rows.append('| ' + ' | '.join(trow) + ' |')
    return '\n'.join(table_rows)


def create_wtq_table_preview(question: str, table: dict, topk: int = 3) -> str:
    # select columns
    question_header_similarity = [
        calc_unigram_f1(question, [header_text])
        for header_text in table["header"]
    ]
    qh_sim = np.array(question_header_similarity)
    column_indices = qh_sim.argsort()[-topk:][::-1]
    column_indices.sort()
    column_indices = column_indices.tolist()
    if column_indices[0] != 0:
        column_indices = [0] + column_indices

    # select rows
    question_row_similarity = [
        calc_unigram_f1(question, row_cells)
        for row_cells in table["rows"]
    ]
    qr_sim = np.array(question_row_similarity)
    row_indices = qr_sim.argsort()[-topk:][::-1]
    row_indices.sort()
    row_indices = row_indices.tolist()
    if row_indices[0] != 0:
        row_indices = [0] + row_indices

    # create preview
    preview_header = [table["header"][i] for i in column_indices]
    preview_rows = []
    for i, row in enumerate(table["rows"]):
        if i in row_indices:
            preview_rows.append([row[i] for i in column_indices])
    table_preview_dict = {"header": preview_header, "rows": preview_rows}
    return serialize_wtq_table_markdown(table_preview_dict)


def get_wtq_prompt_args(example: dict) -> dict[str, str]:
    """Create prompt render arguments for WTQ examples.
    e.g., example["table"]["name"] = "csv/203-csv/435.tsv"
    i.e., {"question": str, "table_file" str, "table_preview": str}
    """
    table_file = "File: " + os.path.join(
        "data", "wtq", example["table"]["name"]
    )
    table_preview = "Preview: " + create_wtq_table_preview(
        example["question"], example["table"]
    )
    return {
        "question": example["question"],
        "table": table_file + '\n' + table_preview,
        "table_file": table_file,
        "table_preview": table_preview,
    }


# %% HiTab

TOP_ROOT_VAL = '<TOP>'
LEFT_ROOT_VAL = '<LEFT>'


def _preorder_traversal(
    node: dict,
    parsed_columns: list,
    tup=tuple(),
    root_val=TOP_ROOT_VAL,
) -> list[str | tuple[str]]:
    if node['value'] != root_val:
        tup = tup + (node["value"],)
    if node.get("line_idx", None) is not None:
        parsed_columns.append(tup)
    for children in node["children_dict"]:
        _preorder_traversal(children, parsed_columns, tup)
    return parsed_columns


def _get_data(data: list[list[dict]]) -> list[list[float]]:
    values = []
    for column in data:
        col_vals = [cell["value"] for cell in column]
        values.append(col_vals)
    return values


def parse_table(file_path: str) -> pd.DataFrame:
    table_dict = json.load(open(file_path, 'r'))

    top_columns = []
    top_columns = _preorder_traversal(
        table_dict["top_root"], top_columns, root_val=TOP_ROOT_VAL
    )

    left_index = []
    left_index = _preorder_traversal(
        table_dict["left_root"], left_index, root_val=LEFT_ROOT_VAL
    )

    columns = pd.MultiIndex.from_tuples(top_columns)
    index = pd.MultiIndex.from_tuples(left_index)
    values = _get_data(table_dict["data"])
    # generate pandas dataframe
    try:
        df = pd.DataFrame(values, index=index, columns=columns).fillna("")
        return df
    except Exception as e:
        print(f"Error: {e}")


def get_df_preview(df: pd.DataFrame) -> str:
    return df.head().to_markdown()


def get_table_preview(table_path: str) -> str:
    df = parse_table(table_path)
    return get_df_preview(df)


def get_table_title(table_path: str) -> str:
    table_dict = load_json_file(table_path)
    return table_dict["title"]


def get_hitab_prompt_args(example: dict) -> dict[str, str]:
    """Create prompt render arguments for HiTab examples.
    e.g., example["table_id"]["name"] = "100"
    i.e., {"question": str, "table_file" str, "table_preview": str}
    """
    table_path = os.path.join(
        "data", "hitab", "tables", "hmt", f"{example['table_id']}.json"
    )
    table_file = "File: " + table_path
    table_preview = "Preview: " + get_table_title(table_path) + \
        '\n' + get_table_preview(table_path)
    return {
        "question": example["question"],
        "table": table_file + '\n' + table_preview,
        "table_file": table_file,
        "table_preview": table_preview,
    }


# %% GQA
def get_gqa_prompt_args(example: dict) -> dict[str, str]:
    """Create prompt render arguments for GQA examples.
    e.g., example["imageId"] = "n54424"
    i.e., {"question": str, "image": str}
    """
    return {
        "question": example["question"],
        "image": os.path.join(
            "data", "gqa", "testdev_images", f"{example['imageId']}.jpg"
        ),
    }


# %% Prompt Args Function

PROMPT_ARGS_FUNC = {
    "math": get_math_prompt_args,
    "tabmwp": get_tabmwp_prompt_args,
    "wtq": get_wtq_prompt_args,
    "hitab": get_hitab_prompt_args,
    "gqa": get_gqa_prompt_args,
}
