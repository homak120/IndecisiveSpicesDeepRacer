import pandas as pd
import matplotlib.pyplot as plt

# change me to data csv filename. Uses evaluation data not training data.
version = 'v12'

data = pd.read_csv(f"data/{version}.csv", index_col=1)

ax = data[data['episode'] == 0].plot(x='X', y='Y')
data[data['episode'] == 1].plot(x='X', y='Y', ax=ax)
data[data['episode'] == 2].plot(x='X', y='Y', ax=ax)

plt.savefig(f"charts/{version}path.png")
