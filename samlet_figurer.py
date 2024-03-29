# -*- coding: utf-8 -*-
"""Samlet_Figurer.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1sbRpLr03APo_aTwK8xMmub1VmL-JFbAm

**Analysis of Request For Quote (RFQ) data for customer Mitsubishi and Lazard** \
Data is obtained from the blotter function (BLT) in BB.
"""

pip install plotly==4.7.1

rfq = pd.read_csv('https://raw.githubusercontent.com/LarsBryld/auctions/master/rfqbbg2020.csv', sep=',', parse_dates=True, dayfirst=False, skiprows=2)

rfq.head(5)

# Import of the .csv file contaning RFQ data. 

import pandas as pd
import numpy as np


rfq = pd.read_csv('https://raw.githubusercontent.com/LarsBryld/auctions/master/rfqbbg2020.csv', sep=',', parse_dates=True, dayfirst=False, skiprows=2)

# Creating 
rfq['Second'] = pd.DatetimeIndex(rfq['Exec Time']).second
rfq['Minute'] = pd.DatetimeIndex(rfq['Exec Time']).minute
rfq['Hour'] = pd.DatetimeIndex(rfq['Exec Time']).hour
rfq['Day'] = pd.DatetimeIndex(rfq['Trade Dt']).day
rfq['Month'] = pd.DatetimeIndex(rfq['Trade Dt']).month
rfq['Year'] = pd.DatetimeIndex(rfq['Trade Dt']).year  
rfq['Source'] = 'RFQ'

# Creating date variable used for plotting
rfq['Date'] = pd.to_datetime(rfq['Trade Dt'], format='%d/%m/%Y')
rfq['WeekDay'] = rfq['Date'].dt.day_name()
rfq['MonthName'] = rfq['Date'].dt.month_name()

#Calculating days to maturity and rounding result 
#rfq['Maturity'] = (pd.to_datetime(rfq['Mat Dt'], format='%d/%m/%Y') - rfq['Date']) / np.timedelta64(1,'D') / 365
#rfq['Maturity'] = rfq['Maturity'].round(1)

import datetime as dt
#rfq['Maturity'] = rfq['Mat Dt'] - rfq['Date']
#rfq['Maturity'] = rfq['Mat Dt'] - rfq['Date']


rfq['Maturity'] = (pd.to_datetime(rfq['Mat Dt'],errors = 'coerce', format='%d/%m/%Y') - pd.to_datetime(rfq['Date'],errors = 'coerce', format='%d/%m/%Y')) / np.timedelta64(1,'D') /365
rfq['Maturity'] = rfq['Maturity'].round(1)


import plotly.express as px

import plotly.io as pio
pio.renderers.default = 'colab'

#import plotly.graph_objects as go
#fig = go.Figure(data=go.Bar(y=[2, 3, 1]))
#fig.show()


#Create inverted price measure 
rfq.loc[rfq['Side'] == 'B', 'PriceDiff'] = (rfq['CBBT Mid Prc'] - rfq['Price']) 
rfq.loc[rfq['Side'] == 'S', 'PriceDiff'] = (rfq['Price'] - rfq['CBBT Mid Prc'])


# Create inverted price dummy 
rfq.loc[rfq['PriceDiff'] < 0, 'PriceDiffDummy'] = 'Inverted'
rfq.loc[rfq['PriceDiff'] > 0, 'PriceDiffDummy'] = 'Non-Inverted'
rfq.loc[rfq['PriceDiff'] == 0, 'PriceDiffDummy'] = 'Non-Inverted'


# away from mid volume  
rfq.loc[rfq['PriceDiffDummy'] == 1, 'VolumenAwayFromMid'] = (rfq['Quantity'] * rfq['PriceDiff'] * 1)
rfq.loc[rfq['PriceDiffDummy'] == 0, 'VolumenAwayFromMid'] = (rfq['Quantity'] * rfq['PriceDiff'] * 1)

rfq.loc[rfq['Status'].isin(['AllocSent', 'Accepted', 'AllocSave', 'AllocAcpt']), 'Status2'] = ('Accepted')
rfq.loc[rfq['Status'].isin(['Tie-TW', 'Covered']), 'Status2'] = ('Covered')
rfq.loc[rfq['Status'].isin(['TrAway', 'Passed', 'C/Expire', 'D/Expire', 'Rejected', 'Corrected', 'Cancel', 'C/Cancel', 'AllocCanc']), 'Status2'] = ('TrAway')

pd.DataFrame(rfq)
rfq.head(5)

# Checking for nan and null in response time, quantity and inverted prices variable
null_rows_q = rfq[rfq['Quantity'].isnull()]
nan_rows_q = rfq[rfq['Quantity'].isna()]

null_rows_rs = rfq[rfq['Rspns Time MS'].isnull()]
nan_rows_rs = rfq[rfq['Rspns Time MS'].isna()]

#null_rows_inv = rfq[rfq['Inverted 0/1'].isnull()]
#nan_rows_inv = rfq[rfq['Inverted 0/1'].isna()]


print('Number of isnull & is na observation in "Quantity" is {} & {} respectivly. '.format(len(null_rows_q), len(nan_rows_q)))
print('Number of isnull & is na observation in "Response Time" is {} & {} respectivly. '.format(len(null_rows_rs), len(nan_rows_rs)))
#print('Number of isnull & is na observation in "Inverted Price" variable is {} & {} respectivly. '.format(len(null_rows_inv), len(nan_rows_inv)))



#
print('Total number of rows with TS Book Name = Depo is {}'.format(len(rfq[rfq['TS Book Name'] == 'DEPO'])))
#print('Unique books in RFQ data {}'.format(pd.unique(rfq['TS Book Name'])))

# Removing Depo book from the RFQ data set since it creates issues with Nan & Null
rfq = rfq[rfq['TS Book Name'].isin(['STAT', 'FLEX', 'REAL', 'ILLIKVID', 'FLOAT', 'INFLATIO'])]

# Checking for nan and null in response time, quantity and inverted prices variable
null_rows_q = rfq[rfq['Quantity'].isnull()]
nan_rows_q = rfq[rfq['Quantity'].isna()]

