import streamlit as st
import pandas as pd
import user_db

st.set_page_config(page_title="Admin Dashboard", layout="wide")

if "admin" not in st.session_state:
    st.session_state.admin = None

def login_form():
    with st.form("Login Admin"):
        uname = st.text_input("Username")
        pwd = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")
        if submitted and user_db.auth_admin(uname, pwd):
            st.session_state.admin = uname
            user_db.log_login(uname)

if not st.session_state.admin:
    login_form()
else:
    st.sidebar.success(f"Login sebagai: {st.session_state.admin}")
    tab = st.sidebar.selectbox("Menu", ["User", "Log", "Reset PIN", "Logout"])
    
    if tab == "User":
        df = user_db.load_users()
        st.dataframe(df)

    elif tab == "Log":
        logs = user_db.load_logs()
        filter_name = st.text_input("Cari Nama")
        if filter_name:
            logs = logs[logs['user'].str.contains(filter_name, case=False)]
        st.dataframe(logs)
        if st.button("Export CSV"):
            logs.to_csv("logs.csv", index=False)
            st.success("Log diekspor!")

    elif tab == "Reset PIN":
        user = st.text_input("Nama user")
        new_pin = st.text_input("PIN Baru", type="password")
        if st.button("Reset PIN"):
            user_db.reset_pin(user, new_pin)
            st.success("PIN direset")

    elif tab == "Logout":
        st.session_state.admin = None
