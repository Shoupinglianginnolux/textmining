from datetime import date
import xlsxwriter

workbook = xlsxwriter.Workbook('chart_date_axis.xlsx')

worksheet = workbook.add_worksheet()
chart = workbook.add_chart({'type': 'line'})
date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})

# Widen the first column to display the dates.
worksheet.set_column('A:A', 12)

# Some data to be plotted in the worksheet.
dates = [date(2013, 1, 1),
         date(2013, 1, 2),
         date(2013, 1, 3),
         date(2013, 1, 4),
         date(2013, 1, 5),
         date(2013, 1, 6),
         date(2013, 1, 7),
         date(2013, 1, 8),
         date(2013, 1, 9),
         date(2013, 1, 10),
         date(2013, 1, 11),
         date(2013, 1, 12),
         date(2013, 1, 13),
         date(2013, 1, 14),
         date(2013, 1, 15),
         date(2013, 1, 16),
         date(2013, 1, 17),
         date(2013, 1, 18),
         date(2013, 1, 19),
         date(2013, 1, 20)]

values = [10, 30, 20, 40, 20, 60, 50, 40, 30, 30,10, 30, 20, 40, 20, 60, 50, 40, 30, 30]

# Write the date to the worksheet.
worksheet.write_column('A1', dates, date_format)
worksheet.write_column('B1', values)

# Add a series to the chart.
chart.add_series({
    'categories': '=Sheet1!$A$1:$A$10',
    'values': '=Sheet1!$B$1:$B$10',
})

# Configure the X axis as a Date axis and set the max and min limits.
chart.set_x_axis({
    'date_axis': True,
    'minor_unit':      4,
    'minor_unit_type': 'months',
    'major_unit':      1,
    'major_unit_type': 'years',
    'num_format':      'dd/mm/yyyy',
})

# Turn off the legend.
chart.set_legend({'none': True})

# Insert the chart into the worksheet.
worksheet.insert_chart('D2', chart)

workbook.close()