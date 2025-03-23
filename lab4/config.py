# config.py
from environs import Env

env = Env()
env.read_env()


HF_TOKEN = env.str("HUGGINGFACE_TOKEN")
TG_TOKEN = env.str("TELEGRAM_TOKEN")


MODELS = {
    "Llama": {
        "model_name": "meta-llama/Llama-3.2-1b",
        "parameters": {
            "temperature": 1.0,
            "top_k": 50,
            "repetition_penalty": 1.8,
            "max_new_tokens": 100
        }
    },
    "GPT": {
        "model_name": "ai-forever/rugpt3medium_based_on_gpt2",
        "parameters": {
            "temperature": 1.0,
            "top_k": 30,
            "repetition_penalty": 1.9,
            "max_new_tokens": 100
        }
    }
}


DEFAULT_PARAMS = {
    "temperature": 0.7,
    "top_k": 50,
    "repetition_penalty": 1.1,
    "max_new_tokens": 500
}