null_rows_rs = rfq[rfq['Rspns Time MS'].isnull()]
nan_rows_rs = rfq[rfq['Rspns Time MS'].isna()]

#null_rows_inv = rfq[rfq['Inverted 0/1'].isnull()]
#nan_rows_inv = rfq[rfq['Inverted 0/1'].isna()]



print('Number of isnull & is na observation in "Quantity" is {} & {} respectivly after removing Depo book. '.format(len(null_rows_q), len(nan_rows_q)))
print('Number of isnull & is na observation in "Response Time" is {} & {} respectivly after removing Depo book. '.format(len(null_rows_rs), len(nan_rows_rs)))
#print('Number of isnull & is na observation in "Inverted Price" variable is {} & {} respectivly after removing Depo book. '.format(len(null_rows_inv), len(nan_rows_inv)))

print('{} Perp observations has to be removed with Maturity > 100 '.format(len(rfq[rfq['Maturity'] > 100])))
print('{} observations has to be removed with Yield > 100 '.format(len(rfq[rfq['Yield'] > 100])))

#removing Perp bonds from Data set
rfq = rfq[rfq['Maturity'] < 100]

#removing Perp bonds from Data set
rfq = rfq[rfq['Yield'] < 100 ]

#removing bonds from Data set with price > 200 
rfq = rfq[rfq['Price'] < 200 ]

rfq = rfq[rfq['PriceDiff'] < 9 ]


#Reducing the rfq df to be of one year dimension
#rfq = rfq[rfq['Date']> np.max(rfq['Date']) - pd.DateOffset(years=1)]
#print('Latest date in main RFQ data set is {:%d-%b-%Y}. Earliest date is {:%d-%b-%Y}'.format(np.max(rfq['Date']), np.min(rfq['Date'])))


#changing nan in dls comp to zeros
#rfq['DlrsCmp'].fillna(0, inplace=True)

real = rfq[rfq['TS Book Name'] == 'REAL']

rfq.head(3)

"""**Selecting one year of data**



"""

print('Latest date in main RFQ data set is: {:%d-%b-%Y}. Earliest date is {:%d-%b-%Y}. Latest data minus one year is {:%d-%b-%Y}'.format(max(rfq['Date']), min(rfq['Date']), max(rfq['Date']) - pd.DateOffset(years=1) ))

#Reducing the data set to only include customer of interest 
#rfq.mitsubishi = rfq[rfq['Customer'] == 'MITSUBISHI UFJ KOKU AST MGT CO LTD']
#rfq.lazard = rfq[rfq['Customer'] == 'LAZARD ASSET MANAGEMENT']


#Creating two main df's (lazard & mitsubishi) for one year data for cust and product of interest
#lazard = rfq.lazard[rfq.lazard['TS Book Name'] == 'REAL']
#print('Latest date in {} df is {:%d-%b-%Y}. Earliest date is {:%d-%b-%Y} for trades on {} book'.format(pd.unique(lazard['Customer']), max(lazard['Date']), min(lazard['Date']), pd.unique(lazard['TS Book Name'])))


#mitsubishi = rfq.mitsubishi[rfq.mitsubishi['TS Book Name'] == 'REAL']
#print('Latest date in {} df is {:%d-%b-%Y}. Earliest date is {:%d-%b-%Y} for trades on {} book'.format(pd.unique(mitsubishi['Customer']),max(mitsubishi['Date']), min(mitsubishi['Date']), pd.unique(mitsubishi['TS Book Name'])))


#print(len(pd.unique(rfq['Date'])))

pd.unique(rfq['Customer'])

#Creating descriptive df's which can be skippede

#lsr = rfq.lazard[(rfq.lazard['TS Book Name'] == 'REAL') & (rfq.lazard['Side'] == '[B]')]
#lbr = rfq.lazard[(rfq.lazard['TS Book Name'] == 'REAL') & (rfq.lazard['Side'] == '[S]')]
#lss = rfq.lazard[(rfq.lazard['TS Book Name'] == 'STAT') & (rfq.lazard['Side'] == '[B]')]
#lbs = rfq.lazard[(rfq.lazard['TS Book Name'] == 'STAT') & (rfq.lazard['Side'] == '[S]')]
#lsi = rfq.lazard[(rfq.lazard['TS Book Name'] == 'ILLIKVID') & (rfq.lazard['Side'] == '[B]')]
#lbi = rfq.lazard[(rfq.lazard['TS Book Name'] == 'ILLIKVID') & (rfq.lazard['Side'] == '[S]')]
#lsf = rfq.lazard[(rfq.lazard['TS Book Name'] == 'FLEX') & (rfq.lazard['Side'] == '[B]')]
#lbf = rfq.lazard[(rfq.lazard['TS Book Name'] == 'FLEX') & (rfq.lazard['Side'] == '[S]')]


#msr = rfq.mitsubishi[(rfq.mitsubishi['TS Book Name'] == 'REAL') & (rfq.mitsubishi['Side'] == '[B]')]
#mbr = rfq.mitsubishi[(rfq.mitsubishi['TS Book Name'] == 'REAL') & (rfq.mitsubishi['Side'] == '[S]')]
#mss = rfq.mitsubishi[(rfq.mitsubishi['TS Book Name'] == 'STAT') & (rfq.mitsubishi['Side'] == '[B]')]
#mbs = rfq.mitsubishi[(rfq.mitsubishi['TS Book Name'] == 'STAT') & (rfq.mitsubishi['Side'] == '[S]')]
#msi = rfq.mitsubishi[(rfq.mitsubishi['TS Book Name'] == 'ILLIKVID') & (rfq.mitsubishi['Side'] == '[B]')]
#mbi = rfq.mitsubishi[(rfq.mitsubishi['TS Book Name'] == 'ILLIKVID') & (rfq.mitsubishi['Side'] == '[S]')]

#Descriptive printing. Can be skipped  

#print('Earliest TradeDate for Lazard accross all books are {:%d-%b-%Y} and latest {:%d-%b-%Y}.'.format(min(rfq.lazard['Date']), max(rfq.lazard['Date'])))
#print('Within the latest year:')

#print(' ')

