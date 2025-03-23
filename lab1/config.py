from pathlib import Path
from dotenv import load_dotenv
import os

def load_config():
    """Load configuration from .env file."""
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)
    
    config = {
        'API1_KEY': os.getenv('API1_KEY'),
        'API2_KEY': os.getenv('API2_KEY'),
    }
    
    missing_vars = [key for key, value in config.items() if not value]
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return config
