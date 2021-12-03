import pandas as pd
from pandas._config.config import options
import plotly.express as px
import streamlit as st
import numpy as np


st.set_page_config(page_title="Startup Funding Dashboard ",
                   page_icon=":moneybag:",
                   layout="wide",
                   )
dataf = pd.read_csv("startup_funding.csv",
                    skipinitialspace=True,
                    )


# Correcting the name of the City
dataf['CityLocation'].replace('Delhi', 'New Delhi', inplace=True)
dataf['CityLocation'].replace('bangalore', 'Bangalore', inplace=True)

# Getting all the first City name
dataf['CityLocation'] = dataf['CityLocation'].str.split(' /').str[0]
dataf['CityLocation'] = dataf['CityLocation'].str.split('/').str[0]

dataf['InvestmentType'].replace('SeedFunding', 'Seed Funding', inplace=True)
dataf['InvestmentType'].replace('Crowd funding', 'Crowd Funding', inplace=True)
dataf['InvestmentType'].replace(
    'PrivateEquity', 'Private Equity', inplace=True)
# dataf['InvestmentType'].fillna('Debt funding', inplace=True)
dataf.dropna(subset=['InvestmentType'], inplace=True)

# Preprocessing for (top 5 industries which got easily funded)

dataf1 = dataf.copy()
dataf1.dropna(subset=['IndustryVertical', 'AmountInUSD'], inplace=True)
dataf1['IndustryVertical'].replace('ecommerce', 'Ecommerce', inplace=True)
dataf1['IndustryVertical'].replace('ECommerce', 'Ecommerce', inplace=True)
dataf1['IndustryVertical'].replace('eCommerce', 'Ecommerce', inplace=True)


def amount_generator(amt):
    amt = amt.split(',')
    ans = ""
    for i in range(len(amt)):
        ans = ans+amt[i].strip()
    return int(ans)


dataf1['AmountInUSD'] = dataf1['AmountInUSD'].apply(amount_generator)

# --- sidebar


# --- MAINPAGE
# new_title = '<p style="font-family:sans-serif; color:Green; font-size: 42px;">New image</p>'
# st.markdown(new_title, unsafe_allow_html=True)
st.title(":chart_with_upwards_trend: Indian Startups Funding Dashboard")
st.markdown("##")

total_amt = (dataf1['AmountInUSD'].sum())
total_amt = (total_amt.astype(float)/1000000000).round(2).astype(str) + 'B'
lcol, midcol, rightcol = st.columns(3)
with lcol:
    st.subheader("Total Amount Funded:")
    st.subheader(f"US$ {total_amt}")

st.markdown("##")
agree = st.checkbox('See Dataset')
if agree:
    st.dataframe(dataf)

line_chart_data = dataf.copy()
line_chart_data['Year'] = line_chart_data['Date'].str[-4:]

year = line_chart_data.Year.value_counts()
year.sort_index(inplace=True)


line_chart = px.line(year)
line_chart.update_layout(title='<b>Startups Funding Vs Year<b>',
                         xaxis_title='<b>Years<b>',
                         yaxis_title='<b>No. of Fundings<b>',
                         font_size=16,
                         )

# fig.update_traces(mode='lines')
left_column, right_column = st.columns(2)
left_column.plotly_chart(line_chart, use_container_width=True)
# middle_column.plotly_chart(line_chart, use_container_width=True)
# right_column.plotly_chart(line_chart, use_container_width=True)

# st.write(line_chart)


# ploting th bar chart between location and number of fundings to that location
st.markdown("##")
investment_type = st.multiselect(
    "Select the Investment Type: ",
    options=dataf["InvestmentType"].unique(),
    default=dataf["InvestmentType"].unique()
)

df_selection = dataf.query(
    "InvestmentType == @investment_type"
)

city_number = df_selection['CityLocation'].value_counts()[0:10]
city = city_number.index
numCity = city_number.values
# for i in range(len(city)):
#     print(city[i], numCity[i])

bar_graph = px.bar(city_number,
                   text=city_number.values,
                   orientation="v",
                   width=1100,
                   template="plotly_dark")


bar_graph.update_traces(marker_color=['#0D0887', '#41039D', '#6F01A7', '#890DA2', '#A01B9B', '#C03B83', '#DE6164', '#EF7E50', '#FA9D3B', '#FCB331'], marker_line_color='cyan',
                        marker_line_width=1.5, opacity=1)


bar_graph.update_traces(texttemplate='%{text:.2s}', textposition='outside')

