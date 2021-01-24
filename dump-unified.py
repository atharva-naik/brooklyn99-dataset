import os
import json

ROOT='dataset'
all_dialogues=[]
for season in os.listdir(ROOT):
    season = os.path.join(ROOT, season)
    for file in os.listdir(season):
        file=os.path.join(season, file)
        dialogues=json.load(open(file, "r"))
        all_dialogues+=dialogues
print(len(all_dialogues))
json.dump(all_dialogues, open("unified-dump.json", "w"))