import streamlit as st
from api.medical_api import search_medical_info
from config import MEDICAL_DISCLAIMER

def render():
    st.title('🩺 Medical Information')
    st.caption('Search general health information from MedlinePlus.')
    q = st.text_input('Search a health topic', placeholder='e.g. hypertension, asthma, diabetes')
    if st.button('Search', type='primary') and q.strip():
        with st.spinner('Searching...'):
            results = search_medical_info(q)
        if not results: st.warning('No results found or the service is temporarily unavailable.')
        for item in results:
            with st.expander(item['title'] or 'Health topic'):
                st.write(item['summary'])
                if item.get('url'): st.markdown(f"[Open source]({item['url']})")
    st.warning(MEDICAL_DISCLAIMER)
