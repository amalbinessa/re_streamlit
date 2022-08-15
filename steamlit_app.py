import streamlit as st
import pandas as pd
import numpy as np
# add app title
st.set_page_config(
    page_title="ماذا يقول عنك محرك البحث قوقل",
    page_icon="✅",
    layout="wide",
)

st.title("ابحث عنك في قوقل")

import requests
from bs4 import BeautifulSoup
import re

query = "شركة ثقة لخدمات الأعمال"
search = query.replace(' ', '+')
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
dataset_url ="https://github.com/amalbinessa/re_streamlit/blob/main/Data/T_dataframe.csv"


# read csv from a URL



import csv

with open(dataset_url, mode='w') as employee_file:
    employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)



