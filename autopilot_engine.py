#!/usr/bin/env python3
"""
🤖 REAL PRODUCTION AUTOMATED VIDEO GENERATOR
=============================================
✅ 100% FREE (no paid APIs)
✅ NO EMAIL NEEDED (no App Password)
✅ Uploads to free cloud host → returns download link
✅ Client downloads directly from the site

REPLACES EMAIL WITH DIRECT DOWNLOAD LINK!
"""

import os
import sys
import time
import json
import requests
from pathlib import Path
from flask import Flask, request, jsonify

# ==========================================
# ENVIRONMENT VARIABLES (Set in Render.com)
# ==========================================
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "YOUR_PEXELS_API_KEY_HERE")

# ==========================================
# FLASK APP FOR WEBHOOK / API
# ==========================================
app = Flask(__name__)

# ==========================================
# STEP 1: TEXT-TO-SPEECH (Free edge-tts)
# ==========================================
def generate_voiceover(script_text, output_path="voiceover.mp3"):
    """Generate AI voiceover using free edge-tts (no API key needed)"""
    try:
        import edge_tts
        
        # Use a natural-sounding neural voice
        voice = "en-US-JennyNeural"  # American female, friendly
        
        # Generate speech
        communicate = edge_tts.Communicate(script_text, voice)
        communicate.save(output_path)
        
        print(f"✅ Voiceover generated: {output_path}")
        return output_path
    
    except Exception as e:
        print(f"❌ Voiceover error: {e}")
        # Fallback: use gTTS (also free)
        try:
            from gtts import gTTS
            tts = gTTS(text=script_text, lang='en', slow=False)
            tts.save(output_path)
            print(f"✅ Voiceover generated (fallback gTTS): {output_path}")
            return output_path
        except Exception as e2:
            print(f"❌ All voiceover methods failed: {e2}")
            return None

