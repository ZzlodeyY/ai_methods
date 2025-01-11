from typing import Dict, Optional
import requests
from config import load_config

class API2Client:
    
    def __init__(self):
        config = load_config()
        self.api_key = config['API2_KEY']
        self.auth_token = config['AUTH_TOKEN']
        self.base_url = "https://moroccan-darija-sentiment-analysis.p.rapidapi.com"
        self.headers = {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": "moroccan-darija-sentiment-analysis.p.rapidapi.com",
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": self.auth_token
        }

    def analyze_sentiment(self, text: str) -> Optional[Dict]:
        url = f"{self.base_url}/api/sentimentAnalysis"
        payload = f"InputText={text}"
        
        try:
            response = requests.post(url, data=payload, headers=self.headers)
            response.raise_for_status()
            result = response.json()
            
            if 'Sentiment Analysis' in result:
                sentiment_data = result['Sentiment Analysis']
                return {
                    'sentiment': sentiment_data.get('sentiment', 'unknown'),
                    'confidence': sentiment_data.get('confidence_score', 0.0)
                }
            else:
                print(f"Unknown API response structure: {result}")
                return None
                
        except requests.exceptions.RequestException as e:
            print(f"Error in API2 request: {e}")
            return None