#print('Lazard trades {} unique securities on {} unique books: ({}).'.format(len(pd.unique(rfq.lazard['Security'])), len(pd.unique(rfq.lazard['TS Book Name'])), pd.unique(rfq.lazard['TS Book Name'])))
#print('Lazard is net buyer of {:,.0f} DKK on STAT Book. Buys {:,.0f} DKK of {} unique ISIN and sells {:,.0f} DKK of {} unique ISIN.'.format((sum(lbs['Quantity'])-sum(lss['Quantity'])), sum(lbs['Quantity']), len(pd.unique(lbs['Security'])), sum(lss['Quantity']), len(pd.unique(lss['Security']))))
#print('Lazard is net buyer of {:,.0f} DKK on {} book. Buys {:,.0f} DKK of {} unique ISIN and sells {:,.0f} DKK of {} unique ISIN.'.format((sum(lbr['Quantity'])-sum(lsr['Quantity'])), pd.unique(lazard['TS Book Name']),sum(lbr['Quantity']), len(pd.unique(lbr['Security'])), sum(lsr['Quantity']), len(pd.unique(lsr['Security']))))
#print('Lazard is net buyer of {:,.0f} DKK on ILLIKVID Book. Buys {:,.0f} DKK of {} unique ISIN and sells {:,.0f} DKK of {} unique ISIN.'.format((sum(lbi['Quantity'])-sum(lsi['Quantity'])), sum(lbi['Quantity']), len(pd.unique(lbi['Security'])), sum(lsi['Quantity']), len(pd.unique(lsi['Security']))))
#print('Lazard is net buyer of {:,.0f} DKK on FLEX Book. Buys {:,.0f} DKK of {} unique ISIN and sells {:,.0f} DKK of {} unique ISIN.'.format((sum(lbf['Quantity'])-sum(lsf['Quantity'])), sum(lbf['Quantity']), len(pd.unique(lbf['Security'])), sum(lsf['Quantity']), len(pd.unique(lsf['Security']))))

#print(' ')


#print('Earliest TradeDate for Mitsubishi across all books are {:%d-%b-%Y} and latest {:%d-%b-%Y}'.format(min(mitsubishi['Date']), max(mitsubishi['Date'])))

#print(' ')

#print('Mitsubishi trades {} unique securities on {} unique books: ({}).'.format(len(pd.unique(rfq.mitsubishi['Security'])), len(pd.unique(rfq.mitsubishi['TS Book Name'])), pd.unique(rfq.mitsubishi['TS Book Name'])))
#print('Mitsubishi is net buyer of {:,.0f} DKK on REAL Book. Buys {:,.0f} DKK of {} unique ISIN and sells {:,.0f} DKK of {} unique ISIN.'.format((sum(mbr['Quantity'])-sum(msr['Quantity'])), sum(mbr['Quantity']), len(pd.unique(mbr['Security'])), sum(msr['Quantity']), len(pd.unique(msr['Security']))))
#print('Mitsubishi is net buyer of {:,.0f} DKK on ILLIKVID Book. Buys {:,.0f} DKK of {} unique ISIN and sells {:,.0f} DKK of {} unique ISIN.'.format((sum(mbi['Quantity'])-sum(msi['Quantity'])), sum(mbi['Quantity']), len(pd.unique(mbi['Security'])), sum(msi['Quantity']), len(pd.unique(msi['Security']))))
#print('Mitsubishi is net buyer of {:,.0f} DKK on STAT Book. Buys {:,.0f} DKK of {} unique ISIN and sells {:,.0f} DKK of {} unique ISIN.'.format((sum(mbs['Quantity'])-sum(mss['Quantity'])), sum(mbs['Quantity']), len(pd.unique(mbs['Security'])), sum(mss['Quantity']), len(pd.unique(mss['Security']))))

#lazard_s = lazard[rfq.lazard['Side'] == '[B]']
#lazard_b = lazard[rfq.lazard['Side'] == '[S]']
#lazard_buy = rfq.lazard[rfq.lazard['Side'] == ['S']]


#print('Lazard is net seller of {:,.0f} DKK on FLEX Book. Sells {:,.0f} DKK of {} unique ISIN and buys {:,.0f} DKK of {} unique ISIN.'.format((sum(lazard_s['Quantity'])-sum(lazard_b['Quantity'])), sum(lazard_s['Quantity']), len(pd.unique(lazard_s['Security'])), sum(lazard_b['Quantity']), len(pd.unique(lazard_b['Security']))))

"""**Plotting**


Note the figures represent data viewed from Nykredits' side. Hence Side=['S'] means customer bought and Nykredit sold.

 The two df consists of:


*   Data witin the latest year. 06-Oct-2019 until 06-Oct-2020 (both days included) 
*   Data from the Bloomberg book 'REAL' (TS Book Name = REAL)


"""

#fig = px.bar(real, x="Side", y="Quantity", color="Status", title="Total (Buy vs Sell)", color_discrete_sequence=["red", "green", "yellow", "red", "red", "green", "red", "yellow", "red", "green", "green", "red", "red", "red"])
#fig.update_yaxes(tick0=1, range=[0, 7000000000],dtick=1000000000)


#fig.show()

#based on the above Danske, Pimco, SEB, Lazard, Mitsubishi and W&W are chosen as peer group analysis  

#real = real[real['Customer'].isin(['DANSKE BANK A/S', 'PIMCO DEUTSCHLAND GMBH', 'SEB ASSET MANAGEMENT', 'LAZARD ASSET MANAGEMENT', 'MITSUBISHI UFJ KOKU AST MGT CO LTD', 'NORDEA INVESTMENT MANAGEMENT AB'])]


pd.unique(rfq['Customer'])

fig = px.bar(real, x="Side", y="Quantity", color="Status", title="Total (Buy vs Sell)", color_discrete_sequence=["yellow", "green", "red", "red", "red", "yellow", "green", "red", "green", "red"], facet_col="Customer", facet_col_wrap=6)
fig.show()



"""**When do the customer trade during the day?**"""

lazard = rfq[rfq['Customer'] == 'LAZARD ASSET MANAGEMENT']

fig = px.bar(lazard, x="Hour", y="Quantity", color="Status", title="Hour of Day <br>RFQ's from AP PENSIONSSERVICE A/S <br> ",
             color_discrete_sequence=["yellow", "red", "green", "green"])
