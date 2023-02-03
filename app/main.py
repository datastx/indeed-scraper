import sys

sys.path.append('/Users/brianmoore/githib.com/datastx/indeed-scraper')
import os
import subprocess
import webbrowser
from uuid import uuid4

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

new_uuid = lambda: str(uuid4())
# primer values
if "mdf" not in st.session_state:
    st.session_state.mdf = pd.DataFrame(columns=['What','Where','Search'])
if "file_name" not in st.session_state:
    st.session_state.file_name = None



KEYWORD = 'keyword'
LOCATION='location'
PAGE='page'
POSITION ='position'
COMPANY ='company'
JOBKEY = 'jobkey'
JOB_TITLE='jobTitle'
JOB_DESCRIPTION='jobDescription'


ALL_COLUMNS = [KEYWORD,LOCATION,PAGE,POSITION,COMPANY,JOBKEY,JOB_TITLE,JOB_DESCRIPTION]

st.title('Money Gun')





proxy_logs = 'https://scrapeops.io/app/dashboard'
if st.button('Proxy Logs'):
    webbrowser.open_new_tab(proxy_logs)

option = st.selectbox(
    'Select Scraper Engine',
    ['Indeed'])

data = None



col0, col1= st.columns(2)
what= col0.text_input('What')
where = col1.text_input('Where')

find_jobs = st.button('Find Jobs')

df_new = pd.DataFrame({'What': what, 
                            'Where': where, 
                            'Search': f"{what} and {where}", }
                            , index=[0])    

# Critical path for running scrappy    
if find_jobs:
    st.session_state.mdf = pd.concat([st.session_state.mdf, df_new], axis=0)
    what = what.strip()
    where = where.strip()
    # TODO: hack to share streamlit input with scrapy
    os.environ['WHAT'] = what
    os.environ['WHERE'] = where
    call_scrappy = lambda x : f"scrapy crawl indeed_jobs -o {x}"
    st.session_state.file_name = f"{new_uuid()}.csv"
    print(f"file name is {st.session_state.file_name}")
    subprocess.run(call_scrappy(st.session_state.file_name).split(), stdout=subprocess.PIPE).stdout.decode('utf-8')
        

@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


with st.expander(f"See History: count={st.session_state.mdf.shape[0]}"):
    st.dataframe(st.session_state.mdf)

if st.session_state.file_name is not None:
    with st.container():
        st.title('Search Results')
        data = pd.read_csv(st.session_state.file_name,dtype=object)
        st.dataframe(data=data)

        csv = convert_df(data)

        st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name=f'{st.session_state.file_name}.csv',
            mime='text/csv',
        )