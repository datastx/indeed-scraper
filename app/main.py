import sys

sys.path.append('/Users/brianmoore/githib.com/datastx/indeed-scraper')
from datetime import datetime
import os
import subprocess
import webbrowser
from uuid import uuid4

import pandas as pd
import streamlit as st

new_uuid = lambda: str(uuid4())

INDEED_URL = "https://www.indeed.com/"

# CONSTANTS
KEYWORD = 'keyword'
LOCATION='location'
PAGE='page'
POSITION ='position'
COMPANY ='company'
JOBKEY = 'jobkey'
JOB_TITLE='jobTitle'
JOB_DESCRIPTION='jobDescription'
ALL_COLUMNS = [KEYWORD,LOCATION,PAGE,POSITION,COMPANY,JOBKEY,JOB_TITLE,JOB_DESCRIPTION]

WHAT = 'What'
WHERE = 'Where'
FILE_NAME = 'File Name'
TIME_RAN = 'Time Ran'
ENGINE = 'Engine'
ALL_SEARCH_HISTORY_COLUMNS =[WHAT, WHERE, FILE_NAME, TIME_RAN, ENGINE]

# primer values
if "mdf" not in st.session_state:
    st.session_state.mdf = pd.DataFrame(columns=ALL_SEARCH_HISTORY_COLUMNS)
if "file_name" not in st.session_state:
    st.session_state.file_name = None



st.markdown("<h1 style='text-align: center; color: red;'>Money Gun</h1>", unsafe_allow_html=True)
st.markdown("<h6 style='text-align: center; color: grey;'>version 1.0</h1>", unsafe_allow_html=True)



engine_option = st.selectbox(
    'Select Scraper Engine',
    ['Indeed'])


def add_csv_ext(str_obj: str) -> str:
    return f"{str_obj}.csv"


col0, col1= st.columns(2)
what= col0.text_input(WHAT)
where = col1.text_input(WHERE)


but1, but2 = st.columns([1,1])
with but1:
    find_jobs = st.button('Find Jobs')
with but2:
    proxy_logs = 'https://scrapeops.io/app/dashboard'
    if st.button('Proxy Logs'):
        webbrowser.open_new_tab(proxy_logs)



# Critical path for running scrapy    
if find_jobs:
    st.session_state.file_name = add_csv_ext(new_uuid())
    print(f"file name is {st.session_state.file_name}")
    df_new = pd.DataFrame({WHAT: what, 
                            WHERE: where, 
                            FILE_NAME: st.session_state.file_name,
                            TIME_RAN: datetime.now() ,
                            ENGINE: engine_option}
                            , index=[0])    
    st.session_state.mdf = pd.concat([st.session_state.mdf, df_new], axis=0)
    what = what.strip()
    where = where.strip()
    # TODO: hack to share streamlit input with scrapy
    os.environ[WHAT.upper()] = what
    os.environ[WHERE.upper()] = where
    call_scrappy = lambda x : f"scrapy crawl indeed_jobs -o {x}"
    subprocess.run(call_scrappy(st.session_state.file_name).split(), stdout=subprocess.PIPE).stdout.decode('utf-8')
        


@st.cache
def convert_df(df: pd.DataFrame) -> pd.DataFrame:
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode('utf-8')


with st.expander(f"See History: count={st.session_state.mdf.shape[0]}"):
    st.dataframe(st.session_state.mdf)

if st.session_state.file_name is not None:
    with st.container():
        st.title('Search Results')
        try:
            data = pd.read_csv(st.session_state.file_name,dtype=object)
            st.dataframe(data=data)

            csv = convert_df(data)

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=st.session_state.file_name,
                mime='text/csv',
            )
        except pd.errors.EmptyDataError:
            st.error(f'We did not get any results from indeed for your query. Check indeeds site to make sure Money Gun is working. {INDEED_URL}', icon="🚨")
