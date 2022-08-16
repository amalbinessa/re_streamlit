import streamlit as st # data web app development
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re
import time  # to simulate a real time data, time loop
import plotly.express as px  # interactive charts
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt


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
This app performs Word Cloud
* **Python libraries:** streamlit, pandas BeautifulSoup, Wordcloud..
""")
query = st.text_input('search keywords')
if query:
    query = query #"شركة ثقة لخدمات الأعمال"
else :
    query = "شركة ثقة لخدمات الأعمال"
search = query.replace(' ', '+')
results = 200

print("Top site's name")
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

title_filter = st.selectbox("Select the title", pd.unique(df["cleaned_title"]))

 # dataframe filter
df = df[df["cleaned_title"] == title_filter] 

#the option to choose the number of words to be in the word cloud.
st.sidebar.header("Select No. of words you want to display")
words = st.sidebar.selectbox("No. of words", range(10, 1000, 10))


st.write("Word Cloud Plot")

cleaned_title =  str(df['cleaned_title'])
#cleaning the data with regular expression library
cleaned_text_1 = re.sub('\t', "", cleaned_title)
cleaned_text_2 = re.split('\n', cleaned_text_1)
cleaned_text_3 = "".join(cleaned_text_2)

#using stopwords to remove extra words
stopwords = set(STOPWORDS)
wordcloud = WordCloud(background_color = "white", max_words = words,stopwords = stopwords).generate(cleaned_text_3)


plt.imshow(wordcloud, interpolation = 'bilinear')
plt.axis("off")
plt.show()
st.pyplot()


# create two columns for charts
fig_col1, fig_col2 = st.columns(2)

with fig_col1:
    st.markdown("### firest Chart")
    fig2 = px.histogram(data_frame=df, x="cleaned_title")
    st.write(fig2)

with fig_col2:
    st.markdown("### Second Chart")
    fig2 = px.histogram(data_frame=df, x="source_site_name")
    st.write(fig2)


