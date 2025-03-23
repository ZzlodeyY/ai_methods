
import asyncio
from huggingface_hub import InferenceClient
from config import DEFAULT_PARAMS, HF_TOKEN

client = InferenceClient(token=HF_TOKEN)


SYSTEM_PROMPT = """Ты — эксперт в подборе автомобилей. Пользователи могут задавать вопросы или указывать параметры (тип кузова, класс, тип двигателя, бюджет, предпочтения по брендам и др.). Основная задача — предоставить точные и полезные рекомендации по подходящим моделям авто. Обеспечивай ясные ответы, учитывай предпочтения пользователя и предлагай несколько вариантов с пояснениями о плюсах и минусах каждой модели.
"""

async def generate_response(model: dict, user_message: str) -> str:
    
    try:
        full_prompt = SYSTEM_PROMPT + "\n\nЗапрос пользователя: " + user_message.strip()

        params = {**DEFAULT_PARAMS, **model.get("parameters", {})}
        response = await asyncio.to_thread(
            client.text_generation,
            prompt=full_prompt,
            model=model["model_name"],
            max_new_tokens=params["max_new_tokens"],
            temperature=params["temperature"],
            top_k=params["top_k"],
            repetition_penalty=params["repetition_penalty"],
            do_sample=True
        )
       

        return response

    except Exception as e:
        raise Exception(f"Ошибка генерации: {str(e)}")
