"""Online Function Induction and Program Solution Generation."""

import os
import math
import torch
import random
import argparse
import transformers
from utils import *
from mako.template import Template
from transformers import AutoTokenizer


def main():
    # load dataset and prompt templates
    dataset = load_dataset(args.task_name, args.max_num_examples)
    if args.shuffle_seed is not None:
        random.Random(args.shuffle_seed).shuffle(dataset)
    # prompt templates
    create_path = os.path.join("prompt", args.task_name, "online_create.md")
    template_create = Template(filename=create_path)
    import_path = os.path.join("prompt", args.task_name, "online_import.md")
    template_import = Template(filename=import_path)
    skip_path = os.path.join("prompt", args.task_name, "online_skip.md")
    template_skip = Template(filename=skip_path)

    if '/' in args.task_name:
        args.task_name = args.task_name.split('/')[0]
    # library
    library_path = os.path.join("toolbox", f"{args.task_name}.py")
    default_library = load_toolbox(library_path)
    library = load_toolbox(library_path)

    # configure generation pipeline
    pipeline = transformers.pipeline(
        "text-generation", model=args.model_name,
        torch_dtype=torch.float16, device_map="auto",
    )
    pipeline.tokenizer.pad_token_id = pipeline.model.config.eos_token_id
    tokenizer = AutoTokenizer.from_pretrained(args.model_name)
    stable_gen_args = {
        "num_return_sequences": args.num_return_sequences,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "eos_token_id": tokenizer.eos_token_id,
        "pad_token_id": tokenizer.eos_token_id,
    }
    
    fw_log = open(args.output_log_path, 'w')

    def get_example_responses(
        example: dict, index: int, template: Template, library: dict,
    ) -> list[dict]:
        """Get model responses [solution + function(s)] for an example. """
        # input
        prompt_args = PROMPT_ARGS_FUNC[args.task_name](example)
        if len(library) > 0 or args.task_name.startswith("math"):
            prompt_args["toolbox"] = format_toolbox(library)
            prompt = template.render(**prompt_args)
            write_prompt(fw_log, prompt, prompt_args["toolbox"], index)
        else:
            prompt = template.render(**prompt_args)
            write_prompt(fw_log, prompt, "", index)

        # output
        max_tokens = len(tokenizer(prompt)["input_ids"]) + args.max_new_tokens
        response_list = pipeline(
            prompt, do_sample=True, max_length=max_tokens, **stable_gen_args
        )
        resp_dict_list = []
        for r in response_list:
            r = extract_llama_response(r["generated_text"], input_text=prompt)
            resp_dict_list.append(parse_model_response(r))

        # execute
        for j, res in enumerate(resp_dict_list):
            # collect code pieces
            code_pieces = []
            for _, func_dict in library.items():
                code_pieces.append(func_dict["function"])
            for func_dict in res["function"]:
                code_pieces.append(func_dict["function"])
            code_pieces.append(unwrap_code(res["solution"]))
            code_pieces = clean_import(code_pieces)

            # execute, evaluate
            is_success, exec_output = execute_code_wrapped(
                code_pieces=code_pieces,
                exec_file=args.exec_file,
                timeout=args.exec_timeout,
            )
            if "answer" in ex:
                answer = ex["answer"]
            elif "answers" in ex:
                answer = ex["answers"]
            else:
                raise ValueError(f"Invalid example w/o answers: {ex.keys()}")
            is_correct, model_answer = EVAL_FUNC[args.task_name](
                is_success=is_success, model_output=exec_output,
                answer=answer, return_answers=True,
            )
            exec_dict = {
                "is_success": is_success,
                "is_correct": is_correct,
                "exec_output": exec_output,
                "model_answers": model_answer,
                "answer": answer,
            }

            # update results, log, and library
            resp_dict_list[j].update(exec_dict)
            write_exec_result(fw_log, exec_dict, index=j)
            write_solution_and_tools(fw_log, res, library, update_toolbox=False, index=j)

        return resp_dict_list


    def update_library(
        function_list: list[dict], library: dict, match_old: bool = False
    ) -> dict:
        """Update library with function usage or creation."""
        for func_dict in function_list:
            func_name = func_dict["name"]
            if func_name.startswith("toolbox."):
                func_name = func_name[8: ]
            if func_name not in library:
                library[func_name] = func_dict
                library[func_name]["indices"] = [i]
                library[func_name]["frequency"] = 1
            elif match_old and (func_name in library):
                library[func_name]["indices"].append(i)
                library[func_name]["frequency"] += 1
        return library


    def multi_way_generation(
        example: dict, index: int,
        modes: list[str] = ["import", "create", "skip"]
    ) -> dict:
        """Multi-way generation of selected modes."""
        candidate_list = []
        if "import" in modes:
            import_resp_list = get_example_responses(
                example, index, template_import, library
            )
            best_import_index = select_best_solution(import_resp_list)
            candidate_list.append(import_resp_list[best_import_index])

        if "create" in modes:
            create_resp_list = get_example_responses(
                example, index, template_create, default_library
            )
            best_create_index = select_best_solution(create_resp_list)
            candidate_list.append(create_resp_list[best_create_index])

        if "skip" in modes:
            skip_resp_list = get_example_responses(
                example, index, template_skip, default_library
            )
            best_skip_index = select_best_solution(skip_resp_list)
            candidate_list.append(skip_resp_list[best_skip_index])

        best_resp_index = select_best_solution(candidate_list)
        best_mode = modes[best_resp_index]
        best_resp = candidate_list[best_resp_index]

        if best_mode == "import":
            update_library(best_resp["function"], library, match_old=True)
        if (best_mode == "create") and (best_resp["is_success"]):
            update_library(best_resp["function"], library, match_old=False)

        return {"mode": best_mode, "response": best_resp}


    def trim_library(n: int, library: dict) -> dict:
        """Trimming low-frequency functions from the library."""
        threshold = math.log(n, 20)
        print(
            f"Trimming library of size #{len(library)}",
            f"Usage frequency threshold: {threshold:.2f}",
        )
        for name,d in library.items():
            print(name, " | ", d["frequency"])
            if d["frequency"] < threshold:
                for idx in d["indices"]: trimmed_indices.add(idx)
        library = {name: d for name,d in library.items() if d["frequency"]>=threshold}
        print(f"To size #{len(library)}")
        return library


    # start streaming examples
    result_list = []
    trimmed_indices = set()

    for i, ex in enumerate(dataset):
        # multi-channel (3-way) generation
        result_dict = multi_way_generation(
            example=ex, index=i,
            modes=["import", "create", "skip"]
        )
        result_list.append(result_dict)

        # periodic forgetting
        if (i + 1) % args.trim_steps == 0:
            library = trim_library(i + 1, library)

    # final forgetting
    library = trim_library(len(dataset), library)

    correct_list = [r["response"]["is_correct"] for r in result_list]
    acc = sum(correct_list) / len(correct_list)
    print(f"Overall Response Accuracy: {acc:.2f}")
    print(f"Toolbox Size: #{len(library)}")
    fw_log.write(f"\n## Overall Response Accuracy: {acc:.2f}\n")
    fw_log.write(f"Toolbox Size: #{len(library)}")


    # update solutions of examples missing tools
    trimmed_indices = sorted(list(trimmed_indices))
    print(f"Re-generate solutions for #{len(trimmed_indices)} examples.")
    for i in trimmed_indices:
        result_dict = multi_way_generation(dataset[i], i, ["import", "skip"])
        result_list[i] = result_dict  # update result record

    correct_list = [r["response"]["is_correct"] for r in result_list]
    acc = sum(correct_list) / len(correct_list)
    print(f"Updated Response Accuracy: {acc:.2f}")

    fw_log.write(f"\n## Overall Response Accuracy: {acc:.2f}\n")
    fw_log.write(f"Toolbox Size: #{len(library)}")
    for name, d in library.items():
        fw_log.write(f"=== {name} ===\n")
        fw_log.write(d["function"])
        fw_log.write('\n\n\n')
    fw_log.close()

    dump_json_file(result_list, args.output_results_path)
    dump_toolbox(library, args.output_library_path)




