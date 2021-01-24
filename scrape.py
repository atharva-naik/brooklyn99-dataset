import json
import tqdm
import requests 
import warnings
from tqdm import tqdm
from bs4 import BeautifulSoup as bs

warnings.filterwarnings("ignore")

def get_episodes(base_url):
    page = requests.get(base_url).content
    soup = bs(page)
    seasons = soup.findAll("div",{'class':'series_seasons'})[0]
    return [episode.attrs['href'] for episode in seasons.findAll("a")]

def clean(text):
    text = text.replace('<div class="full-script"',"")
    text = text.replace("</div>","")
    text = text.replace("<br/>","\n")
    return text

# getting the episode urls from the homepage
episodes = get_episodes("https://subslikescript.com/series/Brooklyn_Nine-Nine-2467372")
f=open("scraped-episodes.txt","w")

for episode in tqdm(episodes):
    url = f"https://subslikescript.com{episode}"
    f.write(url)
    # dialogues=[]
    # page = requests.get(url).content
    # soup = bs(page)

f.close()