import pandas as pd
import streamlit as st
from urllib.request import urlretrieve
from urllib.parse import urlparse
import plotly.graph_objects as go
pd.options.plotting.backend = "plotly"

st.title("Risk Analysis")
url_input = st.text_area("Enter a list of Yahoo Stock Data URLs (one per line)")
urls = [url.strip() for url in url_input.split("\n") if url.strip() != ""]
if len(urls) == 0:
    st.stop()
dfs = {}
for url in urls: 
    name = urlparse(url).path[-1]
    urlretrieve(url, "data.csv")
    dfs[name] = pd.read_csv("data.csv",index_col=0, parse_dates=True).replace(0, pd.NA)
df = next(iter(dfs.values()))
st.dataframe(df.head())
fig = go.Figure(data=[go.Candlestick(x=df.index, open=df["Open"], high=df["High"], low=df["Low"], close=df["Close"])])
st.plotly_chart(fig)
days = st.sidebar.number_input("Number of days", value=365)

fig2 = go.Figure(data=[go.Line(x=df.index, y=df["Open"].rolling(days).apply(lambda s: (s.iloc[-1]-s.iloc[0])/s.iloc[0]))])
fig2.add_hline(y=-0.1, line_dash="dot", line_color="red")
fig2.update_layout(dict(title_text="Gain/Loss over {} days".format(days), yaxis_range=(-1, 2)))

st.plotly_chart(fig2)