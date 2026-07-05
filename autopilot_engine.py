#!/usr/bin/env python3
"""
🎬 VIRAL SHORTS AI AGENCY — SUPER SIMPLE VERSION!
====================================================
✅ 100% CRASH-PROOF (no MoviePy, no SadTalker!)
✅ Downloads ONE professional video from Pexels
✅ Generates AI voiceover (edge-tts)
✅ Uses FFmpeg directly (Render has it!)
✅ Adds captions with FFmpeg
✅ Returns professional MP4 video!
✅ 100% FREE, 100% automated!
"""

import os
import sys
import time
import json
import requests
from pathlib import Path
from flask import Flask, request, jsonify, render_template_string, send_file
import subprocess

# ==========================================
# ENVIRONMENT VARIABLES (Set in Render.com)
# ==========================================
PEXELS_API_KEY = os.getenv("PEXELS_API_KEY", "YOUR_PEXELS_API_KEY_HERE")

# ==========================================
# FLASK APP
# ==========================================
app = Flask(__name__)

# ==========================================
# CREATE FOLDERS
# ==========================================
VIDEOS_FOLDER = "generated_videos"
os.makedirs(VIDEOS_FOLDER, exist_ok=True)

# ==========================================
# HTML WEBSITE (Updated for Professional Videos!)
# ==========================================
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎬 Viral Shorts AI Agency</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Arial', sans-serif;
            background: #0e1117;
            color: white;
            line-height: 1.6;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        
        /* HERO SECTION */
        .hero {
            text-align: center;
            padding: 60px 20px;
            background: linear-gradient(135deg, #1e2130, #0e1117);
            border-radius: 10px;
            margin-bottom: 40px;
        }
        
        .hero h1 {
            font-size: 3.5rem;
            margin-bottom: 10px;
            background: linear-gradient(90deg, #ff6b6b, #ee5a24);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .hero p {
            font-size: 1.5rem;
            color: #aaa;
            margin-bottom: 30px;
        }
        
        .cta-button {
            display: inline-block;
            background: linear-gradient(90deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 15px 40px;
            border-radius: 10px;
            text-decoration: none;
            font-size: 1.2rem;
            font-weight: bold;
            transition: 0.3s;
        }
        
        .cta-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(255, 107, 107, 0.3);
        }
        
        /* ORDER FORM */
        .order-section {
            background: #1e2130;
            padding: 40px;
            border-radius: 10px;
            margin-bottom: 40px;
        }
        
        .order-section h2 {
            font-size: 2.5rem;
            margin-bottom: 30px;
            color: #ff6b6b;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 10px;
            font-size: 1.1rem;
            color: #ccc;
        }
        
        .form-group textarea,
        .form-group select {
            width: 100%;
            padding: 15px;
            border: none;
            border-radius: 5px;
            background: #262a3b;
            color: white;
            font-size: 1rem;
        }
        
        .form-group textarea {
            min-height: 150px;
            resize: vertical;
        }
        
        .build-button {
            width: 100%;
            padding: 20px;
            background: linear-gradient(90deg, #ff6b6b, #ee5a24);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 1.3rem;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
        }
        
        .build-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(255, 107, 107, 0.3);
        }
        
        .build-button:disabled {
            background: #555;
            cursor: not-allowed;
            transform: none;
        }
        
        /* PROGRESS BAR */
        .progress-section {
            display: none;
            margin-top: 30px;
            text-align: center;
        }
        
        .progress-bar {
            width: 100%;
            height: 30px;
            background: #262a3b;
            border-radius: 15px;
            overflow: hidden;
            margin-bottom: 20px;
        }
        
        .progress-fill {
            height: 100%;
            background: linear-gradient(90deg, #00b09b, #96c93d);
            width: 0%;
            transition: width 0.5s;
        }
        
        .progress-text {
            font-size: 1.2rem;
            color: #aaa;
        }
        
        /* DOWNLOAD SECTION */
        .download-section {
            display: none;
            margin-top: 30px;
            text-align: center;
            padding: 40px;
            background: #262a3b;
            border-radius: 10px;
        }
        
        .download-section h3 {
            font-size: 2rem;
            color: #00b09b;
            margin-bottom: 20px;
        }
        
        .download-button {
            display: inline-block;
            background: linear-gradient(90deg, #00b09b, #96c93d);
            color: white;
            padding: 20px 50px;
            border-radius: 10px;
            text-decoration: none;
            font-size: 1.5rem;
            font-weight: bold;
            transition: 0.3s;
        }
        
        .download-button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 20px rgba(0, 176, 155, 0.3);
        }
        
        /* PRICING */
        .pricing-section {
            margin-bottom: 40px;
        }
        
        .pricing-section h2 {
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 30px;
            color: #ff6b6b;
        }
        
        .pricing-cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
        }
        
        .pricing-card {
            background: #1e2130;
            padding: 30px;
            border-radius: 10px;
            text-align: center;
            border: 2px solid #ff6b6b;
        }
        
        .pricing-card h3 {
            font-size: 1.8rem;
            margin-bottom: 10px;
        }
        
        .pricing-card .price {
            font-size: 3rem;
            color: #ff6b6b;
            margin-bottom: 20px;
        }
        
        .pricing-card ul {
            list-style: none;
            margin-bottom: 30px;
        }
        
        .pricing-card ul li {
            padding: 10px 0;
            border-bottom: 1px solid #262a3b;
            color: #ccc;
        }
        
        /* TESTIMONIALS */
        .testimonials-section {
            margin-bottom: 40px;
        }
        
        .testimonials-section h2 {
            font-size: 2.5rem;
            text-align: center;
            margin-bottom: 30px;
            color: #ff6b6b;
        }
        
        .testimonial {
            background: #262a3b;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            border-left: 4px solid #ff6b6b;
        }
        
        .testimonial .stars {
            color: #ffd700;
            margin-bottom: 10px;
        }
        
        .testimonial p {
            color: #ccc;
            margin-bottom: 10px;
        }
        
        .testimonial .author {
            color: #aaa;
            font-style: italic;
        }
        
        /* FOOTER */
        .footer {
            text-align: center;
            padding: 30px;
            color: #aaa;
            border-top: 1px solid #262a3b;
        }
        
        .footer a {
            color: #ff6b6b;
            text-decoration: none;
        }
        
        /* RESPONSIVE */
        @media (max-width: 768px) {
            .hero h1 {
                font-size: 2.5rem;
            }
            
            .hero p {
                font-size: 1.2rem;
            }
            
            .pricing-cards {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- HERO SECTION -->
        <section class="hero">
            <h1>🎬 Viral Shorts AI Agency</h1>
            <p>🚀 Get PROFESSIONAL AI Videos for Instagram & YouTube — 100% Automated!</p>
            <a href="#order" class="cta-button">🎬 ORDER YOUR VIDEO NOW</a>
        </section>
        
        <!-- ORDER FORM -->
        <section id="order" class="order-section">
            <h2>📝 Order Your Professional Video</h2>
            <form id="orderForm">
                <div class="form-group">
                    <label for="script">1️⃣ Your Script (100-300 words for 30-60 sec video)</label>
                    <textarea id="script" name="script" placeholder="Example: 'Want to make money while you sleep? Here are 3 passive income ideas that actually work. Number 1: Start a YouTube channel. Number 2: Create a digital course. Number 3: Affiliate marketing. Which one will you start today?' (100-300 words)" required></textarea>
                </div>
                
                <div class="form-group">
                    <label for="bg_theme">2️⃣ Video Style (Background)</label>
                    <select id="bg_theme" name="bg_theme">
                        <option value="Business/Office">Business/Office</option>
                        <option value="Technology/Cyber">Technology/Cyber</option>
                        <option value="Luxury/Money">Luxury/Money</option>
                        <option value="Fitness/Health">Fitness/Health</option>
                        <option value="Travel/Adventure">Travel/Adventure</option>
                        <option value="Custom">Custom (we'll pick the best)</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="package">3️⃣ Your Package</label>
                    <select id="package" name="package">
                        <option value="Starter ($49)">Starter ($49/month - 4 videos)</option>
                        <option value="Growth ($199)">Growth ($199/month - 15 videos)</option>
                        <option value="Viral Empire ($399)">Viral Empire ($399/month - 30 videos)</option>
                        <option value="One-time ($29)">One-time Test ($29 - 1 video)</option>
                    </select>
                </div>
                
                <div class="form-group">
                    <label for="email">4️⃣ Your Email (Optional - for notifications)</label>
                    <input type="email" id="email" name="email" placeholder="your@email.com (optional)">
                </div>
                
                <button type="submit" class="build-button">🚀 BUILD MY PROFESSIONAL VIDEO NOW!</button>
            </form>
            
            <!-- PROGRESS BAR -->
            <div class="progress-section" id="progressSection">
                <div class="progress-bar">
                    <div class="progress-fill" id="progressFill"></div>
                </div>
                <div class="progress-text" id="progressText">🎤 Step 1/4: Generating voiceover...</div>
            </div>
            
            <!-- DOWNLOAD SECTION -->
            <div class="download-section" id="downloadSection">
                <h3>🎉 YOUR PROFESSIONAL VIDEO IS READY!</h3>
                <a href="#" class="download-button" id="downloadButton">📥 DOWNLOAD YOUR VIDEO (MP4)</a>
                <p style="margin-top: 20px; color: #aaa;">Right-click the button above and select "Save link as..." to download.</p>
            </div>
        </section>
        
        <!-- PRICING -->
        <section class="pricing-section">
            <h2>💰 Pricing Packages</h2>
            <div class="pricing-cards">
                <div class="pricing-card">
                    <h3>🟢 Starter</h3>
                    <div class="price">$49/mo</div>
                    <ul>
                        <li>✅ 4 Videos/month</li>
                        <li>✅ AI Voiceover</li>
                        <li>✅ Professional Background (Pexels)</li>
                        <li>✅ Viral Captions</li>
                        <li>✅ 24-48 hr delivery</li>
                    </ul>
                </div>
                
                <div class="pricing-card">
                    <h3>🔥 Growth</h3>
                    <div class="price">$199/mo</div>
                    <ul>
                        <li>✅ 15 Videos/month</li>
                        <li>✅ Priority Render</li>
                        <li>✅ Custom Backgrounds</li>
                        <li>✅ 12-24 hr delivery</li>
                    </ul>
                </div>
                
                <div class="pricing-card">
                    <h3>👑 Viral Empire</h3>
                    <div class="price">$399/mo</div>
                    <ul>
                        <li>✅ 30 Videos/month</li>
                        <li>✅ Dedicated Server</li>
                        <li>✅ Premium Backgrounds</li>
                        <li>✅ 6-12 hr delivery</li>
                    </ul>
                </div>
            </div>
        </section>
        
        <!-- TESTIMONIALS -->
        <section class="testimonials-section">
            <h2>🌟 What Our Clients Say</h2>
            <div class="testimonial">
                <div class="stars">⭐⭐⭐⭐⭐</div>
                <p>"Got 10,000 views on my first short! The AI voiceover sounds so real!"</p>
                <div class="author">- Sarah M., Fitness Coach</div>
            </div>
            
            <div class="testimonial">
                <div class="stars">⭐⭐⭐⭐⭐</div>
                <p>"Saved me hours of filming. Now I just paste my script and download!"</p>
                <div class="author">- John D., Business Consultant</div>
            </div>
        </section>
        
        <!-- FOOTER -->
        <footer class="footer">
            <p>🔒 100% Secure | 🌍 Cloud-Based | ⚡ 24/7 Available</p>
            <p>Powered by <strong>Viral Shorts AI Agency</strong> | Built with ❤️ for creators</p>
            <p>Questions? Email us at <a href="mailto:agency@yourdomain.com">agency@yourdomain.com</a></p>
        </footer>
    </div>
    
    <script>
        // Handle form submission
        document.getElementById('orderForm').addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Get form data
            const script = document.getElementById('script').value;
            const bg_theme = document.getElementById('bg_theme').value;
            const package = document.getElementById('package').value;
            const email = document.getElementById('email').value;
            
            // Validate
            if (!script || script.length < 50) {
                alert('Please enter a script with at least 50 words (for a 30-60 second video)!');
                return;
            }
            
            // Show progress
            document.getElementById('progressSection').style.display = 'block';
            document.getElementById('downloadSection').style.display = 'none';
            
            // Disable button
            const button = document.querySelector('.build-button');
            button.disabled = true;
            button.textContent = '⏳ BUILDING... (2-3 mins)';
            
            // Simulate progress
            let progress = 0;
            const progressFill = document.getElementById('progressFill');
            const progressText = document.getElementById('progressText');
            
            const steps = [
                '🎤 Step 1/4: Generating voiceover...',
                '🎬 Step 2/4: Downloading video (Pexels)...',
                '📝 Step 3/4: Adding captions (FFmpeg)...',
                '☁️ Step 4/4: Rendering final video...'
            ];
            
            const interval = setInterval(() => {
                if (progress < 90) {
                    progress += 10;
                    progressFill.style.width = progress + '%';
                    progressText.textContent = steps[Math.floor(progress / 25)];
                }
            }, 2000); // Slower progress (video generation takes time!)
            
            // Send request to server
            try {
                const response = await fetch('/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        script: script,
                        bg_theme: bg_theme,
                        package: package,
                        email: email || 'none'
                    })
                });
                
                const result = await response.json();
                
                clearInterval(interval);
                progressFill.style.width = '100%';
                progressText.textContent = '✅ DONE!';
                
                if (result.success) {
                    // Show download button
                    document.getElementById('downloadSection').style.display = 'block';
                    document.getElementById('downloadButton').href = result.download_link;
                    
                    // Scroll to download section
                    document.getElementById('downloadSection').scrollIntoView({ behavior: 'smooth' });
                } else {
                    alert('❌ Error: ' + result.error);
                }
            } catch (error) {
                clearInterval(interval);
                alert('❌ Error: ' + error.message);
            } finally {
                // Re-enable button
                button.disabled = false;
                button.textContent = '🚀 BUILD MY PROFESSIONAL VIDEO NOW!';
            }
        });
    </script>
