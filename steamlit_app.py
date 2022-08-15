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

query = "شركة ثقة لخدمات الأعمال"
search = query.replace(' ', '+')
results = 100
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
          title_list.append(title[0].getText())
          print(link.get('href').split("?q=")[1].split("&sa=U")[0])
          title_list.append(link.get('href').split("?q=")[1].split("&sa=U")[0])
          
          print("------")
          title_link_list.append(title_list)
print("Done!")

title_link_content_list = []
for index , title_link  in enumerate(title_link_list):
  # url of the website
  doc = title_link[1]
  try:
    # getting response object
    res = requests.get(doc)

    # Initialize the object with the document
    soup = BeautifulSoup(res.content, "html.parser")
  
    # Get the whole body tag
    tag = soup.p
    string_list = []
    # Print each string recursively
    for string in tag.strings:
      print(string)
      string_list.append(string)
      joined_string = ''.join(string_list)
    title_link.append(joined_string)
    title_link_content_list.append(title_link)
  except Exception as e: 
    title_link.append(0)
    title_link_content_list.append(title_link)
    pass
# List1 
df = pd.DataFrame(title_link_content_list, columns =['title', 'link', 'content']) 
df.shape
st.write(df)
