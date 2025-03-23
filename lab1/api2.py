from typing import Dict, Optional
import requests
from config import load_config

class API2Client:
    
    def __init__(self):
        config = load_config()
        self.api_key = config['API2_KEY']
        # Убрали auth_token
        self.base_url = "https://text-analysis-classification-summarisation.p.rapidapi.com"
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "text-analysis-classification-summarisation.p.rapidapi.com",
            "Content-Type": "application/json"
        }

    def analyze_sentiment(self, text: str) -> Optional[Dict]:
        """
        Отправляет текст на анализ тональности к API:
        POST /api/v1/sentiment_analysis/
        Возвращает результат в формате:
        {
            "sentiment": "Positive" | "Negative" | "Neutral",
            "confidence": float
        }
        """
        url = f"{self.base_url}/api/v1/sentiment_analysis/"
        payload = {"sentence": text}
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            result = response.json()
            return {
                "sentiment": result.get("sentiment", "unknown"),
                "confidence": result.get("confidence", 0.0)
            }
        except requests.exceptions.RequestException as e:
            print(f"Error in API2 request: {e}")
            return None
