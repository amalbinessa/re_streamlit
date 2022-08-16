import streamlit as st
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re

# add app title
st.set_page_config(
    page_title="ماذا يقول عنك محرك البحث قوقل",
    page_icon="✅",
    layout="wide",
)


st.title("ابحث عنك في قوقل")
query = st.text_input('search keywords')
    if query:
        query = "شركة ثقة لخدمات الأعمال"
search = query.replace(' ', '+')
results = st.text_input('number of result')
    if results:
        results = 10
url = (f"https://www.google.com/search?q={search}&num={results}")

requests_results = requests.get(url)
soup_link = BeautifulSoup(requests_results.content, "html.parser")
links = soup_link.find_all("a")
#links_list = []
title_link_list = []

for link in links:
    link_href = link.get('href')
    if "url?q=" in link_href and not "webcache" in link_href:
      title = link.find_all('h3')

      if len(title) > 0:
          title_list = []
          print(title[0].getText())
          title_list.append(title[0].getText())
          print(link.get('href').split("?q=")[1].split("&sa=U")[0])
          title_list.append(link.get('href').split("?q=")[1].split("&sa=U")[0])
          
          print("------")
          title_link_list.append(title_list)


# List1 
df = pd.DataFrame(title_link_list, columns =['title', 'link']) 
df.shape
st.dataframe(df)

   
