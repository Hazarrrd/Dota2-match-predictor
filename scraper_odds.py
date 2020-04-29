import pandas as pd
import re
import numpy as np

with open("data/orginal/odds.txt") as f:
    content = f.readlines()

with open('data/orginal/odds.txt', 'w') as f:
    for line in content:
        if not "2019" in line:
            f.write(line)

names_1 = []
names_2 = []
odd_1 = []
odd_2 = []
winner = []
for row_nr in range(0, len(content), 4):
    names = re.search("\\t.*\\t", content[row_nr]).group(0)[1:-1].split(" - ")
    names_1.append(names[0])
    names_2.append(names[1])
    odd_1.append(content[row_nr + 1].rstrip())
    odd_2.append(content[row_nr + 2].rstrip())
    match_results = content[row_nr][-4:-1].split(":")
    if match_results[0] > match_results[1]:
        winner.append(1)
    elif match_results[1] > match_results[0]:
        winner.append(2)
    else:
        winner.append(0)

pd.DataFrame(np.transpose([names_1, names_2, odd_1, odd_2, winner])).to_csv("data/generated/odds.csv")
