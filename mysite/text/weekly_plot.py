import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']
import pandas as pd
import numpy as np

df = pd.read_excel('D:\\Jennifer\\RMA_FR\\Phase2_Keyword/keywords_results_0518.xlsx')
df['CreatedDate'] = pd.to_datetime(df['CreatedDate'], format='%Y-%m-%d %H:%M:%S')
df['week'] = df['CreatedDate'].dt.week
weekly_df = df.groupby(['Class', 'week']).size().rename('counts').reset_index()

plt.figure(figsize=(8, 4))
sns.lineplot(x="week", y="counts",
             hue="Class",
             data=weekly_df)

plt.xticks(np.arange(min(df['week']), max(df['week']) + 1, 1), fontsize=15)
plt.yticks(fontsize=15)
plt.xlabel('週別', fontsize=15)
plt.ylabel('數量', fontsize=15)
plt.title('week{} 至 week {} 各Class搜尋數量'.format(min(df['week']), max(df['week'])), fontsize=18)
plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., fontsize=15)
plt.show()