import streamlit as st
import streamlit.components.v1 as components
from datetime import date
import urllib.parse
import pandas as pd

st.title("BadgeForge - Professional Achievement Badge Generator")

# Achievement categories and specific achievements
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

# User Input Section
st.header("Enter Achievement Details")
recipient_name = st.text_input("Recipient Name")
categories = list(achievements_dict.keys())
category = st.selectbox("Achievement Category", categories)
achievement = st.selectbox("Select Specific Achievement", achievements_dict[category])
issue_date = st.date_input("Issue Date", date.today())
notes = st.text_area("Optional Notes or Evidence")

if st.button("Generate Badge"):
    if not recipient_name:
        st.error("Please enter a recipient name.")
    else:
        # Generate QR code URL
        qr_data = "Name: " + recipient_name + "\nAchievement: " + achievement + "\nDate: " + str(issue_date)
        qr_encoded = urllib.parse.quote(qr_data)
        qr_url = "https://api.qrserver.com/v1/create-qr-code/?data=" + qr_encoded + "&size=100x100"

        # Create HTML content
        html_content = """
            <div style="
                max-width: 600px;
                margin: 20px auto;
                padding: 20px;
                border: 2px solid #1F2937;
                border-radius: 10px;
                text-align: center;
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #1F2937, #4B5563);
                color: white;
            ">
                <h1 style="
                    font-size: 24px;
                    margin-bottom: 20px;
                    color: white;
                ">Achievement Badge</h1>
                <div style="
                    font-size: 32px;
                    margin-bottom: 15px;
                    font-family: 'Times New Roman', serif;
                    color: #FFD700;
                ">{}</div>
                <div style="
                    font-size: 20px;
                    margin-bottom: 15px;
                ">{}</div>
                <div style="
                    font-size: 18px;
                    margin-bottom: 15px;
                    font-style: italic;
                ">{}</div>
                <div style="
                    font-size: 16px;
                    margin-bottom: 15px;
                ">Issued on: {}</div>
                <div style="
                    font-size: 14px;
                    margin-bottom: 20px;
                ">{}</div>
                <img src="{}" alt="QR Code" style="
                    width: 100px;
                    height: 100px;
                    border: 2px solid white;
                    border-radius: 10px;
                ">
            </div>
        """.format(
            recipient_name,
            achievement,
            category,
            issue_date.strftime("%B %d, %Y"),
            notes if notes else "",
            qr_url
        )

        # Display badge
        st.success("Badge generated successfully!")
        components.html(html_content, height=600)

        # Save to achievements list
        if "achievements" not in st.session_state:
            st.session_state["achievements"] = []
        
        st.session_state["achievements"].append({
            "Name": recipient_name,
            "Category": category,
            "Achievement": achievement,
            "Issue Date": issue_date.strftime("%Y-%m-%d")
        })

        # Add download button
        st.download_button(
            "Download Badge as HTML",
            html_content,
            file_name="badge.html",
            mime="text/html"
        )

# Display Achievement Dashboard
st.header("Achievement Tracking Dashboard")
if "achievements" in st.session_state and st.session_state["achievements"]:
    df = pd.DataFrame(st.session_state["achievements"])
    st.dataframe(df)
else:
    st.info("No achievements generated yet.")