bar_graph.update_yaxes(range=[0, 700])
st.markdown("##")
bar_graph.update_layout(
    title_text='<b>Top 10 Indian Cities location for startup<b>',
    xaxis_title='<b>Location<b>',
    yaxis_title='<b>No. of Fundings<b>',
    margin=dict(t=30, l=380, r=50, b=50),
    font_size=16,

)

# right_column.plotly_chart(bar_graph, use_container_width=True)
st.write(bar_graph, use_container_width=True)

# pie chart
iv = list(dataf1.IndustryVertical)
amt = list(dataf1.AmountInUSD)
d = {}

for i in range(len(iv)):
    d[iv[i]] = d.get(iv[i], 0)+amt[i]

key = list(d.keys())
values = list(d.values())

# for state, capital in d.items():
#     print(state, ":", capital)

key = np.array(key)
values = np.array(values)

ind = values.argsort()[::-1]
ind = ind[:5]

key = key[ind]
values = values[ind]

values = (values/sum(values))*100
values = np.round(values, decimals=2)
# print(key)
# print(values)

pie_chart = px.pie(
    values=values,
    names=key,
    title="<b>Top 5 Industries in terms of funding </b>",

    # figure height in pixels

    # color_discrete_sequence=px.colors.sequential.RdBu
)
# colors = ['#890DA2', '#FA9D3B', '#C03B83', '#DE6164', '#EF7E50']
colors = ['rgb(33, 75, 99)', 'rgb(79, 129, 102)', 'rgb(151, 179, 100)',
          'rgb(175, 49, 35)', 'rgb(36, 73, 147)']
pie_chart.update_traces(hoverinfo='label+percent', textposition='inside', textinfo='percent', textfont_size=20,
                        marker=dict(colors=colors, line=dict(color='#000000', width=2)))
pie_chart.update_layout(uniformtext_minsize=12, uniformtext_mode='hide', font_size=16, annotations=[dict(text='', x=0.18, y=0.5, font_size=20, showarrow=False),
                                                                                                    dict(text='', x=0.82, y=0.5, font_size=20, showarrow=False)]
                        )
right_column.plotly_chart(pie_chart, use_container_width=True)


# .The list of top 5 investors from dataset
# '''Creating the Dictionary in which we store the key as name of the investors and
#    value as the number of times they invested'''

dataf2 = dataf.copy()
dataf2.dropna(subset=['InvestorsName'], inplace=True)


def make_dictionary(arr):
    dictionary = {}
    for i in arr:
        # print(i)
        # '''We do not need to take the Undisclosed Investors and also the investors with blank name'''
        if i == 'Undisclosed Investors' or i == 'Undisclosed investors' or i == '':
            continue
        if ',' not in i:
            if i in dictionary:
                dictionary[i] = dictionary.get(i)+1
            else:
                dictionary[i] = 1
        else:
            string = i.strip().split(',')
            for j in string:
                if j.strip() in dictionary:
                    dictionary[j.strip()] = dictionary.get(j.strip())+1
                elif j.strip() != "":
                    dictionary[j.strip()] = 1
    return dictionary


st.markdown("##")
investor_selector = st.slider('Select the numbers of Investors you want:',
                              min_value=2,
                              max_value=15,
                              value=(2, 15)
                              )

invest_type = st.multiselect(
    "Select the Investment Type of the Investor: ",
    options=dataf2["InvestmentType"].unique(),
    default=dataf2["InvestmentType"].unique()
)
st.markdown("##")
df_select = dataf2.query(
    "InvestmentType == @invest_type"
)
# print(investor_selector[0])

# Getting the Dictionary
dictionary = make_dictionary(df_select['InvestorsName'])

key1 = list(dictionary.keys())
values1 = list(dictionary.values())

invl = len(key1)
with midcol:
    st.subheader("Total No. of Investors:")
    st.subheader(f"{invl}")


key1 = np.array(key1)
values1 = np.array(values1)
ind = values1.argsort()[::-1]
ind = ind[:investor_selector[0]]

key1 = key1[ind]
values1 = values1[ind]
values1 = (values1/sum(values1))*100
values1 = np.round(values1, decimals=2)

# print(invest_type)
d1 = {
    'iname': key1,
    'ivalue': values1
}
df1 = pd.DataFrame(d1)
pie_chart1 = px.pie(
    data_frame=df1,
    values='ivalue',
    template='presentation',
    names='iname',
    title=f'<b>Top {investor_selector[0]} Investors names who have invested maximum number of times<b>',
    width=1100,
    height=500,  # figure height in pixels
    hole=0.4,

    # color_discrete_sequence=px.colors.sequential.RdBu
)
# colors = ['#890DA2', '#FA9D3B', '#C03B83', '#DE6164', '#EF7E50']
colors = ['rgb(33, 75, 99)', 'rgb(79, 129, 102)', 'rgb(151, 179, 100)',
          'rgb(175, 49, 35)', 'rgb(36, 73, 147)']