# ==========================================
# STEP 2: FETCH BACKGROUND VIDEO (Pexels API)
# ==========================================
def fetch_background(bg_theme, output_path="background.mp4"):
    """Fetch a free stock video from Pexels API (needs free API key)"""
    try:
        # Map themes to search queries
        theme_queries = {
            "Business/Office": "office work business professional",
            "Technology/Cyber": "technology computer coding cyber",
            "Luxury/Money": "luxury money success expensive",
            "Fitness/Health": "fitness gym workout healthy",
            "Travel/Adventure": "travel adventure nature explore",
            "Custom (we'll pick the best)": "lifestyle people success"
        }
        
        query = theme_queries.get(bg_theme, "lifestyle")
        
        # Call Pexels API
        headers = {"Authorization": PEXELS_API_KEY}
        params = {"query": query, "per_page": 1, "orientation": "portrait"}
        
        response = requests.get(
            "https://api.pexels.com/videos/search",
            headers=headers,
            params=params,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            if data["videos"]:
                # Get the best quality portrait video
                video_files = data["videos"][0]["video_files"]
                # Filter for portrait (9:16) or closest
                best_video = None
                for vf in video_files:
                    if vf["width"] < vf["height"]:  # Portrait
                        best_video = vf
                        break
                if not best_video:
                    best_video = video_files[0]  # Fallback
                
                # Download the video
                video_url = best_video["link"]
                video_response = requests.get(video_url, timeout=30)
                
                with open(output_path, "wb") as f:
                    f.write(video_response.content)
                
                print(f"✅ Background video downloaded: {output_path}")
                return output_path
            else:
                print("❌ No videos found on Pexels")
                return None
        else:
            print(f"❌ Pexels API error: {response.status_code}")
            return None
    
    except Exception as e:
        print(f"❌ Background fetch error: {e}")
        return None

# ==========================================
# STEP 3: GENERATE AI AVATAR (Free Hugging Face)
# ==========================================
def generate_ai_avatar(script_text, voiceover_path, output_path="avatar.mp4"):
    """Generate lip-synced AI avatar using free Hugging Face GPU space"""
    try:
        from gradio_client import Client
        
        # Connect to free Hugging Face space (KwaiVGI/LivePortrait)
        # This uses FREE GPU — no payment needed!
        client = Client("KwaiVGI/LivePortrait")
        
        # For demo: use a default avatar image
        # In production, let users upload their own face image!
        avatar_image = "https://raw.githubusercontent.com/KwaiVGI/LivePortrait/main/assets/examples/source/s9.jpg"
        
        # Call the API to generate lip-synced video
        result = client.predict(
            image=avatar_image,
            audio=voiceover_path,
            api_name="/generate"
        )
        
        # Download the result
        if result and len(result) > 0:
            video_url = result[0]  # Assuming first result is video URL
            video_response = requests.get(video_url, timeout=30)
            
            with open(output_path, "wb") as f:
                f.write(video_response.content)
            
            print(f"✅ AI avatar generated: {output_path}")
            return output_path
        else:
            print("❌ Hugging Face space didn't return a video")
            return None
    
    except Exception as e:
        print(f"❌ Avatar generation error: {e}")
        print("💡 Make sure you installed: pip install gradio_client")
        return None

# ==========================================
# STEP 4: COMPOSITE VIDEO (MoviePy + Captions)
# ==========================================
def build_viral_short(voiceover_path, background_path, avatar_path, output_path="final_video.mp4"):
    """Composite all elements into a viral short with captions"""
    try:
        from moviepy.editor import (
            VideoFileClip, AudioFileClip, 
            TextClip, CompositeVideoClip,
            ImageClip
        )
        import numpy as np
        from PIL import Image
        
        # Settings
        RESOLUTION = (1080, 1920)  # 9:16 vertical
        FPS = 30
        
        # Load clips
        background = VideoFileClip(background_path).resize(RESOLUTION)
        voiceover = AudioFileClip(voiceover_path)
        avatar = VideoFileClip(avatar_path).resize(height=600)
        
        # Trim background to match voiceover length
        background = background.subclip(0, min(background.duration, voiceover.duration + 1))
        
        # Create captions (3-word chunks)
        script_words = open(voiceover_path.replace(".mp3", "_script.txt"), "r").read().split()
        caption_clips = []
        
        word_duration = voiceover.duration / len(script_words)
        for i in range(0, len(script_words), 3):
            chunk = " ".join(script_words[i:i+3])
            start_time = i * word_duration
            end_time = min((i + 3) * word_duration, voiceover.duration)
            
            caption = TextClip(
                chunk,
                fontsize=70,
                color="yellow",
                font="Arial-Bold",
                stroke_color="black",
                stroke_width=2
            ).set_position(("center", 700)).set_start(start_time).set_end(end_time)
            
            caption_clips.append(caption)
        
        # Position avatar (circle cutout at bottom)
        avatar = avatar.set_position(("center", 1100))
        
        # Composite everything
        final = CompositeVideoClip(
            [background] + caption_clips + [avatar],
            size=RESOLUTION
        )
        final = final.set_audio(voiceover)
        final = final.subclip(0, voiceover.duration)
        
        # Export
        final.write_videofile(
            output_path,
            fps=FPS,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True
        )
        
        print(f"✅ Final video built: {output_path}")
        return output_path
    
    except Exception as e:
        print(f"❌ Video compositing error: {e}")
        return None

# ==========================================
# STEP 5: UPLOAD TO FREE CLOUD HOST (No Email!)
# ==========================================
def upload_to_free_host(video_path, host="file.io"):
    """Upload video to a free cloud host and return download link"""
    
    if host == "file.io":
        """
        file.io — FREE, no signup, temporary (7 days)
        Perfect for client downloads!
        """
        try:
            with open(video_path, "rb") as f:
                response = requests.post(
                    "https://file.io",
                    files={"file": f},
                    timeout=60
                )
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    download_link = data["link"]
                    print(f"✅ Video uploaded to file.io: {download_link}")
                    return download_link
                else:
                    print(f"❌ file.io upload failed: {data}")
                    return None
            else:
                print(f"❌ file.io HTTP error: {response.status_code}")
                return None
        
        except Exception as e:
            print(f"❌ file.io upload error: {e}")
            return None
    
    elif host == "transfer.sh":
        """
        transfer.sh — FREE, no signup, permanent
        """
        try:
            with open(video_path, "rb") as f:
                response = requests.put(
                    f"https://transfer.sh/{Path(video_path).name}",
                    data=f,
                    timeout=60
                )
            
            if response.status_code == 200:
                download_link = response.text.strip()
                print(f"✅ Video uploaded to transfer.sh: {download_link}")
                return download_link
            else:
                print(f"❌ transfer.sh HTTP error: {response.status_code}")
                return None
        
        except Exception as e:
            print(f"❌ transfer.sh upload error: {e}")
            return None
    
    else:
        print(f"❌ Unknown host: {host}")
        return None

# ==========================================
# MAIN PIPELINE — CALLED BY WEBHOOK/FORM
# ==========================================
def process_video_order(payload):
    """
    Main function to process a video order.
    payload = {
        "script": "...",
        "bg_theme": "Business/Office",
        "package": "Starter ($49)",
        "email": "client@email.com" (optional)
    }
    """
    print("\n" + "="*50)
    print("🤖 NEW VIDEO ORDER RECEIVED!")
    print("="*50)
    print(f"Script: {payload['script'][:100]}...")
    print(f"Theme: {payload['bg_theme']}")
    print(f"Package: {payload['package']}")
    print("="*50 + "\n")
    
    # Save script to file (for captions)
    script = payload["script"]
    with open("voiceover_script.txt", "w") as f:
        f.write(script)
    
    # Step 1: Generate voiceover
    print("🎤 Step 1/5: Generating voiceover...")
    voiceover_path = generate_voiceover(script)
    if not voiceover_path:
        return {"error": "Voiceover generation failed"}
    
    # Step 2: Fetch background
    print("🎬 Step 2/5: Fetching background video...")
    background_path = fetch_background(payload["bg_theme"])
    if not background_path:
        return {"error": "Background video fetch failed"}
    
    # Step 3: Generate AI avatar
    print("🤖 Step 3/5: Generating AI avatar (using free Hugging Face GPU)...")
    avatar_path = generate_ai_avatar(script, voiceover_path)
    if not avatar_path:
        return {"error": "Avatar generation failed"}
    
    # Step 4: Build final video
    print("🎥 Step 4/5: Compositing final video...")
    final_video_path = build_viral_short(voiceover_path, background_path, avatar_path)
    if not final_video_path:
        return {"error": "Video compositing failed"}
    
    # Step 5: Upload to free cloud host
    print("☁️ Step 5/5: Uploading to free cloud host...")
    download_link = upload_to_free_host(final_video_path, host="file.io")
    if not download_link:
        # Fallback to transfer.sh
        download_link = upload_to_free_host(final_video_path, host="transfer.sh")
    
    if download_link:
        print("\n" + "="*50)
        print("✅ VIDEO READY! DOWNLOAD LINK:")
        print(download_link)
        print("="*50 + "\n")
        
        return {
            "success": True,
            "download_link": download_link,
            "message": "Your viral short is ready! Click the link to download."
        }
    else:
        return {"error": "Upload failed — all free hosts failed"}

# ==========================================
# FLASK ROUTES (API Endpoints)
# ==========================================
@app.route("/")
def home():
    return """
    <h1>🎬 Viral Shorts AI Agency — Autopilot Server</h1>
    <p>✅ Server is running!</p>
    <p>📡 Send POST requests to <code>/generate</code> to build videos.</p>
    <p>🔒 No email needed — clients get a download link!</p>
    """

@app.route("/generate", methods=["POST"])
def generate_video():
    """API endpoint to generate a video (called by Streamlit app)"""
    try:
        payload = request.json
        
        # Validate payload
        if not payload or "script" not in payload:
            return jsonify({"error": "Missing script in request"}), 400
        
        # Process the order
        result = process_video_order(payload)
        
        if "error" in result:
            return jsonify(result), 500
        else:
            return jsonify(result), 200
    
    except Exception as e:
        print(f"❌ API error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/webhook", methods=["POST"])
def webhook():
    """Webhook endpoint (called by Tally.so or other forms)"""
    try:
        payload = request.json
        # Extract script from Tally form data
        # (Adjust based on Tally's webhook format)
        script = payload.get("data", {}).get("script", "")
        bg_theme = payload.get("data", {}).get("bg_theme", "Custom")
        
        if not script:
            return jsonify({"error": "No script provided"}), 400
        
        # Process
        result = process_video_order({
            "script": script,
            "bg_theme": bg_theme,
            "package": "Webhook",
            "email": "none"
        })
        
        return jsonify(result), 200
    
    except Exception as e:
        print(f"❌ Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

# ==========================================
# RUN THE SERVER (for Render.com)
# ==========================================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 STARTING AUTOMATED VIDEO SERVER...")
    print("="*50)
    print("✅ No email needed!")
    print("✅ Clients get download links!")
    print("✅ 100% free cloud hosting!")
    print("="*50 + "\n")
    
    # Run Flask app
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
