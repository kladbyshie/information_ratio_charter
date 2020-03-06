# Information Ratio Charter

"The information ratio (IR) is a measurement of portfolio returns beyond the returns of a benchmark, usually an index, compared to the volatility of those returns. The benchmark used is typically an index that represents the market or a particular sector or industry." - Investopedia

This proof-of-concept code will acquire the close for the stocks and dates selected (along with an S&P500 benchmark), run calculations, and then present the information ratios in a bar graph using Bokeh. It is essentially a Sharpe-ratio, using an S&P500 benchmark rather than T-bills.

The code features the following:
* Pandas_datareader, used for sourcing the stock and S&P500 information for the selected dates from Yahoo Finance
* Bokeh, used for visualizing the information processed using a bar chart (includes labels and a hover-tool implementation)
* Scalability; the code can accomodate several tickers (using several for loops and string formatting), and can scale to suit these. The code will also accomodate different time spans (ie. the annual 


Room for growth:
* Bokeh labels seem to be a bit busted, especially since the positioning is tied to the height. If the stock underperforms and has a negative info ratio, the label will be hidden. 
* The code is slow when there are a large amount of stocks being passed. The limitation lies in the pandas_datareader; using a pre-cached CSV from earlier (or potentially a wholly different source) should let it run faster.
* Importing the T-Bill rate (based on the time period selected) would make this a Sharpe Ratio Charter. However, I couldn't find a clean method for importing these (maybe some sort of data scraping module in the future?).
