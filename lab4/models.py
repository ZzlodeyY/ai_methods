import aiohttp
from typing import Optional
from config import BotConfig

class ModelManager:
    _instance = None

    def __init__(self, config: BotConfig):
        self.config = config
        self.headers = {"Authorization": f"Bearer {config.hf_token}"}
        self.system_prompt = """Ты - опытный консультант по подбору автомобилей. Твоя задача - помогать пользователям 
        с выбором автомобиля на основе их запросов. При ответе на запрос пользователя:
        
        1. Всегда предлагай подборку из 3 разных автомобилей
        2. Для каждого автомобиля указывай:
           - Полное название модели и год выпуска
           - Основные характеристики (двигатель, мощность, расход топлива)
           - Примерную стоимость
           - Краткое описание преимуществ
        3. В конце подборки добавляй краткое заключение, почему именно эти автомобили подойдут пользователю
        4. Используй вежливый, профессиональный тон
        5. Учитывай все параметры из запроса пользователя
        6. Пиши на русском языке
        """

    @classmethod
    def initialize(cls, config: BotConfig):
        cls._instance = cls(config)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            raise RuntimeError("ModelManager не инициализирован")
        return cls._instance

    def _format_prompt(self, user_prompt: str) -> str:
        return f"{self.system_prompt}\n\nЗапрос пользователя: {user_prompt}\n\nПодборка автомобилей:"

    async def generate_response(self, model_name: str, prompt: str) -> Optional[str]:
        if model_name not in self.config.model_urls:
            return None

        # Форматирование запроса
        formatted_prompt = self._format_prompt(prompt)

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.config.model_urls[model_name],
                headers=self.headers,
                json={"inputs": formatted_prompt}
            ) as response:
                if response.status != 200:
                    return f"Ошибка: {response.status}"
                result = await response.json()
                # Проверка корректности ответа
                if isinstance(result, list) and result:
                    # Удаляем системный prompt из ответа, если он включен
                    generated_text = result[0].get("generated_text", "Ошибка генерации ответа")
                    if "Подборка автомобилей:" in generated_text:
                        generated_text = generated_text.split("Подборка автомобилей:", 1)[1].strip()
                    return generated_text

                return "Ошибка: некорректный ответ от модели"