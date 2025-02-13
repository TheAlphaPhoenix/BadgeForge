import streamlit as st
import streamlit.components.v1 as components
from datetime import date
import urllib.parse
import pandas as pd

st.title("BadgeForge - Professional Achievement Badge Generator")

# ----- User Input Section -----
st.header("Enter Achievement Details")
recipient_name = st.text_input("Recipient Name")

# Define achievement categories and specific achievements
achievements_dict = {
    "Reading Progress Milestones": [
        "Started first book",
        "Completed 1 book",
        "Completed 5 books",
        "Completed 10 books",
        "Completed 20 books"
    ],
    "Volunteer Milestones": [
        "Completed 10 Hours Community Service",
        "Completed 25 Hours Mentoring",
        "Completed 50 Hours Social Impact",
        "Volunteer of the Month"
    ],
    "Pharmacy Informatics APPE Rotations": [
        "Completed Basic Informatics Rotation",
        "Completed Advanced Informatics Rotation",
        "Completed Informatics Research Project",
        "Exemplary Performance in APPE Rotation"
    ],
    "Well-being Initiatives": [
        "Well-being Book Club Participation",
        "Mindfulness Program Completion",
        "Health & Wellness Champion"
    ]
}

categories = list(achievements_dict.keys())
category = st.selectbox("Achievement Category", categories)
achievement = st.selectbox("Select Specific Achievement", achievements_dict[category])

issue_date = st.date_input("Issue Date", date.today())
notes = st.text_area("Optional Notes or Evidence")
evidence = st.file_uploader("Upload Evidence (optional)", type=["jpg", "png", "pdf"])

# ----- Badge Generation and Preview -----
if st.button("Generate Badge"):
    if not recipient_name:
        st.error("Please enter a recipient name.")
    else:
        # Generate QR code URL using an online service.
        qr_data = f"Name: {recipient_name}\nAchievement: {achievement}\nDate: {issue_date}"
        qr_encoded = urllib.parse.quote(qr_data)
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?data={qr_encoded}&size=100x100"

        # Create the circular badge as an HTML string with a modern and sleek design.
        badge_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <title>Achievement Badge</title>
          <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500&family=Great+Vibes&display=swap" rel="stylesheet">
          <style>
            body {{
              background-color: #f9f9f9;
              margin: 0;
              padding: 0;
              display: flex;
              justify-content: center;
              align-items: center;
              height: 100vh;
              font-family: 'Roboto', sans-serif;
            }}
            .badge {{
              width: 400px;
              height: 400px;
              border-radius: 50%;
              background: linear-gradient(135deg, #1F2937, #4B5563);
              position: relative;
              box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
              display: flex;
              flex-direction: column;
              align-item



