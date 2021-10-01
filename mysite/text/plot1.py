import seaborn as sns
import matplotlib.pyplot as plt, mpld3; 
plt.rcParams['font.sans-serif'] = ['Microsoft JhengHei']

import numpy as np
import pandas as pd

def plot1():
    df = pd.read_excel('D:\keywords_results_20200518.xlsx')
    df['CreatedDate'] = pd.to_datetime(df['CreatedDate'], format='%Y-%m-%d %H:%M:%S')
    df['week'] = df['CreatedDate'].dt.week
    weekly_df = df.groupby(['Class', 'week']).size().rename('counts').reset_index()
    print(weekly_df)

    # to draw the graph in html
    # fig, ax = plt.subplots(figsize=(3,3))
    # fig, ax = plt.subplots(figsize=(3,3))

    # if I just need to plot the graph out(param: figsize=(8, 4))
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
    plt.savefig('mysite/static/text/keyword_search_by_week.png')

    # g = mpld3.fig_to_html(fig)

    # return g

# Some sample data to plot.
# list_data = [10, 20, 30, 20, 15, 30, 45]

# Create a Pandas dataframe from the data.
# df = pd.DataFrame(list_data)

# Create a Pandas Excel writer using XlsxWriter as the engine.
# excel_file = 'line.xlsx'
# sheet_name = 'Sheet1'

# writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
# weekly_df.to_excel(writer, sheet_name=sheet_name)

# Access the XlsxWriter workbook and worksheet objects from the dataframe.
# workbook = writer.book
# worksheet = writer.sheets[sheet_name]

# Create a chart object.
# chart = workbook.add_chart({'type': 'line'})

# Configure the series of the chart from the dataframe data.
# cat_1 = ['y1', 'y2', 'y3', 'y4']

# Configure the series of the chart from the dataframe data.
# for i in range(len(cat_1)):
#     col = i + 1
#     chart.add_series({
#         'name':       ['Sheet1', 0, col],
#         'categories': ['Sheet1', 1, 0, 21, 0],
#         'values':     ['Sheet1', 1, col, 21, col],
#     })

# # Configure the chart axes.
# chart.set_x_axis({'name': '週別', 'position_axis': 'on_tick'})
# chart.set_y_axis({'name': '數量', 'major_gridlines': {'visible': False}})

# # Turn off chart legend. It is on by default in Excel.
# # chart.set_legend({'position': 'none'})

# # Insert the chart into the worksheet.
# worksheet.insert_chart('D2', chart)

# # Close the Pandas Excel writer and output the Excel file.
# writer.save()

if __name__ == '__main__':
    plot1()