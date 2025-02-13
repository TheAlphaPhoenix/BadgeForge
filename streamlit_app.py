import streamlit as st
import streamlit.components.v1 as components
from datetime import date
import urllib.parse
import pandas as pd

st.title("BadgeForge - Professional Achievement Badge Generator")

# ----- User Input Section -----
st.header("Enter Achievement Details")
recipient_name = st.text_input("Recipient Name")

# New achievement categories
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

# Create a list of categories based on the keys of the achievements_dict
categories = list(achievements_dict.keys())
category = st.selectbox("Achievement Category", categories)

# Specific achievement selection based on chosen category
achievement = st.selectbox("Select Specific Achievement", achievements_dict[category])

issue_date = st.date_input("Issue Date", date.today())
notes = st.text_area("Optional Notes or Evidence")
evidence = st.file_uploader("Upload Evidence (optional)", type=["jpg", "png", "pdf"])

# ----- Badge Generation and Preview -----
if st.button("Generate Certificate"):
    if not recipient_name:
        st.error("Please enter a recipient name.")
    else:
        # Generate QR code URL using an online service.
        qr_data = f"Name: {recipient_name}\nAchievement: {achievement}\nDate: {issue_date}"
        qr_encoded = urllib.parse.quote(qr_data)
        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?data={qr_encoded}&size=100x100"

        # Create the certificate as an HTML string.
        certificate_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
          <meta charset="UTF-8">
          <title>Certificate of Achievement</title>
          <link href="https://fonts.googleapis.com/css2?family=Great+Vibes&display=swap" rel="stylesheet">
          <style>
            body {{
              font-family: Arial, sans-serif;
              text-align: center;
              margin: 0;
              padding: 0;
              background-color: #f0f0f0;
            }}
            .certificate {{
              width: 800px;
              height: 600px;
              background-color: white;
              border: 10px solid gold;
              margin: 20px auto;
              padding: 20px;
              position: relative;
              box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }}
            .header {{
              background-color: #003366;
              color: gold;
              padding: 20px;
              font-size: 36px;
            }}
            .recipient {{
              font-family: 'Great Vibes', cursive;
              font-size: 48px;
              margin: 30px 0;
              color: #003366;
            }}
            .details {{
              font-size: 24px;
              margin: 20px 0;
            }}
            .footer {{
              position: absolute;
              bottom: 20px;
              width: 100%;
              font-size: 16px;
            }}
            .qr-code {{
              position: absolute;
              bottom: 20px;
              right: 20px;
            }}
          </style>
        </head>
        <body>
          <div class="certificate">
            <div class="header">Certificate of Achievement</div>
            <div class="recipient">{recipient_name}</div>
            <div class="details">
              has been recognized for <strong>{achievement}</strong> in the category <strong>{category}</strong>.<br>
              Issued on: {issue_date.strftime('%B %d, %Y')}
            </div>
            <div class="footer">
              {notes if notes else ""}
            </div>
            <div class="qr-code">
              <img src="{qr_url}" alt="QR Code">
            </div>
          </div>
        </body>
        </html>
        """
        st.success("Certificate generated successfully!")

        # Preview the certificate in the app.
        components.html(certificate_html, height=650, scrolling=True)

        # ----- Export Options -----
        # Download the certificate as an HTML file.
        st.download_button("Download Certificate as HTML",
                           certificate_html,
                           file_name="certificate.html",
                           mime="text/html")

        # ----- Achievement Tracking Dashboard -----
        if "achievements" not in st.session_state:
            st.session_state["achievements"] = []
        st.session_state["achievements"].append({
            "Name": recipient_name,
            "Category": category,
            "Achievement": achievement,
            "Issue Date": issue_date.strftime("%Y-%m-%d")
        })

# ----- Achievement Tracking Dashboard Display -----
st.header("Achievement Tracking Dashboard")
if "achievements" in st.session_state and st.session_state["achievements"]:
    df = pd.DataFrame(st.session_state["achievements"])
    st.dataframe(df)
else:
    st.info("No achievements generated yet.")

