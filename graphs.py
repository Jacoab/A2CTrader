import pandas as pd
import matplotlib.pyplot as plt


amd = pd.read_csv('amd-train.csv')
nvidia = pd.read_csv('nvda-train.csv')
ad_ap = pd.read_csv('amd-nvidia.csv')
print(ad_ap)

test = ad_ap[16:17]
range = ad_ap['ranges_per_trial']
print(range[16:17]['ranges_per_trial'])
#dates = amd[range[0], range[1]]
