from typing import Dict, Optional
import requests
from config import load_config

class API1Client:
    
    def __init__(self):
        config = load_config()
        self.api_key = config['API1_KEY']
        self.base_url = "https://aspect-based-sentiment-analysis.p.rapidapi.com"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "aspect-based-sentiment-analysis.p.rapidapi.com",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }

    def analyze_sentiment(self, text: str) -> Optional[Dict]:
       
        url = f"{self.base_url}/topic-sentiment?domain=generic"
        payload = [{
            "id": 1,
            "language": "en",
            "text": text
        }]
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            result = response.json()  

           
            negative_score = 0.0
            positive_score = 0.0
            neutral_score = 0.0

            
            if isinstance(result, list) and len(result) > 0:
                data = result[0]
                
                sentiments = data.get("sentiments", [])

                if not sentiments:
                    
                    neutral_score = 1.0
                else:
                    
                    for s in sentiments:
                        scale = s.get("scale", 0.0)
                        is_positive = s.get("positive", False)
                        if is_positive:
                            positive_score += scale
                        else:
                            negative_score += scale
            else:
                
                neutral_score = 1.0

            
            total = negative_score + neutral_score + positive_score
            if total > 0:
                negative_score /= total
                neutral_score /= total
                positive_score /= total

            return {
                "outputs": {
                    "negative": negative_score,
                    "neutral": neutral_score,
                    "positive": positive_score
                },
                
                "confidence": 1.0,
                "raw": result
            }
        except requests.exceptions.RequestException as e:
            print(f"Error in API1 request: {e}")
            return None
