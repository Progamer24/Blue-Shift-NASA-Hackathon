import requests
from django.conf import settings

class NASADataFetcher:
    """
    Handles fetching data from various NASA APIs
    """
    def __init__(self):
        self.api_key = settings.NASA_API_KEY
        self.base_url = settings.NASA_BASE_URL
    
    def fetch_apod(self, date=None):
        """
        Fetch NASA's Astronomy Picture of the Day
        """
        url = f"{self.base_url}/planetary/apod"
        params = {'api_key': self.api_key}
        if date:
            params['date'] = date
        
        try:
            response = requests.get(url, params=params)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Error fetching APOD: {e}")
            return None
    
    def fetch_mars_weather(self):
        """
        Fetch Mars weather data (example endpoint)
        """
        url = f"{self.base_url}/insight_weather/"
        params = {'api_key': self.api_key, 'feedtype': 'json', 'ver': '1.0'}
        
        try:
            response = requests.get(url, params=params)
            return response.json() if response.status_code == 200 else None
        except Exception as e:
            print(f"Error fetching Mars weather: {e}")
            return None
