"""Utility Function for API Calls."""

import time
import openai
import random


# %% Cost Estimation

TOKENIZER_NAME = "cl100k_base"
COST_UNIT_SIZE = 1000
PRICE_MAP = {
    "gpt-3.5-turbo": {"input_price": 0.0015, "output_price": 0.002},
    "gpt-4": {"input_price": 0.03, "output_price": 0.06},
}


# %% API Keys
key_pool = [line.strip() for line in open("./utils/keys.txt", 'r')]
key_num = len(key_pool)
# openai.api_key = key_pool[0]
openai.api_key = random.sample(key_pool, 1)[0]

STOP_TOKENS = ["###", "===", "**"]


# %% Call API

def chat_api_wait(
    user_msg: str, system_msg: str, 
    model_name: str = "gpt-3.5-turbo",
    total_iters: int = 1, sleep_interval: int = 30, 
    temperature: float = 0.3, max_tokens: int = 1024, 
    top_p: float = None, n: int = 1, 
) -> list[str] | None:
    i_iter = 0
    while i_iter < total_iters:
        i_iter += 1
        openai.api_key = random.sample(key_pool, 1)[0]
        try:
            response_list = openai.ChatCompletion.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": system_msg},
                    {"role": "user", "content": user_msg},
                ],
                temperature=temperature,
                max_tokens=max_tokens,
                top_p=top_p,
                n=n,
                # stop=STOP_TOKENS, 
            )
            return [
                choice["message"]["content"].strip()
                for choice in response_list["choices"]
            ]
        except:
            time.sleep(i_iter * sleep_interval)
    # raise Exception("Iterations exhausted")
    return ["" for _ in range(n)]


def calc_price(num_input_tokens: int, num_output_tokens: int, model_name: str):
    input_unit_price = PRICE_MAP[model_name]["input_price"]
    output_unit_price = PRICE_MAP[model_name]["output_price"]
    input_cost = input_unit_price * num_input_tokens / COST_UNIT_SIZE
    output_cost = output_unit_price * num_output_tokens / COST_UNIT_SIZE
    print(' | '.join([
        f"Input Cost: {input_cost:.2f}",
        f"Output Cost: {output_cost:.2f}",
        f"Total Cost: {input_cost+output_cost:.2f}"
    ]) + '\n')
