import os
import subprocess
import webbrowser
from datetime import datetime
from uuid import uuid4

import pandas as pd
import streamlit as st
import streamlit_toggle as tog

new_uuid = lambda: str(uuid4())

INDEED_URL = "https://www.indeed.com/"

# CONSTANTS
KEYWORD = "keyword"
LOCATION = "location"
PAGE = "page"
POSITION = "position"
COMPANY = "company"
JOBKEY = "jobkey"
JOB_TITLE = "jobTitle"
JOB_DESCRIPTION = "jobDescription"
ALL_COLUMNS = [
    KEYWORD,
    LOCATION,
    PAGE,
    POSITION,
    COMPANY,
    JOBKEY,
    JOB_TITLE,
    JOB_DESCRIPTION,
]

WHAT = "What"
WHERE = "Where"
FILE_NAME = "File Name"
TIME_RAN = "Time Ran"
ENGINE = "Engine"
ALL_SEARCH_HISTORY_COLUMNS = [WHAT, WHERE, FILE_NAME, TIME_RAN, ENGINE]


MONEY_GUN = "Money Gun"
ZOOM_INFO = "Zoom Info"
HUB_SPOT = "Hub Spot"

ALL_NAVIATION_OPTIONS = [MONEY_GUN, ZOOM_INFO, HUB_SPOT]


def add_csv_ext(str_obj: str) -> str:
    return f"{str_obj}.csv"


# primer values
if "mdf" not in st.session_state:
    st.session_state.mdf = pd.DataFrame(columns=ALL_SEARCH_HISTORY_COLUMNS)
if "file_name" not in st.session_state:
    st.session_state.file_name = None


st.markdown(
    "<h1 style='text-align: center; color: red;'>Money Gun</h1>", unsafe_allow_html=True
)
st.markdown(
    "<h6 style='text-align: center; color: grey;'>version 1.1</h1>",
    unsafe_allow_html=True,
)

engine_option = st.selectbox("Select Scraper Engine", ["Indeed"])

col0, col1 = st.columns(2)
what = col0.text_input(WHAT)
where = col1.text_input(WHERE)
with st.expander(f"Advanced search options"):
    st.error(
        "each page has ~15 records and runs this inequality...Start Page <= n < End Page"
    )
    start_page = st.number_input("Start Page:(inclusive)", value=1, step=1)
    end_page = st.number_input("End Page:(exclusive)", value=2, step=1)
    sort_by = tog.st_toggle_switch(
        label="Date",
        key="Key1",
        default_value=True,
        label_after=True,
        inactive_color="#D3D3D3",
        active_color="white",
        track_color="red",
    )
number_of_pages = end_page - start_page

write1, write2, write3, write4 = st.columns([1, 1, 1,1])
with write1:
    st.write("start page:", start_page)
with write2:
    st.write("end page:", end_page)
with write3:
    st.write(f"Number of pages:", number_of_pages)
with write4:
    st.write("Sort By Date:", sort_by)


but1, but2 = st.columns([1, 1])
with but1:
    if number_of_pages < 1:
        st.error(f"You cannot submit a request for {number_of_pages} pages", icon="🚨")
    else:
        find_jobs = st.button("Find Jobs")
with but2:
    proxy_logs = tog.st_toggle_switch(
        label="Proxy Logs",
        key="Proxy Logs",
        default_value=False,
        label_after=True,
        inactive_color="#D3D3D3",
        active_color="white",
        track_color="red",
    )
    if proxy_logs:
        # Hack to get the link to work atm
        proxy_logs_link = "https://scrapeops.io/app/dashboard"
        st.markdown(proxy_logs_link, unsafe_allow_html=True)




# Critical path for running scrapy
if find_jobs:
    st.session_state.file_name = add_csv_ext(new_uuid())
    print(f"file name is {st.session_state.file_name}")
    df_new = pd.DataFrame(
        {
            WHAT: what,
            WHERE: where,
            FILE_NAME: st.session_state.file_name,
            TIME_RAN: datetime.now(),
            ENGINE: engine_option,
        },
        index=[0],
    )
    st.session_state.mdf = pd.concat([st.session_state.mdf, df_new], axis=0)
    what = what.strip()
    where = where.strip()
    # TODO: hack to share streamlit input with scrapy
    os.environ[WHAT.upper()] = what
    os.environ[WHERE.upper()] = where
    os.environ["START_PAGE"] = str(start_page)
    os.environ["END_PAGE"] = str(end_page)
    call_scrappy = lambda x: f"scrapy crawl indeed_jobs -o {x}"
    subprocess.run(
        call_scrappy(st.session_state.file_name).split(), stdout=subprocess.PIPE
    ).stdout.decode("utf-8")


@st.cache
def convert_df(df: pd.DataFrame) -> pd.DataFrame:
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv().encode("utf-8")


with st.expander(f"See History: count={st.session_state.mdf.shape[0]}"):
    st.dataframe(st.session_state.mdf)

if st.session_state.file_name is not None:
    with st.container():
        st.title("Search Results")
        try:
            data = pd.read_csv(st.session_state.file_name, dtype=object)
            st.dataframe(data=data)

            csv = convert_df(data)

            st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=st.session_state.file_name,
                mime="text/csv",
            )
        except pd.errors.EmptyDataError:
            st.error(
                f"We did not get any results from indeed for your query. Check indeeds site to make sure Money Gun is working. {INDEED_URL}",
                icon="🚨",
            )
