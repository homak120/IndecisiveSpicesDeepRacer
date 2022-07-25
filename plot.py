import pandas as pd
import matplotlib.pyplot as plt

version='v7'

data = pd.read_csv(f"data/{version}.csv", index_col=1)

ax=data[data['episode']==0][['reward']].plot()
ax = data[data['episode']==1][['reward']].plot(ax=ax)
data[data['episode']==2][['reward']].plot(ax=ax)

plt.savefig(f"charts/{version}.png")