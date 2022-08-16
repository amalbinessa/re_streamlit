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
    query = query #"شركة ثقة لخدمات الأعمال"
search = query.replace(' ', '+')
results = st.text_input('number of result')
if results:
    results = results
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


# extract information from title and link data  
df = pd.DataFrame(title_link_list, columns =['title', 'link']) 

def split_text(text):
  
  if ' - ' in text:
    print(text.rsplit('-',1))
    return text.split('-',1)
  elif '/' in text:
    print(text.rsplit('/',1))
    return text.rsplit('/',1)
  elif '|' in text:
    print( text.rsplit('|',1))
    return text.rsplit('|',1)
  
  else:
    print([text,'0'])
    return [text,0]

import re
df['title'] = df['title'].str.replace('.', '')
df['title'].str.strip()
df['splited_title'] =[split_text(text) for text in df['title']]
df['sub_title'] = [splited_title[0] for splited_title in df['splited_title']]

df['surce_name'] = [splited_title[-1] for splited_title in df['splited_title']]

# get source_site_name from link

df['sub_link'] = df['link'].str.split('/', 3)

def get_source_site_name(site_link):
  site_link[2].split('.')[-2]
  return site_link[2].split('.')[-2]

df['source_site_name'] = [get_source_site_name(link) for link in df['sub_link']]

# text preprocessing :
def get_text_preprocessing(text):
  # text = str(text).strip()
  # text = text.lstrip()
  # " ".join(text.split())
  
  #clean non Arabic letters and spicial characters  

  text = re.sub('([@A-Za-z0-9_ـــــــــــــ]+)|[^\w\s]|#|http\S+', '', text) # cleaning up

  return " ".join(text.split())
df['cleaned_title'] = [get_text_preprocessing(text) for text in df['sub_title']]
# top-level filters

job_filter = st.selectbox("Select the Job", pd.unique(df["cleaned_title"]))

AgGrid(df, height=500, fit_columns_on_grid_load=True)

   
