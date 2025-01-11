from dataclasses import dataclass
from typing import Dict
from environs import Env

@dataclass
class BotConfig:
    tg_token: str
    hf_token: str
    model_urls: Dict[str, str]

def load_config() -> BotConfig:
    env = Env()
    env.read_env()

    return BotConfig(
        tg_token=env.str("TELEGRAM_TOKEN"),
        hf_token=env.str("HUGGINGFACE_TOKEN"),
        model_urls={
            "llama": "https://api-inference.huggingface.co/models/IlyaGusev/saiga_llama3_8b",
            "gpt-neo": "https://api-inference.huggingface.co/models/ai-forever/rugpt3medium_based_on_gpt2"
        }
    )