fig.update_xaxes(range=[8, 18] ,dtick=1)

fig.show()



real.ww = real[real['Customer'] == 'W&W ASSET MANAGEMENT GMBH']

fig = px.bar(real.ww, x="Hour", y="Quantity", color="Side", title="Hour of Day <br>RFQ's from W&W ASSET MANAGEMENT <br> ")
fig.update_xaxes(range=[8, 18] ,dtick=1)

fig.show()

fig = px.bar(real, x="Hour", y="Quantity", color="Side", title="RFQ (Hour of Day)")
fig.update_yaxes(tick0=1, range=[0, 20000000000],dtick=1000000000)
fig.update_xaxes(rangeslider_visible=True)

fig.show()

# Mitsubish

"""**When do the customer trade during the week?**"""

mix = real[real['Customer'].isin(['W&W ASSET MANAGEMENT GMBH', 'MITSUBISHI UFJ KOKU AST MGT CO LTD'])]


fig = px.bar(mix, x="WeekDay", y="Quantity", color="Side", title="Day of Week <br>RFQ's from W&W ASSET MANAGEMENT", facet_col="Customer", facet_col_wrap=6,)
fig.update_xaxes(categoryorder='array')
fig.update_xaxes(categoryarray= ['Monday','Tuesday','Wednesday','Thursday', 'Friday', 'December'])
#fig.update_yaxes(tick0=1, range=[0, 3500000000],dtick=500000000)
fig.show()

fig = px.bar(ap, x="WeekDay", y="Quantity", color="Status", title="Day of Week <br>RFQ's from AP's Pension", facet_col="Customer", facet_col_wrap=6, color_discrete_sequence=["yellow", "red", "green", "green"])
fig.update_xaxes(categoryorder='array')
fig.update_xaxes(categoryarray= ['Monday','Tuesday','Wednesday','Thursday', 'Friday', 'December'])
#fig.update_yaxes(tick0=1, range=[0, 3500000000],dtick=500000000)
fig.show()

"""**When do the customer trade during the year**"""

real.mit = real[real['Customer'] == 'MITSUBISHI UFJ KOKU AST MGT CO LTD']


