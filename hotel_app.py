
import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="Hotel Help Desk Assistant",
    page_icon="🏨",
    layout="centered"
)

# Page title
st.title("🏨 Hotel Help Desk Ticket Classification")
st.write("Enter a guest complaint to identify its category.")

# Ticket input
ticket = st.text_area(
    "Guest Complaint",
    placeholder="Example: My hotel WiFi is not working...",
    height=150
)

# Analyze button
if st.button("Analyze Ticket"):

    if not ticket.strip():
        st.warning("Please enter a guest complaint.")

    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/analyze",
                json={"ticket": ticket},
                timeout=10
            )

            if response.status_code == 200:
                result = response.json()

                st.success("Ticket analyzed successfully!")

                st.subheader("Classification Result")

                st.write("**Category:**", result["category"])
                st.write("**Summary:**", result["summary"])

            else:
                st.error(f"API Error: {response.status_code}")
                st.write(response.text)

        except requests.exceptions.RequestException:
            st.error(
                "Cannot connect to the API. "
                "Please make sure the FastAPI server is running."
            )
