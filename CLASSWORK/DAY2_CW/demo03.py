import pandas as pd
import streamlit as st

st.title("CSV EXPLORER")

data_file = st.file_uploader("Upload a CSV File", type="csv")

if data_file:
    df = pd.read_csv(data_file)
    st.dataframe(df)