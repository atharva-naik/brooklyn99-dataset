import os
import re
import json
import tqdm
import parse
import requests 
import warnings
import threading
from tqdm import tqdm
from parse import parse
from threading import Thread
from bs4 import BeautifulSoup as bs

warnings.filterwarnings("ignore")
NUM_THREADS=8

def get_episodes(base_url):
    page = requests.get(base_url).content
    soup = bs(page)
    seasons = soup.findAll("div",{'class':'series_seasons'})[0]
    return [episode.attrs['href'] for episode in seasons.findAll("a")]

def clean(text):
    text = text.replace('<div class="full-script"',"")
    text = text.replace("</div>","")
    text = text.replace("<br/>","\n")
    text = re.sub('<script.*</script>', '', text)
    text = re.sub('\(.*', '', text)
    text = re.sub('.*\)', '', text)
    text = re.sub('\(.*\)', '', text)
    text = re.sub('<!--.*-->', '', text)
    text = re.sub('<script>', '', text)
    text = re.sub('</script>', '', text)
    text = re.sub('<ins.*</ins>', '', text)
    text = re.sub('\(adsbygoogle.*\);', '', text)
    # text = re.sub('<script>\n     \(adsbygoogle = window.adsbygoogle \|\| \[]\).push\(\{}\);\n</script>','', text)

    return text

def dump_episode(episode):
    dialogues=[]
    url = f"https://subslikescript.com{episode}"
    season, ep = parse("/series/Brooklyn_Nine-Nine-2467372/{}/{}", episode)
    
    try:
        os.mkdir(f"dataset/{season}")
        os.mkdir(f"plain-text/{season}")
    except FileExistsError:
        pass

    page = requests.get(url).content
    soup = bs(page)
    script = str(soup.findAll("div", {"class":"full-script"})[0])
    script = clean(script)
    
    for line in script.split('\n\n'):
        line = line.strip()
        line = ' '.join(line.split('\n'))
        if line != '':
            dialogues.append(line)
    json.dump(dialogues, open(f"dataset/{season}/{ep}.json", "w"))

    g = open(f"plain-text/{season}/{ep}.txt", "w")
    g.write(script)
    g.close()

def dump_episodes(episodes):
    for episode in tqdm(episodes): dump_episode(episode)

# getting the episode urls from the homepage
episodes = get_episodes("https://subslikescript.com/series/Brooklyn_Nine-Nine-2467372")

try:
    os.mkdir('plain-text')
    os.mkdir('dataset')
except FileExistsError:
    pass

GRP_SIZE=int(len(episodes)/NUM_THREADS)
groups=[]
for i in range(NUM_THREADS):
    groups.append(episodes[i*GRP_SIZE:(i+1)*GRP_SIZE])
# groups[-1]=episodes()
groups[-1]=episodes[i*GRP_SIZE:]
# sanity check, so that no episode is missed out
print(sum([len(i) for i in groups]))

f=open("scraped-episodes.txt","w")
for episode in episodes:
    url = f"https://subslikescript.com{episode}"
    f.write(url+'\n')
f.close()

threads=[]
for group in groups:
    threads.append(Thread(target=dump_episodes, args=(group,)))
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()