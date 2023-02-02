import streamlit as st
import pandas as pd

# "scrapy crawl indeed_jobs -o indeed_jobs_data.csv"
call_scrappy = lambda x : f"scrapy crawl indeed_jobs -o x"



def main():
    st.title('Search Indeed')
    search = st.text_input('Be sure to seperate what ";" and where')
    if search:
        what, where = search.split(';')
        what = what.strip()
        where = where.strip()
        df = pd.read_csv('indeed_jobs_data.csv',dtype=object)
        st.dataframe(df)

if __name__ == '__main__':
    main()
