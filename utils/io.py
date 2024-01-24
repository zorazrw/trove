"""Utility Function for I/O Operations."""

import json


def load_json_file(
    path: str, 
    max_num_examples: int = None,
) -> list:
    """Load dataset from a json or jsonl file.""" 
    if path.endswith(".json"):
        dataset = json.load(open(path, 'r'))
    elif path.endswith(".jsonl"):
        dataset = [json.loads(l.strip()) for l in open(path, 'r')]
    else:
        raise ValueError(f"Invalid file type: {path}")
    if max_num_examples is None:
        return dataset 
    else:
        print(f"Loaded {len(dataset)} examples, using the first {max_num_examples} for experiment only.")
        return dataset[: max_num_examples]


def dump_json_file(data: dict | list[dict], path: str):
    """Write dataset into a json or jsonl file."""
    if path.endswith(".json"):
        json.dump(data, open(path, 'w'))
    elif path.endswith(".jsonl"):
        assert isinstance(data, list)
        with open(path, 'w') as fw:
            for item in data:
                fw.write(json.dumps(item) + "\n")
    else:
        raise ValueError(f"Invalid file type: {path}")


def load_gqa_dataset(
    path: str,
    max_num_examples: int = None,
) -> list[dict]:
    datadict = load_json_file(path)
    key_list = list(datadict.keys())
    print(f"Loaded {len(datadict)} examples, using the first {max_num_examples} for experiment only.")
    if max_num_examples is not None:
        key_list = key_list[: max_num_examples]
    dataset = [datadict[k] for k in key_list]
    return dataset


# %% Dataset Loader

def load_dataset(task: str, max_num_examples: int = None) -> list[dict]:
    """Load json/jsonl datasets in the experiments."""
    from utils.constant import DATA_PATH, ERROR_HITAB_DATA

    loader = load_gqa_dataset if task == "gqa" else load_json_file
    dataset = loader(DATA_PATH[task], max_num_examples)
    if task == "hitab":  # remove erroneous hitab examples
        dataset = [ex for i,ex in enumerate(dataset) if i not in ERROR_HITAB_DATA]
    return dataset