pie_chart1.update_traces(hoverinfo='label+percent', textposition='inside', textinfo='percent', textfont_size=20,
                         marker=dict(colors=colors, line=dict(color='#000000', width=2)))
pie_chart1.update_layout(uniformtext_minsize=12,
                         uniformtext_mode='hide',
                         font_size=16,
                         margin=dict(t=30, l=380, r=50, b=50),
                         annotations=[dict(text='', x=0.18, y=0.5, font_size=20, showarrow=False), dict(
                             text='', x=0.82, y=0.5, font_size=20, showarrow=False)]
                         )
st.markdown("##")
st.write(pie_chart1)


# top startups
dataf3 = dataf.copy()

dataf3 .dropna(subset=['StartupName', 'AmountInUSD'], inplace=True)
dataf3['StartupName'].replace('Flipkart.com', 'Flipkart', inplace=True)
dataf3['StartupName'].replace('Ola Cabs', 'Ola', inplace=True)
dataf3['StartupName'].replace('Olacabs', 'Ola', inplace=True)
dataf3['StartupName'].replace('Ola Cabs', 'Ola', inplace=True)
dataf3['StartupName'].replace('Olacabs', 'Ola', inplace=True)
dataf3['StartupName'].replace('Oyo Rooms', 'Oyo', inplace=True)
dataf3['StartupName'].replace('OyoRooms', 'Oyo', inplace=True)
dataf3['StartupName'].replace('OYO Rooms', 'Oyo', inplace=True)
dataf3['StartupName'].replace('Paytm Marketplace', 'Paytm', inplace=True)

dataf3['AmountInUSD'] = dataf3['AmountInUSD'].apply(amount_generator)

st1 = list(dataf3.StartupName)
amt = list(dataf3.AmountInUSD)
d = {}
slen = len(st1)
with rightcol:
    st.subheader("Total Startups incorporated:")
    st.subheader(f"{slen}")

for i in range(len(st1)):
    d[st1[i]] = d.get(st1[i], 0)+amt[i]

key2 = list(d.keys())
values2 = list(d.values())

key2 = np.array(key2)
values2 = np.array(values2)

ind = values2.argsort()[::-1]
ind = ind[:40]

key2 = key2[ind]
values2 = values2[ind]

# print(key2)
# print(values2)

for i in range(len(values2)):
    d[key2[i]] = values2[i]

the_dict = {'dates': key2, 'y_vals': values2}
bar_graph2 = px.bar(the_dict, x='dates', y='y_vals',
                    orientation="v",
                    width=1100,
                    height=500,
                    template="plotly_dark")

colors1 = ['#0D0887', '#41039D', '#6F01A7', '#890DA2', '#A01B9B',
           '#C03B83', '#DE6164', '#EF7E50', '#FA9D3B', '#FCB331',
           '#0D0887', '#41039D', '#6F01A7', '#890DA2', '#A01B9B',
           '#C03B82', '#DE6165', '#EF7E52', '#FA9D6B', '#FCB339',
           '#0D0887', '#41039D', '#6F01A7', '#890DA2', '#A01B9B',
           '#C03B83', '#DE6164', '#EF7E50', '#FA9D3B', '#FCB331',
           '#0D0887', '#41039D', '#6F01A7', '#890DA2', '#A01B9B',
           '#C03B83', '#DE6164', '#EF7E50', '#FA9D3B', '#FCB331',
           '#0D0887', '#41039D', '#6F01A7', '#890DA2', '#A01B9B',
           '#C03B83', '#DE6164', '#EF7E50', '#FA9D3B', '#FCB331',
           '#0D0887', '#41039D', '#6F01A7', '#890DA2', '#A01B9B',
           '#C03B83', '#DE6164', '#EF7E50', '#FA9D3B', '#FCB331']*5
bar_graph2.update_traces(marker_color=colors1, marker_line_color='cyan',
                         marker_line_width=0.5, opacity=1)

st.markdown("##")
bar_graph2.update_layout(
    title_text='<b>Top Startups based on Fundings<b>',
    xaxis_title='<b>Startup Name<b>',
    yaxis_title='<b>Amount<b>',
    margin=dict(t=30, l=380, r=50, b=50),
    font_size=16,

)
st.write(bar_graph2)


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
