import pandas as pd
import matplotlib.pyplot as plt


amd = pd.read_csv('amd-train.csv')
nvidia = pd.read_csv('nvda-train.csv')
ad_ap = pd.read_csv('amd-nvidia.csv')
print(ad_ap)

ad_ap[16:17]
