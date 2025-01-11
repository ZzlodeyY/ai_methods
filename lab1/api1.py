from typing import Dict, Optional
import requests
from config import load_config

class API1Client:
    
    def __init__(self):
        config = load_config()
        self.api_key = config['API1_KEY']
        self.base_url = "https://sentiment-api3.p.rapidapi.com"
        self.headers = {
            "x-rapidapi-key": self.api_key,
            "x-rapidapi-host": "sentiment-api3.p.rapidapi.com",
            "Content-Type": "application/json"
        }

    def _transform_response(self, api_response: Dict) -> Dict:
        """Transform API response to standardized format."""
        overall_sentiment = api_response.get('overall_sentiment', '').lower()
        confidence_score = api_response.get('confidence_score', 0.0)
        
        sentiment_scores = {'negative': 0.0, 'neutral': 0.0, 'positive': 0.0}
        if 'positive' in overall_sentiment:
            sentiment_scores['positive'] = confidence_score
        elif 'negative' in overall_sentiment:
            sentiment_scores['negative'] = confidence_score
        else:
            sentiment_scores['neutral'] = confidence_score
            
        return {
            'outputs': sentiment_scores,
            'confidence': confidence_score
        }

    def analyze_sentiment(self, text: str) -> Optional[Dict]:
        """Analyze sentiment of the given text."""
        url = f"{self.base_url}/sentiment_analysis"
        payload = {"input_text": text}
        
        try:
            response = requests.post(url, json=payload, headers=self.headers)
            response.raise_for_status()
            result = response.json()
            return self._transform_response(result)
        except requests.exceptions.RequestException as e:
            print(f"Error in API1 request: {e}")
            return None