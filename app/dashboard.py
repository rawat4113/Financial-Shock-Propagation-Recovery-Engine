import streamlit as st

def render_dashboard():
    st.title("Financial Shock Propagation & Recovery Engine")
    st.write("Load processed datasets to run shock detection, propagation and recovery scenarios.")
    st.metric("Systemic Risk", "—")
    st.metric("Shock Score", "—")
    st.metric("Expected Recovery", "— days")
