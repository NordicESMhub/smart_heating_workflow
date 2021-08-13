"""Python program to plot the temperature to prescribe to the 
   central heating system. These temperatures are in degrees 
   celcius and derived from meteorological forecasts.
"""

import pandas as pd
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, DatetimeTickFormatter
from bokeh.models.tools import HoverTool
import click


@click.command()
@click.option("--in-file", required=True, help="input file name with time and temperatures in Celcius (tabular).")
@click.option("--out-file", required=True, help="HTML output file to store the plot")
def main(in_file, out_file):
       
    df = pd.read_csv(in_file, sep='\t', index_col='time', parse_dates=True,
                     infer_datetime_format=True)
    output_file(out_file)
    source = ColumnDataSource(df)
    
    p = figure(x_axis_type="datetime", plot_width=800, plot_height=400)
    p.line(x='time', y='temperature_heating',
           line_width=3,
           source=source, color='darkblue')
    p.title.text = 'Temperature to prescribe to the heater (computed from HIRLAM forecasts)'
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Temperature in the tank (degrees)'
    p.xaxis.formatter=DatetimeTickFormatter(
        hours=["%d %B %Y (%H h)"],
        days=["%d %B %Y  (%H h)"],
        months=["%d %B %Y (%H h)"],
        years=["%d %B %Y (%H h)"],
    )
    
    hover = HoverTool()
    hover.tooltips = [
        ('Date', "@time{%d %B %Y %H:%M:%S}"),
        ('Temperature', '@temperature_heating'),
    ]
    hover.formatters = {"@time": "datetime"}
    p.add_tools(hover)
    show(p)


if __name__ == "__main__":
    main()