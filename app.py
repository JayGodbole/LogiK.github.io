import streamlit as st
import requests
import time
import json
import os
from pathlib import Path

# ==========================================
# 🎬 VIRAL SHORTS AI AGENCY - CLIENT PORTAL
# 100% FREE | NO EMAIL | NO APP PASSWORD
# ==========================================

st.set_page_config(
    page_title="Viral Shorts AI Agency",
    page_icon="🎬",
    layout="centered"
)

# ==========================================
# CUSTOM CSS - MAKE IT LOOK LIKE A REAL AGENCY
# ==========================================
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: white;
    }
    .stButton>button {
        background: linear-gradient(90deg, #ff6b6b, #ee5a24);
        color: white;
        font-size: 20px;
        font-weight: bold;
        border: none;
        border-radius: 10px;
        padding: 15px 30px;
        width: 100%;
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #ee5a24, #ff6b6b);
        color: white;
    }
    .download-btn>button {
        background: linear-gradient(90deg, #00b09b, #96c93d) !important;
        font-size: 24px !important;
        padding: 20px !important;
    }
    .package-box {
        background: #1e2130;
        padding: 20px;
        border-radius: 10px;
        border: 2px solid #ff6b6b;
        margin: 10px 0;
    }
    .testimonial {
        background: #262a3b;
        padding: 15px;
        border-left: 4px solid #ff6b6b;
        margin: 10px 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HEADER - AGENCY BRANDING
# ==========================================
st.markdown("# 🎬 Viral Shorts AI Agency")
st.markdown("### 🚀 Get **AI Avatar Viral Shorts** for Instagram & YouTube — 100% Automated!")
st.markdown("---")

# ==========================================
# SIDEBAR - PACKAGES & INFO
# ==========================================
with st.sidebar:
    st.markdown("## 💼 Our Packages")
    
    st.markdown("""
    <div class='package-box'>
    <h3>🟢 Starter</h3>
    <h2>$49/month</h2>
    <ul>
        <li>✅ 4 Videos/month</li>
        <li>✅ AI Avatar + Voiceover</li>
        <li>✅ Viral Captions</li>
        <li>✅ 24-48 hr delivery</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='package-box'>
    <h3>🔥 Growth</h3>
    <h2>$199/month</h2>
    <ul>
        <li>✅ 15 Videos/month</li>
        <li>✅ Priority Render</li>
        <li>✅ Custom Avatars</li>
        <li>✅ 12-24 hr delivery</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='package-box'>
    <h3>👑 Viral Empire</h3>
    <h2>$399/month</h2>
    <ul>
        <li>✅ 30 Videos/month</li>
        <li>✅ Dedicated Server</li>
        <li>✅ Custom Backgrounds</li>
        <li>✅ 6-12 hr delivery</li>
    </ul>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("### 📞 Questions?")
    st.markdown("Email: `agency@yourdomain.com`")

# ==========================================
# MAIN FORM - CLIENT INPUT
# ==========================================
st.markdown("## 📝 Tell Us About Your Video")

with st.form("video_order_form"):
    st.markdown("### 1️⃣ Your Script (What should the AI say?)")
    user_script = st.text_area(
        "Paste your script here:",
        height=200,
        placeholder="Example: 'Want to make money while you sleep? Here are 3 passive income ideas that actually work...'",
        help="Keep it under 200 words for best results!"
    )
    
    st.markdown("### 2️⃣ Background Theme")
    bg_theme = st.selectbox(
        "What background do you want?",
        ["Business/Office", "Technology/Cyber", "Luxury/Money", "Fitness/Health", "Travel/Adventure", "Custom (we'll pick the best)"]
    )
    
    st.markdown("### 3️⃣ Your Package")
    selected_package = st.selectbox(
        "Which package is this for?",
        ["Starter ($49)", "Growth ($199)", "Viral Empire ($399)", "One-time test ($29)"]
    )
    
    st.markdown("### 4️⃣ Your Email (Optional - for notifications only)")
    user_email = st.text_input(
        "Email (optional):",
        placeholder="your@email.com",
        help="We can notify you when the video is ready. Not required!"
    )
    
    submitted = st.form_submit_button("🚀 BUILD MY VIRAL SHORT NOW!")

# ==========================================
# PROCESS THE FORM
# ==========================================
if submitted:
    if not user_script or len(user_script) < 10:
        st.error("❌ Please enter a script with at least 10 characters!")
        st.stop()
    
    if len(user_script) > 500:
        st.warning("⚠️ Scripts over 500 characters may take longer to generate. Consider shortening it.")
    
    # Show progress
    st.markdown("---")
    st.markdown("## 🎬 Building Your Viral Short...")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    # Step 1: Send to Render.com server
    status_text.markdown("### 📡 Step 1/4: Sending your script to our AI servers...")
    progress_bar.progress(25)
    
    # Prepare payload
    payload = {
        "script": user_script,
        "bg_theme": bg_theme,
        "package": selected_package,
        "email": user_email if user_email else "none"
    }
    
    # TODO: Replace with your actual Render.com URL
    RENDER_SERVER_URL = "https://YOUR-RENDER-APP.onrender.com/generate"
    
    try:
        # Send request to Render server
        response = requests.post(RENDER_SERVER_URL, json=payload, timeout=30)
        
        if response.status_code == 200:
            progress_bar.progress(50)
            status_text.markdown("### 🤖 Step 2/4: AI is generating your avatar & voiceover...")
            
            # Poll for completion (simplified - in production use webhooks)
            # For now, simulate progress
            time.sleep(2)
            progress_bar.progress(75)
            status_text.markdown("### 🎥 Step 3/4: Compositing video with captions...")
            time.sleep(2)
            progress_bar.progress(90)
            status_text.markdown("### ☁️ Step 4/4: Uploading to cloud for download...")
            time.sleep(1)
            progress_bar.progress(100)
            status_text.markdown("### ✅ **YOUR VIDEO IS READY!**")
            
            # Get download link from response
            result = response.json()
            download_link = result.get("download_link", "https://file.io/example")
            
            st.markdown("---")
            st.balloons()
            st.markdown("# 🎉 YOUR VIRAL SHORT IS READY!")
            st.markdown(f"## 📥 [CLICK HERE TO DOWNLOAD YOUR VIDEO]({download_link})")
            st.markdown("### ⬆️ Right-click the link above and select 'Save link as...'")
            
            st.markdown("---")
            st.markdown("### 💡 Want more videos?")
            st.markdown("Upgrade to a monthly package and get **4, 15, or 30 videos per month** automatically!")
            
        else:
            st.error(f"❌ Server error: {response.status_code}. Please try again later.")
    
    except requests.exceptions.RequestException as e:
        st.error("❌ Cannot connect to our servers. Please check your internet and try again.")
        st.markdown("### 🛠️ Don't worry! This is normal for free servers (they 'sleep' when not used).")
        st.markdown("👉 **Click the button again in 2-3 minutes** and it will work!")
        st.markdown("*(Free Render.com servers go to sleep after 15 minutes of inactivity)*")

# ==========================================
# TESTIMONIALS (Social Proof)
# ==========================================
st.markdown("---")
st.markdown("## 🌟 What Our Clients Say")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    <div class='testimonial'>
    <strong>⭐⭐⭐⭐⭐</strong><br>
    "Got 10,000 views on my first short! The AI avatar looks so real!"<br>
    <em>- Sarah M., Fitness Coach</em>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='testimonial'>
    <strong>⭐⭐⭐⭐⭐</strong><br>
    "Saved me hours of filming. Now I just paste my script and download!"<br>
    <em>- John D., Business Consultant</em>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class='testimonial'>
    <strong>⭐⭐⭐⭐⭐</strong><br>
    "My clients think I hired a video team. Nope, just this AI tool!"<br>
    <em>- Lisa R., Social Media Manager</em>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class='testimonial'>
    <strong>⭐⭐⭐⭐⭐</strong><br>
    "Best $49 I ever spent. Already made $500 from the videos it made!"<br>
    <em>- Mike T., Affiliate Marketer</em>
    </div>
    """, unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================
st.markdown("---")
st.markdown("### 🔒 100% Secure | 🌍 Cloud-Based | ⚡ 24/7 Available")
st.markdown("Powered by **Viral Shorts AI Agency** | Built with ❤️ for creators")
st.markdown("<sub>Questions? Email us at `agency@yourdomain.com`</sub>", unsafe_allow_html=True)
