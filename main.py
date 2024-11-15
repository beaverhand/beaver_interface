import streamlit as st
from app.bulk_loader import bulk_loader_page
# from app.ad_hoc_loader import ad_hoc_loader_page
# from app.top_match import top_match_page

st.set_page_config(page_title="Candidate Matcher", layout="wide")

PAGES = {
    "Bulk Loader": bulk_loader_page,
    # "Ad-hoc Loader": ad_hoc_loader_page,
    # "Top Match": top_match_page,
}

st.sidebar.title('Navigation')
selection = st.sidebar.radio("Go to", list(PAGES.keys()))
page = PAGES[selection]
page()