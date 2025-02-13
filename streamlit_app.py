import streamlit as st
import streamlit.components.v1 as components
import streamlit_authenticator as stauth
import pandas as pd
from datetime import date
from PIL import Image, ImageDraw, ImageFont
import qrcode
import io

# ----- Basic Authentication Setup -----
# For demonstration, we create a single user.
names = ["John Doe"]
usernames = ["johndoe"]
# In a production app, NEVER store plaintext passwords.
passwords = ["password"]  
hashed_passwords = stauth.Hasher(passwords).generate()

credentials = {
    "usernames": {
        usernames[0]: {
            "name": names[0],
            "password": hashed_passwords[0]
        }
    }
}

authenticator = stauth.Authenticate(credentials, "badgeforge_cookie", "badgeforge_key", cookie_expiry_days=1)
name, authentication_status, username = authenticator.login("Login", "main")

if st.session_state.get("authentication_status"):
    st.title("BadgeForge - Professional Achievement Badge Generator")
    st.write("Welcome,", st.session_state["name"])

    # ----- User Input Section -----
    st.header("Enter Achievement Details")
    recipient_name = st.text_input("Recipient Name")
    
    achievement_categories = ["Reading", "Volunteer Work", "Well-being"]
    category = st.selectbox("Achievement Category", achievement_categories)
    
    # Define specific achievements for each category
    achievements_dict = {
        "Reading": [
            "10 Leadership Books (Annual)",
            "20 Professional Development Books",
            "Book Club Leadership"
        ],
        "Volunteer Work": [
            "10 Hours Community Service",
            "25 Hours Mentoring",
            "50 Hours Social Impact"
        ],
        "Well-being": [
            "Well-being Book Club Participation",
            "Mindfulness Program Completion",
            "Health & Wellness Champion"
        ]
    }
    achievement = st.selectbox("Select Specific Achievement", achievements_dict[category])
    
    issue_date = st.date_input("Issue Date", date.today())
    
    notes = st.text_area("Optional Notes or Evidence")
    evidence = st.file_uploader("Upload Evidence (optional)", type=["jpg", "png", "pdf"])
    
    # ----- Badge Generation -----
    if st.button("Generate Badge"):
        try:
            # Validate required inputs
            if not recipient_name:
                st.error("Please enter a recipient name.")
            else:
                # --- Generate QR Code for verification ---
                qr_data = f"Name: {recipient_name}\nAchievement: {achievement}\nDate: {issue_date}"
                qr = qrcode.QRCode(box_size=2, border=2)
                qr.add_data(qr_data)
                qr.make(fit=True)
                qr_img = qr.make_image(fill_color="black", back_color="white")
                qr_buffer = io.BytesIO()
                qr_img.save(qr_buffer, format="PNG")
                qr_buffer.seek(0)
                qr_img = Image.open(qr_buffer)
                
                # --- Create the Certificate/Badge Image ---
                cert_width, cert_height = (800, 600)
                certificate = Image.new("RGB", (cert_width, cert_height), color="white")
                draw = ImageDraw.Draw(certificate)
                
                # Draw an official-looking gold border
                border_color = "gold"
                border_width = 10
                for i in range(border_width):
                    draw.rectangle([i, i, cert_width - i - 1, cert_height - i - 1], outline=border_color)
                
                # Draw a dark-blue header with a title (blue and gold color scheme)
                header_height = 100
                draw.rectangle([0, 0, cert_width, header_height], fill="#003366")
                title_text = "Certificate of Achievement"
                try:
                    title_font = ImageFont.truetype("arial.ttf", 40)
                except:
                    title_font = ImageFont.load_default()
                title_w, title_h = draw.textsize(title_text, font=title_font)
                draw.text(((cert_width - title_w) / 2, (header_height - title_h) / 2),
                          title_text, fill="gold", font=title_font)
                
                # Display the recipient's name in a calligraphy-like style if available
                try:
                    # Make sure to have the font file (e.g., GreatVibes-Regular.ttf) in your working directory
                    recipient_font = ImageFont.truetype("GreatVibes-Regular.ttf", 50)
                except:
                    recipient_font = ImageFont.truetype("arial.ttf", 50) if "arial.ttf" in ImageFont.getfont("arial.ttf").path else ImageFont.load_default()
                rec_text = recipient_name
                rec_w, rec_h = draw.textsize(rec_text, font=recipient_font)
                draw.text(((cert_width - rec_w) / 2, header_height + 50),
                          rec_text, fill="#003366", font=recipient_font)
                
                # Add achievement details below the name
                detail_text = f"has been recognized for {achievement}."
                try:
                    detail_font = ImageFont.truetype("arial.ttf", 30)
                except:
                    detail_font = ImageFont.load_default()
                detail_w, detail_h = draw.textsize(detail_text, font=detail_font)
                draw.text(((cert_width - detail_w) / 2, header_height + 120),
                          detail_text, fill="black", font=detail_font)
                
                # Add issue date near the bottom
                date_text = f"Issued on: {issue_date.strftime('%B %d, %Y')}"
                try:
                    date_font = ImageFont.truetype("arial.ttf", 20)
                except:
                    date_font = ImageFont.load_default()
                date_w, date_h = draw.textsize(date_text, font=date_font)
                draw.text(((cert_width - date_w) / 2, cert_height - 80),
                          date_text, fill="black", font=date_font)
                
                # Resize and paste the QR code at bottom-right
                qr_size = 100
                qr_img = qr_img.resize((qr_size, qr_size))
                certificate.paste(qr_img, (cert_width - qr_size - 20, cert_height - qr_size - 20))
                
                # --- Prepare the Certificate for Download ---
                # Convert certificate to PNG bytes
                png_buffer = io.BytesIO()
                certificate.save(png_buffer, format="PNG")
                png_data = png_buffer.getvalue()
                
                # Convert certificate to PDF bytes using Pillow (requires Pillow >= 9.1)
                pdf_buffer = io.BytesIO()
                certificate.save(pdf_buffer, format="PDF")
                pdf_data = pdf_buffer.getvalue()
                
                st.success("Badge generated successfully!")
                
                # Show preview
                st.image(certificate, caption="Badge Preview", use_column_width=True)
                
                # ----- Export Options -----
                st.download_button("Download as PNG", data=png_data, file_name="badge.png", mime="image/png")
                st.download_button("Download as PDF", data=pdf_data, file_name="badge.pdf", mime="application/pdf")
                st.markdown("[Share your badge](https://example.com/share_badge)", unsafe_allow_html=True)
                
                # ----- Achievement Tracking Dashboard -----
                if "achievements_df" not in st.session_state:
                    st.session_state["achievements_df"] = pd.DataFrame(columns=["Name", "Achievement", "Issue Date"])
                new_entry = {"Name": recipient_name, "Achievement": achievement, "Issue Date": issue_date.strftime("%Y-%m-%d")}
                st.session_state["achievements_df"] = st.session_state["achievements_df"].append(new_entry, ignore_index=True)
        except Exception as e:
            st.error(f"Error generating badge: {e}")
    
    st.header("Achievement Tracking Dashboard")
    if "achievements_df" in st.session_state and not st.session_state["achievements_df"].empty:
        st.dataframe(st.session_state["achievements_df"])
    else:
        st.info("No achievements generated yet.")
    
    # Logout button
    authenticator.logout("Logout", "main")

elif st.session_state.get("authentication_status") is False:
    st.error("Username/password is incorrect")
elif st.session_state.get("authentication_status") is None:
    st.warning("Please enter your username and password")
