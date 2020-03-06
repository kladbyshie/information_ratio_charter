import pandas_datareader as dr
import pandas as pd
import numpy as np
from bokeh.plotting import figure, output_file, show
from bokeh.models import ColumnDataSource, LabelSet, HoverTool

#The following values can be changed in order to adjust what stocks/what dates are sourced; S&P500 is always sourced
stocks=['FB','AAPL','GOOGL','MSFT']
startdate='2019/01/01'
enddate='2020/01/01'

#formulas that pull stocks and S&P500 from yahoo for given dates; note, runs slow (year worth of data for 4 stocks and 1 index)
def form(startdate,enddate):
    return(dr.DataReader(stocks,'yahoo',startdate,enddate)['Close'])

def sp500(startdate,enddate):
    return(dr.DataReader("^GSPC",'yahoo',startdate,enddate))

for item in stocks:
    results=form(startdate,enddate)
    
sp500=sp500(startdate,enddate)

#accounts for count of dates selected in annual calculation
num=len(results.index)
annual_info_ratio=np.sqrt(num)

#creates blank df and df2 dataframes with 'Value' placeholder index
placeholder=['Value']
df=pd.DataFrame(index=placeholder)
df2=pd.DataFrame(index=placeholder)

#populates df and df2 (which stores annual sharpe ratio values)
sp500['Percent Change']=sp500['Close'].pct_change()
for item in stocks:
    results[f'{item} Percent Change']=results[item].pct_change()
    results[f'{item} excess'] = results[f'{item} Percent Change'] - sp500['Percent Change']

for item in stocks:
    df[f'{item} avg_excess'] = results[f'{item} excess'].mean()
    df[f'{item} sd_excess'] = results[f'{item} excess'].std()
    df[f'{item} daily_info_ratio']=df[f'{item} avg_excess'] / df[f'{item} sd_excess']
    df2[item]=df[f'{item} daily_info_ratio']*annual_info_ratio

#makes df2 usable for Bokeh
df2=df2.transpose()
#creates a rounded dataframe (to 4 decimal values) for the labels
df3=round(df2,4)

#generates bar graph, hover tools, and labels
source = ColumnDataSource(data=dict(df2=df2['Value'],
                                   stocks=stocks,
                                   df3=df3['Value']))

f = figure(x_range=stocks, title="Information Ratios", toolbar_location='above', plot_width=400,plot_height=400)

f.vbar(x='stocks',width=0.5,bottom=0,top='df2', color="firebrick",source=source)

labels = LabelSet(x='stocks', y='df2', text='df3', level='glyph',
        x_offset=-23, y_offset=0, source=source, render_mode='canvas')

hover=HoverTool(tooltips=[("Stock Name: ","@stocks"),("Information Ratio: ","@df2")])
f.add_tools(hover) 
f.add_layout(labels)

show(f)
