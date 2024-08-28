#%%
import requests
import os
import sys
from bs4 import BeautifulSoup
sys.path.append(os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))))
from models.FalconsAI.model import *

api_key=os.environ.get("API_KEY")
cse_id = os.environ.get('CSE_ID')

def google_search(query, api_key = api_key, cse_id = cse_id, num_results=5):
    search_url = f"https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cse_id,
        "num": num_results
    }
    response = requests.get(search_url, params=params)
    results = response.json()
    search_results = [
        (item['link']) for item in results.get('items', [])
    ]
    return search_results

def get_body(links):
    contents = []
    for link in links:
        try:
            response = requests.get(link)
            response.raise_for_status()  
            soup = BeautifulSoup(response.text, 'html.parser')
            content = ' '.join([p.get_text() for p in soup.find_all('p')])
            contents.append(content)
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
    return contents

def get_search_summary(query):
    links = google_search(query)
    contents = get_body(links)
    summaries = []
    for val in contents:
        summaries.append(get_summary(val))
    return summaries
# %%
temp = get_search_summary('what is quantum fusion?')
# %%
