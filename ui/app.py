import streamlit as st
import requests

st.set_page_config(layout="wide")
st.title("Aegis – Intelligent Incident Manager")

incident = st.text_area("Describe the incident")

if st.button("Analyze Incident"):
    response = requests.post(
        "http://localhost:8000/analyze",
        json={"text": incident}
    ).json()

    st.subheader("Incident Understanding")
    st.json(response["parsed_incident"])

    st.subheader("Similar Historical Incidents")
    st.write(response["similar_incidents"])

    st.subheader("Likely Root Cause")
    st.write(response["root_cause"])

    st.subheader("Recommended Actions")
    st.write(response["recommended_actions"])
