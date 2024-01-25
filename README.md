# TROVE: Inducing Verifiable and Efficient Toolboxes for Solving Programmatic Tasks :hammer_and_wrench:

## Setup

Install the required packages:

```python
pip install -r requirements.txt
```

Tasks and datasets are organized as follows:
```
├── MATH
│   ├── algebra
│   ├── counting_and_probability
│   ├── geometry
│   ├── intermediate_algebra
│   ├── number_theory
│   ├── prealgebra
│   └── precalculus
├── TableQA
│   ├── TabMWP
│   ├── WTQ
│   └── HiTab
├── VQA
└── └── GQA
```

## Running Experiments

### Our Method: TroVE

```bash
python run_trove.py --task_name "math/algebra"
```

* For MATH tasks, specify the task name as _math/${dataset_name}_, e.g., _math/algebra_.
* For TableQA and VQA tasks, directly used the dataset name: [_tabmwp_, _wtq_, _hitab_, _gqa_].

Note that the specified `--task_name` argument should be lowercased.

### Baseline Methods: Primitive & Instance

```bash
python baseline.py --task_name "math/algebra" --suffix "primitive"  # or "instance"
```

Note that for GQA dataset, we implement the `locate_objects` and `visual_qa` functions as fast apis.
So you need to launch the server first (as below), then run the trove/baseline experiments.

```bash
uvicorn server.gqa:app
```

## Evaluation

```python
python -m utils.eval --results_path ${RESULTS_PATH}
```