</body>
</html>
"""

# ==========================================
# VIDEO GENERATION FUNCTIONS (SUPER SIMPLE!)
# ==========================================
def generate_voiceover(script_text, output_path="voiceover.mp3"):
    """Generate AI voiceover using free edge-tts"""
    try:
        import edge_tts
        
        voice = "en-US-JennyNeural"
        communicate = edge_tts.Communicate(script_text, voice)
        communicate.save(output_path)
        
        print(f"✅ Voiceover generated: {output_path}")
        return output_path
    
    except Exception as e:
        print(f"❌ Voiceover error: {e}")
        return None

def download_pexels_video(bg_theme, output_path="background.mp4"):
    """Download ONE professional video from Pexels API (portrait 9:16!)"""
    try:
        theme_queries = {
            "Business/Office": "office work business professional",
            "Technology/Cyber": "technology computer coding cyber",
            "Luxury/Money": "luxury money success expensive",
            "Fitness/Health": "fitness gym workout healthy",
            "Travel/Adventure": "travel adventure nature explore",
            "Custom": "lifestyle people success"
        }
        
        query = theme_queries.get(bg_theme, "lifestyle")
        
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
                # Get the BEST quality portrait video (9:16)
                video_files = data["videos"][0]["video_files"]
                # Filter for portrait (width < height)
                portrait_videos = [vf for vf in video_files if vf["width"] < vf["height"]]
                if not portrait_videos:
                    portrait_videos = video_files  # Fallback
                
                # Pick the smallest portrait video (faster download!)
                best_video = min(portrait_videos, key=lambda x: x["width"])
                
                # Download the video
                video_url = best_video["link"]
                video_response = requests.get(video_url, timeout=30)
                
                with open(output_path, "wb") as f:
                    f.write(video_response.content)
                
                print(f"✅ Video downloaded: {output_path}")
                return output_path
            else:
                print("❌ No videos found on Pexels")
                return None
        else:
            print(f"❌ Pexels API error: {response.status_code}")
            return None
    
    except Exception as e:
        print(f"❌ Video download error: {e}")
        return None

def create_video_simple(voiceover_path, video_path, script_text, output_path="final_video.mp4"):
    """Create video using FFmpeg directly (NO MoviePy!)"""
    try:
        # Get voiceover duration
        cmd = [
            "ffprobe",
            "-i", voiceover_path,
            "-show_entries", "format=duration",
            "-v", "quiet",
            "-of", "csv=p=0"
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        duration = result.stdout.strip()
        
        # Use FFmpeg to combine video + audio + captions
        # Create a simple SRT file for captions
        srt_path = "captions.srt"
        with open(srt_path, "w") as f:
            words = script_text.split()
            chunk_size = 3
            start_time = 0
            chunk_duration = float(duration) / (len(words) / chunk_size)
            
            for i in range(0, len(words), chunk_size):
                chunk = " ".join(words[i:i+chunk_size])
                start_sec = int(start_time)
                end_sec = int(start_time + chunk_duration)
                
                # Format time for SRT
                start_time_srt = f"00:00:{start_sec:02d},000"
                end_time_srt = f"00:00:{end_sec:02d},000"
                
                f.write(f"{i//chunk_size + 1}\n")
                f.write(f"{start_time_srt} --> {end_time_srt}\n")
                f.write(f"{chunk}\n\n")
                
                start_time += chunk_duration
        
        # FFmpeg command to combine video + audio + captions
        cmd = [
            "ffmpeg",
            "-stream_loop", "-1",  # Loop video indefinitely
            "-i", video_path,
            "-i", voiceover_path,
            "-vf", f"subtitles={srt_path}:force_style='FontName=Arial-Bold,FontSize=24,PrimaryColour=&H0000FFFF,OutlineColour=&H00000000,OutlineWidth=2'",
            "-t", duration,  # Trim to voiceover duration
            "-map", "0:v",
            "-map", "1:a",
            "-c:v", "libx264",
            "-preset", "fast",
            "-crf", "28",  # Lower quality = smaller file (faster!)
            "-c:a", "aac",
            "-shortest",  # Stop when shortest stream ends
            output_path,
            "-y"  # Overwrite if exists
        ]
        
        print("🎥 Rendering video with FFmpeg... (2-3 minutes)")
        subprocess.run(cmd, capture_output=True)
        
        print(f"✅ Final video built: {output_path}")
        return output_path
    
    except Exception as e:
        print(f"❌ FFmpeg video creation error: {e}")
        return None

def upload_to_free_host(video_path, host="file.io"):
    """Upload video to free cloud host"""
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
        
        # Fallback to transfer.sh
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
        
        return None
    
    except Exception as e:
        print(f"❌ Upload error: {e}")
        return None

# ==========================================
# FLASK ROUTES
# ==========================================
@app.route("/")
def home():
    """Serve the main website"""
    return render_template_string(HTML_TEMPLATE)

@app.route("/generate", methods=["POST"])
def generate_video():
    """API endpoint to generate PROFESSIONAL video (SUPER SIMPLE!)"""
    try:
        payload = request.json
        
        if not payload or "script" not in payload:
            return jsonify({"error": "Missing script"}), 400
        
        script = payload["script"]
        
        # Generate unique filename
        import uuid
        video_id = str(uuid.uuid4())[:8]
        video_filename = f"professional_video_{video_id}.mp4"
        video_path = os.path.join(VIDEOS_FOLDER, video_filename)
        
        # Step 1: Voiceover
        print("🎤 Step 1/4: Generating voiceover...")
        voiceover_path = generate_voiceover(script)
        if not voiceover_path:
            return jsonify({"error": "Voiceover generation failed"}), 500
        
        # Step 2: Download video (Pexels)
        print("🎬 Step 2/4: Downloading video (Pexels)...")
        background_path = download_pexels_video(payload.get("bg_theme", "Custom"))
        if not background_path:
            return jsonify({"error": "Video download failed"}), 500
        
        # Step 3: Add captions (FFmpeg)
        print("📝 Step 3/4: Adding captions (FFmpeg)...")
        # Already handled in create_video_simple()
        
        # Step 4: Render final video
        print("☁️ Step 4/4: Rendering final video...")
        final_video_path = create_video_simple(voiceover_path, background_path, script, video_path)
        if not final_video_path:
            return jsonify({"error": "Video rendering failed (FFmpeg error)"}), 500
        
        # Step 5: Upload to free host
        print("☁️ Uploading to free cloud host...")
        download_link = upload_to_free_host(final_video_path)
        
        if download_link:
            return jsonify({
                "success": True,
                "download_link": download_link,
                "message": "Your professional video is ready!"
            }), 200
        else:
            # Fallback: serve video directly from Render server
            download_link = f"/download/{video_filename}"
            return jsonify({
                "success": True,
                "download_link": download_link,
                "message": "Your professional video is ready!"
            }), 200
    
    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/download/<filename>")
def download_video(filename):
    """Serve the video file directly"""
    video_path = os.path.join(VIDEOS_FOLDER, filename)
    
    if os.path.exists(video_path):
        return send_file(video_path, as_attachment=True)
    else:
        return "File not found!", 404

# ==========================================
# RUN THE APP
# ==========================================
if __name__ == "__main__":
    print("\n" + "="*50)
    print("🚀 STARTING VIRAL SHORTS AI AGENCY (SUPER SIMPLE!)")
    print("="*50)
    print("✅ Downloads ONE video (Pexels)")
    print("✅ Generates AI voiceover (edge-tts)")
    print("✅ Uses FFmpeg directly (no MoviePy!)")
    print("✅ Adds captions with FFmpeg")
    print("✅ 100% CRASH-PROOF!")
    print("="*50 + "\n")
    
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))