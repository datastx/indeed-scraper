import re
from typing import Any, List

import pandas as pd
from bs4 import BeautifulSoup
from markdown import markdown


def markdown_to_text(markdown_string):
    """ Converts a markdown string to plaintext """

    # md -> html -> text since BeautifulSoup can extract text cleanly
    html = markdown(markdown_string)

    # remove code snippets
    html = re.sub(r'<pre>(.*?)</pre>', ' ', html)
    html = re.sub(r'<code>(.*?)</code >', ' ', html)

    # extract text
    soup = BeautifulSoup(html, "html.parser")
    text = ''.join(soup.findAll(text=True))

    return text


def remove_markdown(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """_summary_

    Args:
        df (pd.DataFrame): _description_
        columns (List[str]): _description_

    Returns:
        pd.DataFrame: _description_
    """
    for column in columns:
        df[column] = df[column].apply(markdown_to_text)
        
    return df