fig = px.bar(real.mit, x="MonthName", y="Quantity", color="Side", title=" Month of Year <br>RFQ's from MITSUBISHI ", facet_col="Customer", facet_col_wrap=6)
fig.update_xaxes(categoryorder='array', categoryarray= ['January','February','March','April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
#fig.update_yaxes(tick0=1, range=[0, 2000000000],dtick=250000000)
fig.show()

fig = px.bar(ap, x="MonthName", y="Quantity", color="Status", title=" Month of Year <br>RFQ's from AP Pension ", facet_col="Customer", facet_col_wrap=6, color_discrete_sequence=["yellow", "red", "green", "green"])
fig.update_xaxes(categoryorder='array', categoryarray= ['January','February','March','April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
#fig.update_yaxes(tick0=1, range=[0, 2000000000],dtick=250000000)
fig.show()

fig = px.bar(real, x="Security", y="Quantity", color="Side", title="RFQ (Security)")
fig.show()

fig = px.bar(ap, x="Security", y="Quantity", color="Status", hover_data=['Security'], title="RFQ (Security) AP Pension", color_discrete_sequence=["yellow", "red", "green", "green"])

fig.show()

#nordea = real[real['Customer'].isin(['NORDEA INVESTMENT MANAGEMENT AB'])]
#rfq_group = rfq.groupby(['Customer', 'TS Book Name']).sum('Quantity')
#group.sort_values('Quantity', ascending=False).head(2)

pd.set_option('display.max_rows', None)  # or 1000

fig = px.bar(real, x="Security", y="Quantity", color="Side", hover_data=['Security'], title="RFQ (Security)", facet_col="Customer", facet_col_wrap=6)
fig.show()

import plotly.figure_factory as ff

group_labels = pd.unique(real['Customer'])

group_labels

"""**How is the competition compared to maturity**"""

fig = px.scatter(real, x="Maturity", y="DlrsCmp", color="Side", size='Quantity',
                  hover_data=['Security', 'Customer', 'Price', 'Side'], title="RFQ (Comp vs Maturity)", facet_col="Customer", facet_col_wrap=6)

fig.update_yaxes(range=[0,8],tick0=0, dtick=1)


fig.show()

"""**How is the competition compared to size**"""

real.seb = real[real['Customer'] == 'SEB ASSET MANAGEMENT']



fig = px.scatter(real.seb, x="Quantity", y="DlrsCmp", color="Side", size = 'Quantity',
                 hover_data=['Security', 'Price','Side','Customer'], title="SEB Asset Management <br>Comp vs Quantity", facet_col="Customer", facet_col_wrap=6)

fig.update_xaxes(range=[0,170000000],tick0=0, dtick=10000000)
fig.update_yaxes(range=[-1,7],tick0=0, dtick=1)

fig.show()

fig = px.scatter(ap, x="Quantity", y="DlrsCmp", color="Status", size = 'Quantity',
                 hover_data=['Security', 'Price','Side','Customer'], title="AP Pension <br>Comp vs Quantity", facet_col="Customer", facet_col_wrap=6, color_discrete_sequence=["yellow", "red", "green", "green"])

fig.update_xaxes(range=[0,170000000],tick0=0, dtick=10000000)
fig.update_yaxes(range=[-1,7],tick0=0, dtick=1)

fig.show()

fig = px.scatter(real, x="Quantity", y="DlrsCmp", color="Side",
                 hover_data=['Security', 'Price','Side','Customer'], title="Real", facet_col="Customer", facet_col_wrap=6,
                 color_discrete_sequence=["green", "red", "yellow", "red", "yellow", "green", "red", "red", "red", "red", "green", "green"])

fig.update_yaxes(range=[0,8],tick0=0, dtick=1)

fig.show()

"""**Has the competition changed during the year**"""

#lazard.groupby(['MonthName'])
month_averages = [rfq.groupby(['MonthName']).aggregate({"DlrsCmp":np.mean})]
#mitsubishi.groupby(['MonthName', 'DlrsCmp']).max()

rfq.groupby(['MonthName'])['DlrsCmp'].mean().plot()

real.dab = real[real['Customer'] == 'DANSKE BANK A/S']

fig = px.box(lazard, x="MonthName", y="DlrsCmp", title="LAZARD ASSET MANAGEMENT <br>Dealers in competition pr. month", hover_data=rfq.groupby(['MonthName']).aggregate({"DlrsCmp":np.mean}), facet_col="Customer", facet_col_wrap=6)
fig.update_xaxes(categoryorder='array', categoryarray= ['January','February','March','April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
fig.update_yaxes(range=[0,6],tick0=0, dtick=1)

fig.show()

fig = px.box(ap, x="MonthName", y="DlrsCmp", title="AP Pension <br>Dealers in competition pr. month", hover_data=rfq.groupby(['MonthName']).aggregate({"DlrsCmp":np.mean}), facet_col="Customer", facet_col_wrap=6)
fig.update_xaxes(categoryorder='array', categoryarray= ['January','February','March','April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
fig.update_yaxes(range=[0,6],tick0=0, dtick=1)

fig.show()

print(pd.unique(real.dab['DlrsCmp']))
len(real.dab[~real.dab['DlrsCmp'].isin([1,2,3,4,5,6,])])

print(pd.unique(real.seb['DlrsCmp']))
len(real.seb[~real.seb['DlrsCmp'].isin([1,2,3,4,5,6,])])

"""**Yield compared to Buy/Sell**"""

fig = px.scatter(real, x="Yield", y="Side", color="Status", size='Quantity',
                 hover_data=['Security', 'Customer', 'Price','Side', 'DlrsCmp'], title="RFQ (Yield vs Side)", facet_col="Customer", facet_col_wrap=6,
                 color_discrete_sequence=["green", "red", "yellow", "red", "yellow", "green", "red", "red", "red", "red", "green", "green"])

#fig.update_yaxes(dtick=0.1)
fig.update_xaxes(showgrid=True, ticks="outside", tickson="boundaries", range=[-1,3], dtick=0.25)
fig.update_yaxes(showgrid=True, range=['[S]','[B]'], dtick=0)

fig.show()

"""**Is the distance to midprice differe compared to status**"""

fig = px.scatter(real, x="Quantity", y="DlrsCmp", color="Status", size='Quantity',
                 hover_data=['Security', 'Customer', 'Price','Side', 'DlrsCmp'], title="RFQ (Yield vs Side)", facet_col="Customer", facet_col_wrap=6,
                 color_discrete_sequence=["green", "red", "yellow", "red", "yellow", "green", "red", "red", "red", "red", "green", "green"])

#fig.update_yaxes(dtick=0.1)
fig.update_xaxes(showgrid=True, ticks="outside", tickson="boundaries", range=[-1,3], dtick=0.25)
fig.update_yaxes(showgrid=True, range=['[S]','[B]'], dtick=0)

fig.show()

fig = px.scatter(real, x="Status", y="PriceDiff", color="Status", hover_data=['Security', 'Price', 'CBBT Mid Prc', 'Customer', 'Price','Side', 'DlrsCmp'], title="(Quoted Price – CBT Mid). Price diff > 10 has been removed",
                  color_discrete_sequence=["green", "yellow", "yellow", "red", "yellow", "green", "red", "red", "red", "red", "green", "red"], facet_col="Customer", facet_col_wrap=6)
fig.update_xaxes(categoryorder='array', categoryarray= ['Accepted', 'AllocAcpt', 'AllocSent', 'Covered', 'Tie-TW', 'TrAway', 'C/Expire', 'D/Expire']
                 )
#rfq['CBTMidPrice'].fillna(0, inplace=False)
#color_discrete_sequence=["green", "green", "green", "yellow", "yellow", "red", "red", "red", "red", "red", "red"]

fig.show()

fig = px.box(real, x="Status", y="Rspns Time MS", color="Status", title="Lazard (Rspns Time MS)", facet_col="Customer", facet_col_wrap=6,
             color_discrete_sequence=["green", "yellow", "red", "red", "yellow", "green", "red", "red", "red", "red", "green", "red"])
fig.update_xaxes(categoryorder='array', categoryarray= ['Accepted', 'AllocAcpt', 'AllocSent', 'Covered', 'Tie-TW', 'TrAway', 'C/Expire', 'D/Expire'])
fig.update_yaxes(showgrid=True, ticks="outside", tickson="boundaries", range=[0,150000], dtick=10000)
fig.show()

#fig = px.box(rfq, x="Status", y="Rspns Time MS", hover_data=['Security','Customer', 'TS Book Name'], title="RFQ ")
#fig.update_xaxes(categoryorder='array', categoryarray= ['January','February','March','April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
#fig.update_yaxes(range=[0,5],tick0=0, dtick=1)
#fig.show()

#fig = px.box(rfq, x="TS Book Name", y="Rspns Time MS")
#fig.update_xaxes(categoryorder='array', categoryarray= ['January','February','March','April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
#fig.update_yaxes(range=[0,5],tick0=0, dtick=1)
#fig.show()

#fig = px.histogram(real, x = rfq['Rspns Time MS'], nbins=1000)
#fig.show()

#Creating the waiting time for customers

#real['QuotingTime'] = real['Exec Time'].astype('datetime64[ns]') - real['Time'].astype('datetime64[ms]')

#x = rfq['DIFF2']

#x.fillna(1)

#x.isnull().values.sum()
#len(y)

#x.fillna(100, inplace=True)
#x.isnull().values.sum()

#fig = px.histogram(real, x = real['QuotingTime'], nbins=100)
#fig.show()

#rfq['Exec Time']

rfq['ExecTime'] = pd.to_datetime(rfq['Exec Time']) 
rfq['AskTime'] = pd.to_datetime(rfq['Time'])
rfq['QuotingTime'] = (rfq['ExecTime'] - rfq['AskTime'])
 
rfq['QuotingTime'] = (rfq['QuotingTime'].dt.total_seconds()*1000)
rfq['WaitingTimeMS'] = rfq['QuotingTime'] - rfq['Rspns Time MS']

#real = rfq[real['WaitingTime'] > 0]

real.mix = real[real['Customer'].isin(['UBS ASSET MANAGEMENT SWITZERLAND AG', 'SEB ASSET MANAGEMENT'])]

fig = px.histogram(real.mix, x = 'WaitingTimeMS', color="Status", hover_data=['Security', 'Customer', 'Price','Side', 'DlrsCmp'], nbins=400, facet_col="Customer", facet_col_wrap=6,
                   title="Waiting Time Ms:<br>(Execution Time - RFQ Time) - Rspns Time <br>", 
                   color_discrete_sequence=["green", "yellow", "red", "red", "green", "red", "green", "red", "red", "yellow", "red", "red"])

fig.update_yaxes(showgrid=True, ticks="outside", tickson="boundaries", range=[0,80], dtick=10)

fig.add_shape(type="line",
    x0=4999, y0=0, x1=5000, y1=80, row=0 , col=1,
    line=dict(color="Black",width=1)
)

fig.add_shape(type="line",
    x0=9999, y0=0, x1=10000, y1=80, row=0 , col=1,
    line=dict(color="Black",width=1)
)

fig.add_shape(type="line",
    x0=19999, y0=0, x1=20000, y1=80, row=0 , col=1,
    line=dict(color="Black",width=1)
)

fig.add_shape(type="line",
    x0=4999, y0=0, x1=5000, y1=80, row=0 , col=2,
    line=dict(color="Black",width=1)
)

fig.add_shape(type="line",
    x0=9999, y0=0, x1=10000, y1=80, row=0 , col=2,
    line=dict(color="Black",width=1)
)

fig.add_shape(type="line",
    x0=19999, y0=0, x1=20000, y1=80, row=0 , col=2,
    line=dict(color="Black",width=1)
)



fig.show()

#fig = px.histogram(mit2, x = mit2['DIFF4'], nbins=100, marginal="box", color="Customer")

#rfq['Exec Time']

ap['ExecTime'] = pd.to_datetime(ap['Exec Time']) 
ap['AskTime'] = pd.to_datetime(ap['Time'])
ap['QuotingTime'] = (ap['ExecTime'] - ap['AskTime'])
 
ap['QuotingTime'] = (ap['QuotingTime'].dt.total_seconds()*1000)
ap['WaitingTimeMS'] = ap['QuotingTime'] - ap['Rspns Time MS']

fig = px.histogram(ap, x = 'WaitingTimeMS', color="Status", hover_data=['Security', 'Customer', 'Price','Side', 'DlrsCmp'], nbins=12, facet_col="Customer", facet_col_wrap=6,
                   title="Waiting Time Ms:<br>(Execution Time - RFQ Time) - Rspns Time <br>", 
                   color_discrete_sequence=["Yellow", "red", "green", "green"])

fig.add_shape(type="line",
    x0=9999, y0=0, x1=10000, y1=80, row=0 , col=1,
    line=dict(color="Black",width=1)
)

fig.add_shape(type="line",
    x0=4999, y0=0, x1=5000, y1=80, row=0 , col=1,
    line=dict(color="Black",width=1)
)

fig.update_yaxes(showgrid=True, ticks="outside", tickson="boundaries", range=[0,15], dtick=10)


fig.show()



fig = px.box(rfq, x="Status", y="WaitingTimeMS", color="Status", title="Box plot (Waiting Time MS)", facet_col="Customer", facet_col_wrap=6,
             color_discrete_sequence=["green", "yellow", "red", "red", "yellow", "green", "red", "red", "red", "red", "green", "red"])
fig.update_xaxes(categoryorder='array', categoryarray= ['Accepted', 'AllocAcpt', 'AllocSent', 'Covered', 'Tie-TW', 'TrAway', 'C/Expire', 'D/Expire'])
fig.update_yaxes(showgrid=True, ticks="outside", tickson="boundaries", range=[0,150000], dtick=10000)
fig.show()

fig = px.histogram(real, x = real['WaitingTimeMS'], hover_data=['Security', 'Price','Side', 'DlrsCmp','CBBT Bid Prc','CBBT Mid Prc', 'CBBT Ask Prc'], color="Status", nbins=500, facet_col="Customer", facet_col_wrap=3,
                   title="Waiting time ", 
                   color_discrete_sequence=["green", "yellow", "red", "red", "yellow", "green", "red", "red", "red", "red", "green", "red"], opacity = 0.2)

fig.show()

fig = px.histogram(real, x = real['PriceDiff'], hover_data=['Security', 'Price','Side', 'DlrsCmp','CBBT Bid Prc','CBBT Mid Prc', 'CBBT Ask Prc'], color="Status", nbins=500, facet_col="Customer", facet_col_wrap=6,
                   title="Price Distribution from CBBT Mid <br>Negative x-values indicates non-inverted prices. Positive values indicates inverted prices.<br> ", 
                   color_discrete_sequence=["green", "yellow", "red", "red", "yellow", "green", "red", "red", "red", "red", "green", "red"], opacity = 0.2)


# Set axes ranges
fig.update_xaxes(range=[-0.5, 0.5])
fig.update_yaxes(range=[0, 25])

fig.add_shape(type="line",
    x0=0, y0=0, x1=0, y1=100, row=1 , col=1,
    line=dict(color="Black",width=4)
)

fig.add_shape(type="line",
    x0=0, y0=0, x1=0, y1=100, row=0 , col=1,
    line=dict(color="Black",width=4)
)

fig.add_shape(type="line",
    x0=0, y0=0, x1=0, y1=100, row=0 , col=2,
    line=dict(color="Black",width=4)
)

fig.add_shape(type="line",
    x0=0, y0=0, x1=0, y1=100, row=0 , col=3,
    line=dict(color="Black",width=4)
)

fig.add_shape(type="line",
    x0=0, y0=0, x1=0, y1=100, row=1 , col=2,
    line=dict(color="Black",width=4)
)


fig.add_shape(type="line",
    x0=0, y0=0, x1=0, y1=100, row=1 , col=3,
    line=dict(color="Black",width=4)
)


#fig.add_shape(
#    dict(type="line", x0=-2, y0=12, x1=2, y1=20), row=1, col=1, line=dict(color="Black",width=3)
#)


fig.show()

real = rfq[rfq['TS Book Name'].isin(['REAL'])]

real_acc = real[real['Status'].isin(['AllocSent', 'Accepted'])]
real_cov = real[real['Status'].isin(['Tie-TW', 'Covered'])]
real_notacc = real[real['Status'].isin(['TrAway', 'Passed', 'C/Expire', 'D/Expire', 'Rejected', 'Cancel'])]
real_notacc = real[real['PriceDiff'] < 6]
#real_acc = accepted[accepted['TS Book Name'].isin(['REAL'])]
#real_Nacc = accepted[accepted['TS Book Name'].isin(['ILLIKVID'])]

real_2 = [real_acc['PriceDiff'].dropna().tolist(), real_notacc['PriceDiff'].dropna().tolist(), real_cov['PriceDiff'].dropna().tolist()]

import plotly.figure_factory as ff
import numpy as np

group_labels = ['REAL Accepted', 'REAL NOT Accepted', 'REAL Covered / Tie']


# Create distplot with custom bin_size
fig = ff.create_distplot(real_2, group_labels, bin_size=[.01, .01, .01]
                   )

fig.add_shape(type="line",
    x0=0, y0=0, x1=0, y1=13, 
    
    line=dict(color="red",width=2)
)

fig.update_layout(title='REAL Book <br>Side B: CBBT Mid Prc - Price<br>Side S: Price - CBBT Mid Prc')

fig.update_xaxes(range=[-1.5,1.5],tick0=0, dtick=0.1)
fig.update_xaxes(showgrid=True)

#fig.show()


#rfq.loc[rfq['Side'] == '[B]', 'PriceDiff'] = (rfq['CBBT Mid Prc'] - rfq['Price']) 
#rfq.loc[rfq['Side'] == '[S]', 'PriceDiff'] = (rfq['Price'] - rfq['CBBT Mid Prc'])



all = rfq[rfq['Status'].isin(['AllocSent', 'Accepted', 'AllocAcpt'])]


all_stat = all[all['TS Book Name'].isin(['STAT'])]
all_real = all[all['TS Book Name'].isin(['REAL'])]
all_flex = all[all['TS Book Name'].isin(['FLEX'])]
all_ill = all[all['TS Book Name'].isin(['ILLIKVID'])]
#all_float = all[all['TS Book Name'] < 6]
#real_acc = accepted[accepted['TS Book Name'].isin(['REAL'])]
#real_Nacc = accepted[accepted['TS Book Name'].isin(['ILLIKVID'])]

all_2 = [all_stat['PriceDiff'].dropna().tolist(), all_real['PriceDiff'].dropna().tolist(), all_flex['PriceDiff'].dropna().tolist(), all_ill['PriceDiff'].dropna().tolist()]



group_labels = ['Stat', 'REAL', 'FLEX', 'ILLIKVID']


# Create distplot with custom bin_size
fig = ff.create_distplot(all_2, group_labels, bin_size=[.01, .01, .01, 0.01]
                   )

fig.add_shape(type="line",
    x0=0, y0=0, x1=0, y1=37, 
    
    line=dict(color="red",width=2)
)

fig.update_layout(title='Price Diff for all acceptede trades on all books <br>Side B: CBBT Mid Prc - Price<br>Side S: Price - CBBT Mid Prc')

fig.update_xaxes(range=[-1.5,1.5],tick0=0, dtick=0.1)

fig.update_xaxes(showgrid=True)



#fig.show()

#real = rfq[rfq['TS Book Name'].isin(['REAL'])]

rfq_acc = rfq[rfq['Status'].isin(['AllocSent', 'Accepted'])]
rfq_cov = rfq[rfq['Status'].isin(['Tie-TW', 'Covered'])]
rfq_notacc = rfq[rfq['Status'].isin(['TrAway', 'Passed', 'C/Expire', 'D/Expire', 'Rejected', 'Cancel'])]
#ap_notacc = ap[ap['PriceDiff'] < 6]
#real_acc = accepted[accepted['TS Book Name'].isin(['REAL'])]
#real_Nacc = accepted[accepted['TS Book Name'].isin(['ILLIKVID'])]

rfq_2 = [rfq_acc['PriceDiff'].dropna().tolist(), rfq_notacc['PriceDiff'].dropna().tolist(), rfq_cov['PriceDiff'].dropna().tolist()]

import plotly.figure_factory as ff
import numpy as np

group_labels = ['All Accepted', 'All NOT Accepted', 'All Covered / Tie']


# Create distplot with custom bin_size
fig = ff.create_distplot(rfq_2, group_labels, bin_size=[.01, .01, .01]
                   )

fig.add_shape(type="line",
    x0=0, y0=0, x1=0, y1=20, 
    
    line=dict(color="red",width=2)
)

fig.update_layout(title='RFQ All Books <br>Side B: CBBT Mid Prc - Price<br>Side S: Price - CBBT Mid Prc')

fig.update_xaxes(range=[-1,1.5],tick0=0, dtick=0.1)
fig.update_xaxes(showgrid=True)

#fig.show()


#rfq.loc[rfq['Side'] == '[B]', 'PriceDiff'] = (rfq['CBBT Mid Prc'] - rfq['Price']) 
#rfq.loc[rfq['Side'] == '[S]', 'PriceDiff'] = (rfq['Price'] - rfq['CBBT Mid Prc'])

real.groupby(['Customer','Status2', 'PriceDiffDummy'])['Quantity'].count()

fig = px.pie(real, values='Quantity', names='Status2', title='Quantity pr Status', color='Status2', 
             color_discrete_map={'TrAway':'red',
                                 'Accepted':'green',
                                 'Covered':'yellow'
                                 })
fig.show()



import plotly.express as px

fig = px.sunburst(lazard, path=['TS Book Name', 'Status2', 'PriceDiffDummy'], values='Quantity', title='Lazard Status & Book', color='Status2',
                  color_discrete_map={'TrAway':'red',
                                 'Accepted':'green',
                                 'Covered':'yellow',
                                 '(?)': 'BLUE',
                                 'STAT': 'Black'
                                 }
                                 )
fig.show()

stat = rfq[rfq['TS Book Name'].isin(['STAT'])]

fig = px.sunburst(stat, path=[ 'Status2', 'PriceDiffDummy'], values='Quantity', title='STAT Quantity pr Status', color='Status2', 
                  color_discrete_map={'TrAway':'red',
                                      'Non-Inverted':'green',
                                 'Accepted':'green',
                                 'Covered':'yellow',
                                  'Inverted':'red'
                                  
                                 })
fig.show()

"""**ENDS HERE**"""

daiwa = rfq[rfq['Customer'] == 'DAIWA ASSET MANAGEMENT CO. LTD']

fig = px.sunburst(lazard, path=[ 'Status2', 'PriceDiffDummy'], values='Quantity', title='Daiwa pr Status', color='Status2', 
                  color_discrete_map={'TrAway':'red',
                                 'Accepted':'green',
                                 'Accepted/Inverted':'red',
                                 'Covered':'yellow'
                                 })
fig.show()

ubs = rfq[rfq['Customer'] == 'UBS ASSET MANAGEMENT SWITZERLAND AG']

fig = px.sunburst(lazard, path=[ 'Status2', 'PriceDiffDummy'], values='Quantity', title='LAZARD pr Status', color='Status2', 
                  color_discrete_map={'TrAway':'red',
                                 'Accepted':'green',
                                 'Covered':'yellow'
                                 })
fig.show()

nordea = rfq[rfq['Customer'] == 'NORDEA INVESTMENT MANAGEMENT AB']

fig = px.sunburst(nordea, path=[ 'Status2', 'PriceDiffDummy'], values='Quantity', title='Nordea pr Status', color='Status2', 
                  color_discrete_map={'TrAway':'red',
                                 'Accepted':'green',
                                 'Covered':'yellow'
                                 })
fig.show()

skandia = rfq[rfq['Customer'] == 'SKANDIA ASSET MGMT FONDSMGLERS A/S']

fig = px.sunburst(skandia, path=[ 'Status2', 'PriceDiffDummy'], values='Quantity', title='Skandia pr Status', color='Status2', 
                  color_discrete_map={'TrAway':'red',
                                 'Accepted':'green',
                                 'Covered':'yellow'
                                 })
fig.show()

fig = px.box(skandia, x="MonthName", y="DlrsCmp",  hover_data=rfq.groupby(['MonthName']).aggregate({"DlrsCmp":np.mean}), facet_col="Customer", facet_col_wrap=6)
fig.update_xaxes(categoryorder='array', categoryarray= ['January','February','March','April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
fig.update_yaxes(range=[0,6],tick0=0, dtick=1)

fig.show()

inverted = rfq[rfq['PriceDiffDummy'] == 'Inverted']

fig = px.sunburst(inverted, path=[ 'Status2', 'TS Book Name'], values='Quantity', title='Skandia pr Status', color='Status2', 
                  color_discrete_map={'TrAway':'red',
                                 'Accepted':'green',
                                 'Covered':'yellow'
                                 })
fig.show()

fig = px.sunburst(rfq, path=[ 'Status2', 'TS Book Name', 'PriceDiffDummy'], values='Quantity', title='Skandia pr Status', color='Status2', 
                  color_discrete_map={'TrAway':'red',
                                 'Accepted':'green',
                                 'Covered':'yellow'
                                 })
fig.show()

fig = px.sunburst(real, path=[ 'Status2',  'PriceDiffDummy', 'Customer'], values='Quantity', title='Skandia pr Status', color='Status2', 
                  color_discrete_map={'TrAway':'red',
                                 'Accepted':'green',
                                 'Covered':'yellow'
                                 })
fig.show()

import plotly.express as px
import numpy as np

fig = px.treemap(lazard, path=['TS Book Name', 'Status2', 'PriceDiffDummy'], values='Quantity',
                  color='Status2', hover_data=['Customer'])
fig.show()

import plotly.express as px
import numpy as np

fig = px.treemap(real, path=['Status2', 'PriceDiffDummy','Customer'], values='Quantity',
                  color='Customer', hover_data=['Customer'])
fig.show()

fig = px.treemap(inverted, path=['TS Book Name', 'Status2', 'Customer'], values='Quantity',
                  color='Status2', hover_data=['Customer'])
fig.show()

lazard_real = lazard[lazard['TS Book Name'] == 'REAL']

fig = px.treemap(lazard_real, path=['TS Book Name', 'Status2', 'PriceDiffDummy'], values='Quantity',
                  color='Customer', hover_data=['Customer'])
fig.show()

inverted_real_laz = lazard_real[lazard_real['Status2'] == 'Accepted']

fig = px.treemap(inverted_real_laz, path=['TS Book Name', 'Status2', 'PriceDiffDummy'], values='Quantity',
                  color='Customer', hover_data=['Customer'])
fig.show()

all_stat = rfq[rfq['TS Book Name'].isin(['STAT'])]
all_real = rfq[rfq['TS Book Name'].isin(['REAL'])]
all_flex = rfq[rfq['TS Book Name'].isin(['FLEX'])]
all_ill = rfq[rfq['TS Book Name'].isin(['ILLIKVID'])]
#all_float = all[rfq['TS Book Name'] < 6]
#real_acc = accepted[accepted['TS Book Name'].isin(['REAL'])]
#real_Nacc = accepted[accepted['TS Book Name'].isin(['ILLIKVID'])]

all_2 = [all_stat['WaitingTimeMS'].dropna().tolist(), all_real['WaitingTimeMS'].dropna().tolist(), all_flex['WaitingTimeMS'].dropna().tolist(), all_ill['WaitingTimeMS'].dropna().tolist()]

group_labels = ['Stat', 'REAL', 'FLEX', 'ILLIKVID']


# Create distplot with custom bin_size
fig = ff.create_distplot(rfq, group_labels, bin_size=[.1, .1, .1, 0.01]
                   )

fig.add_shape(type="line",
    x0=0, y0=0, x1=0, y1=37, 
    
    line=dict(color="red",width=2)
)

fig.update_layout(title='Price Diff for all acceptede trades on all books <br>Side B: CBBT Mid Prc - Price<br>Side S: Price - CBBT Mid Prc')

fig.update_xaxes(range=[-15,15],tick0=0, dtick=0.1)

fig.update_xaxes(showgrid=True)



#fig.show()

