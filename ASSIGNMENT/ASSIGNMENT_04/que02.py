import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Files
if not os.path.exists("users.csv"):
    pd.DataFrame(columns=["user", "pass"]).to_csv("users.csv", index=False)

if not os.path.exists("userfiles.csv"):
    pd.DataFrame(columns=["user", "file", "time"]).to_csv("userfiles.csv", index=False)

# Session
if "user" not in st.session_state:
    st.session_state.user = None

# Menu
if st.session_state.user is None:
    menu = st.sidebar.selectbox("Menu", ["Home", "Login", "Register"])
else:
    menu = st.sidebar.selectbox("Menu", ["Explore CSV", "See History", "Logout"])

# Pages
if menu == "Home":
    st.write("Home")

elif menu == "Register":
    u = st.text_input("User")
    p = st.text_input("Pass", type="password")
    if st.button("Register"):
        df = pd.read_csv("users.csv")
        df.loc[len(df)] = [u, p]
        df.to_csv("users.csv", index=False)

elif menu == "Login":
    u = st.text_input("User")
    p = st.text_input("Pass", type="password")
    if st.button("Login"):
        df = pd.read_csv("users.csv")
        if ((df.user == u) & (df["pass"] == p)).any():
            st.session_state.user = u
            st.rerun()

elif menu == "Explore CSV":
    f = st.file_uploader("Upload CSV", type="csv")
    if f:
        st.dataframe(pd.read_csv(f))
        h = pd.read_csv("userfiles.csv")
        h.loc[len(h)] = [st.session_state.user, f.name, datetime.now()]
        h.to_csv("userfiles.csv", index=False)

elif menu == "See History":
    h = pd.read_csv("userfiles.csv")
    st.dataframe(h[h.user == st.session_state.user])

elif menu == "Logout":
    st.session_state.user = None
    st.rerun()
