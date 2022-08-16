import streamlit as st # data web app development
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import time  # to simulate a real time data, time loop
import plotly.express as px  # interactive charts
import matplotlib.pyplot as plt
import arabic_NER

# to remove any warning coming on streamlit web app page
st.set_option('deprecation.showPyplotGlobalUse', False)
# add app title
st.set_page_config(
    page_title="ماذا يقول عنك محرك البحث قوقل",
    page_icon="✅",
    layout="wide",
)


st.title("ابحث عنك في قوقل")
st. markdown("""
**************************
""")
query = st.sidebar.text_input('search keywords')
if query:
    query = query #"شركة ثقة لخدمات الأعمال"
else :
    query = "شركة ثقة لخدمات الأعمال"
search = query.replace(' ', '+')
results = 200


url = (f"https://www.google.com/search?q={search}&num={results}")

requests_results = requests.get(url)
soup_link = BeautifulSoup(requests_results.content, "html.parser")
links = soup_link.find_all("a")
title_link_list = []

for link in links:
    link_href = link.get('href')
    if "url?q=" in link_href and not "webcache" in link_href:
      title = link.find_all('h3')

      if len(title) > 0:
          title_list = []
          title_list.append(title[0].getText())
          title_list.append(link.get('href').split("?q=")[1].split("&sa=U")[0])
          
          title_link_list.append(title_list)



# add result to dataframe
df = pd.DataFrame(title_link_list, columns =['title', 'link']) 

# extract information from title and link data  

def split_text(text):
  
  if ' - ' in text:
    return text.split('-',1)
  elif '/' in text:
    return text.rsplit('/',1)
  elif '|' in text:
    return text.rsplit('|',1)
  
  else:
    return [text,0]
# text preprocessing 
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

#title_filter = st.sidebar.selectbox("Select the title", pd.unique(df["source_site_name"]))

 # dataframe filter
#df = df[df["cleaned_title"] == title_filter] 

#the option to choose the number of words to be in the word cloud.
st.sidebar.header("Select No. of words you want to display")
words = st.sidebar.selectbox("No. of words", range(10, 1000, 10))

# cleaned_text for 
def get_cleaned_text(text):
    return ' '.join(text.tolist())

cleaned_text = get_cleaned_text(df['cleaned_title'])


##################################### NER ##################################


def text_to_ner_model_line(text):
  text = arabic_NER.get_ner(text)
  return get_entity_key_value(text)
def get_entity_key_value(text):
  key__value_list_outer = []
  for ner_ in text[0]:
    for key , value in ner_.items():
      if '-' in value:
        #key_value_list_inner = [key,value]
        key__value_list_outer.append(key)

  return key__value_list_outer

df['entity_list'] = [text_to_ner_model_line(text) for text in df['cleaned_title']]



############################################################################

# create two columns for charts
fig_col1, fig_col2 , fig_col3 = st.columns(3)

with fig_col1:
    st.markdown("### firest Chart")
    fig2 = px.histogram(data_frame=df, x="cleaned_title")
    st.write(fig2)

with fig_col2:
    st.markdown("### Second Chart")
    fig2 = px.histogram(data_frame=df, x="source_site_name")
    st.write(fig2)
fig_col3 = st.columns(1)

with fig_col3:
    st.markdown("### 3 Chart")
    fig2 = px.histogram(data_frame=df, x="entity_list")
    st.write(fig3)