if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # data config
    parser.add_argument("--task_name", type=str, required=True,
                        choices=[
                            "math/algebra", "math/counting", "math/geometry",
                            "math/intermediate", "math/number",
                            "math/prealgebra", "math/precalculus",
                            "tabmwp", "wtq", "hitab", "gqa"
                        ],
                        help="Task name.")
    parser.add_argument("--shuffle_seed", type=int, default=None)
    
    # experiment config
    parser.add_argument("--run_index", type=int, default=None)

    # example config
    parser.add_argument("--max_num_examples", type=int, default=None,
                        help="Maximum number of examples to generate.")
    parser.add_argument("--trim_steps", type=int, default=500,
                        help="Trim library by threshold every N examples.")

    # execution config
    parser.add_argument("--exec_file", type=str, default="tmp_exec_online.py",
                        help="Temporary execution file.")
    parser.add_argument("--exec_timeout", type=int, default=100,
                        help="Timeout for execution in seconds.")

    # generation config
    parser.add_argument("--model_name", type=str, 
                        default="codellama/CodeLlama-7b-Instruct-hf")
    parser.add_argument("--top_p", type=float, default=0.95)
    parser.add_argument("--num_return_sequences", type=int, default=1)
    parser.add_argument("--temperature", type=float, default=0.3)
    parser.add_argument("--max_new_tokens", type=int, default=256)

    args = parser.parse_args()
    args.suffix = "trove"
    args = auto_decide_path(args, fields=["library", "log"])

    main()
