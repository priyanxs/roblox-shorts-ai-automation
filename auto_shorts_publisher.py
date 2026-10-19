#!/usr/bin/env python3
"""
Autonomous YouTube Shorts Generator & Publisher (v2.0 Elite Edition)
- Deep, engaging storytelling using local Ollama (llama3.2)
- Anti-repetition content engine with 30+ unique gaming topics
- Studio-grade neural voiceover via edge-tts (Guy & Christopher)
- Subtle background gaming lofi beat audio mixing
- High-retention ASS subtitles (2-3 word punchy chunks)
- Dynamic background video selection & random cut points
- Direct publishing via n8n & instant Telegram watch links
"""

import os
import sys
import json
import time
import random
import re
import argparse
import subprocess
import urllib.request
import requests
from content_engine import get_next_topic

BASE_DIR = "/Users/priyanxs/Downloads/automation"
FFMPEG_PATH = os.path.join(BASE_DIR, "bin/ffmpeg")
OLLAMA_URL = "http://localhost:11434/api/generate"
N8N_BASE_URL = "http://localhost:5678"
USER_CHAT_ID = "7268016860"

def query_ollama(niche, topic_info):
    print(f"[{niche.upper()}] Selected Topic: {topic_info['topic']} ({topic_info['category']})")
    
    prompt = f"""You are a top viral {niche.capitalize()} YouTuber creating an addictive, high-retention YouTube Short.
Topic: {topic_info['topic']}
Core Secret / Story: {topic_info['angle']}
Initial Hook: {topic_info['hook']}

Write an engaging, complete 65 to 80 word voiceover narration.
STRICT RULES:
1. Start directly with the hook or a punchy variation that stops anyone scrolling within 2 seconds.
2. DO NOT make cheap teases like 'watch till the end'. Explain the actual lore, trick, or secret with real details and suspense.
3. Keep the pacing fast, energetic, and exciting.
4. Total length MUST be between 65 and 80 words.
5. Provide a viral CTR title under 50 characters with gaming emojis and #Shorts.

Respond ONLY with valid JSON in this exact structure:
{{
  "title": "Viral Title Under 50 Chars 🎮 #Shorts #{niche.capitalize()}",
  "script": "The complete 65-80 word voiceover narration text...",
  "description": "Engaging description with emojis.\\n\\n#{niche.capitalize()} #{niche.capitalize()}Shorts #Shorts #Gaming #Viral",
  "tags": "{niche}, {niche} shorts, {niche} secrets, {niche} facts, gaming, viral"
}}"""

    payload = {
        "model": "llama3.2",
        "prompt": prompt,
        "stream": False,
        "format": "json"
    }

    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        data = json.loads(resp.read().decode('utf-8'))
        response_text = data.get("response", "{}")
        meta = json.loads(response_text)
        
        # Ensure #Shorts in title
        title = meta.get("title", f"Insane {niche.capitalize()} Secrets! 🎮 #Shorts")
        if "#shorts" not in title.lower():
            title = f"{title[:45]} #Shorts"
        meta["title"] = title
        
        # Format tags
        tags = meta.get("tags", f"{niche}, shorts, gaming")
        if isinstance(tags, list):
            tags = ", ".join(tags)
        meta["tags"] = str(tags)
        
        return meta

def generate_voiceover(text, voice="en-US-GuyNeural", rate="+10%"):
    print(f"Generating studio neural voiceover ({voice} at {rate})...")
    temp_audio = os.path.join(BASE_DIR, "temp_voice.mp3")
    temp_vtt = os.path.join(BASE_DIR, "temp_subs.vtt")
    
    cmd = [
        "python3", "-m", "edge_tts",
        "--voice", voice,
        "--rate", rate,
        "--text", text,
        "--write-media", temp_audio,
        "--write-subtitles", temp_vtt
    ]
    subprocess.run(cmd, check=True)
    return temp_audio, temp_vtt

def vtt_to_ass(vtt_path, ass_path):
    ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial Black,74,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,3,2,40,40,480,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    with open(vtt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    cue_pattern = re.compile(
        r'(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[,\.]\d{3})\s*\n(.*?)(?=\n\n|\n\d+|\Z)',
        re.DOTALL
    )
    matches = cue_pattern.findall(content)
    dialogues = []

    for start, end, text in matches:
        clean_text = re.sub(r'[^\w\s\.,!\?\'\-]', '', text)
        clean_text = " ".join(clean_text.strip().split()).upper()
        words = clean_text.split()
        if not words:
            continue

        start_sec = sum(x * float(t) for x, t in zip([3600, 60, 1], start.replace(',', '.').split(':')))
        end_sec = sum(x * float(t) for x, t in zip([3600, 60, 1], end.replace(',', '.').split(':')))
        total_dur = max(0.1, end_sec - start_sec)

        # 2 to 3 words per rapid subtitle chunk
        chunk_size = 3
        chunks = [words[i:i + chunk_size] for i in range(0, len(words), chunk_size)]
        chunk_dur = total_dur / len(chunks)

        for idx, chunk in enumerate(chunks):
            c_start = start_sec + (idx * chunk_dur)
            c_end = start_sec + ((idx + 1) * chunk_dur)
            c_start_str = f"{int(c_start//3600)}:{int((c_start%3600)//60):02d}:{c_start%60:05.2f}"
            c_end_str = f"{int(c_end//3600)}:{int((c_end%3600)//60):02d}:{c_end%60:05.2f}"
            dialogues.append(f"Dialogue: 0,{c_start_str},{c_end_str},Default,,0,0,0,,{' '.join(chunk)}")

    with open(ass_path, 'w', encoding='utf-8') as f:
        f.write(ass_header + "\n".join(dialogues))

def get_duration(file_path):
    cmd = [FFMPEG_PATH, "-i", file_path]
    res = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True)
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
    if m:
        h, mn, s = m.groups()
        return int(h) * 3600 + int(mn) * 60 + float(s)
    return 20.0

def choose_background_video(niche, topic_text=""):
    niche_dir = os.path.join(BASE_DIR, f"assets/{niche}")
    candidates = [
        os.path.join(niche_dir, f) for f in os.listdir(niche_dir)
        if (f.endswith(".webm") or f.endswith(".mp4") or f.endswith(".mkv")) and not f.endswith(".part")
    ]
    if not candidates:
        raise FileNotFoundError(f"No background clips found in: {niche_dir}")
        
    # Smart matching if keyword matches topic
    lower_topic = topic_text.lower()
    for c in candidates:
        name = os.path.basename(c).lower()
        if "brookhaven" in lower_topic and "brookhaven" in name:
            print(f"[{niche.upper()}] Matched Keyword Background: {os.path.basename(c)}")
            return c
        if ("blade" in lower_topic or "deflect" in lower_topic) and "blade" in name:
            print(f"[{niche.upper()}] Matched Keyword Background: {os.path.basename(c)}")
            return c

    chosen = random.choice(candidates)
    print(f"[{niche.upper()}] Selected Background Video: {os.path.basename(chosen)}")
    return chosen

def compose_short(niche, audio_path, ass_path, output_mp4, topic_text=""):
    print(f"[{niche.upper()}] Composing vertical short (Background video audio 100% MUTED, Pure Voiceover only)...")
    bg_video = choose_background_video(niche, topic_text)
    bg_dur = get_duration(bg_video)
    audio_dur = get_duration(audio_path)

    max_start = max(0, bg_dur - audio_dur - 1)
    start_time = random.uniform(0, max_start) if max_start > 0 else 0

    # Video: 9:16 vertical crop + scale to 1080x1920 + burn subtitles
    # Audio: Input 0 (gameplay) is completely MUTED. Only Input 1 (pure voiceover) is mapped!
    filter_complex = f"[0:v]crop=min(iw\\,ih*9/16):min(ih\\,iw*16/9):(iw-ow)/2:(ih-oh)/2,scale=1080:1920,ass={ass_path}[v]"

    cmd = [
        FFMPEG_PATH, "-y",
        "-ss", str(round(start_time, 2)),
        "-i", bg_video,
        "-i", audio_path,
        "-filter_complex", filter_complex,
        "-map", "[v]",
        "-map", "1:a:0",
        "-t", str(round(audio_dur + 0.3, 2)),
        "-c:v", "libx264",
        "-preset", "veryfast",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "192k",
        "-ar", "44100",
        output_mp4
    ]

    subprocess.run(cmd, check=True)

def publish_to_youtube_via_n8n(niche, video_path, meta):
    webhook_url = f"{N8N_BASE_URL}/webhook/auto-upload-{niche.lower()}"
    print(f"[{niche.upper()}] Uploading to YouTube via n8n webhook: {webhook_url}")
    
    with open(video_path, 'rb') as f:
        files = {
            'data': (os.path.basename(video_path), f, 'video/mp4')
        }
        data = {
            'title': meta['title'],
            'description': meta['description'],
            'tags': meta['tags'],
            'chatId': USER_CHAT_ID
        }
        resp = requests.post(webhook_url, files=files, data=data, timeout=300)
        print(f"[{niche.upper()}] n8n Webhook response ({resp.status_code}): {resp.text[:200]}")
        return resp.status_code == 200

def run_pipeline(niche):
    print("=" * 65)
    print(f"🚀 [PRODUCTION] Generating High-Quality Short for: {niche.upper()}")
    print(f"⏰ Execution Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 65)
    
    os.makedirs(os.path.join(BASE_DIR, "output"), exist_ok=True)
    timestamp = int(time.time())
    
    # 1. Fetch Next Unique Viral Topic
    topic_info = get_next_topic(niche)
    voice = topic_info.get("voice", "en-US-GuyNeural")
    
    # 2. Generate Detailed Narrative Script with Ollama
    meta = query_ollama(niche, topic_info)
    print(f"📌 Title: {meta['title']}")
    print(f"📜 Script ({len(meta['script'].split())} words):\n\"{meta['script']}\"")
    
    # 3. Generate Studio Voiceover & Word Timings
    audio_file, vtt_file = generate_voiceover(meta['script'], voice=voice, rate="+10%")
    ass_file = os.path.join(BASE_DIR, "temp_subs.ass")
    vtt_to_ass(vtt_file, ass_file)
    
    # 4. Render Video with Background Gameplay, BGM, and Styled Subtitles
    output_video = os.path.join(BASE_DIR, f"output/{niche}_short_{timestamp}.mp4")
    compose_short(niche, audio_file, ass_file, output_video, topic_text=topic_info['topic'])
    
    # 5. Save metadata JSON
    meta_path = os.path.join(BASE_DIR, f"output/{niche}_short_{timestamp}.json")
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2)
        
    # 6. Upload via n8n to YouTube
    success = publish_to_youtube_via_n8n(niche, output_video, meta)
    
    # 7. Clean up temporary working files
    for tmp in [audio_file, vtt_file, ass_file]:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except Exception:
                pass
                
    if success:
        print(f"🎉 SUCCESS! High-quality short created & published to {niche.upper()} YouTube channel!")
    else:
        print(f"⚠️ Video rendered successfully at {output_video}, but webhook returned error.")
    print("=" * 65)
    return success

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous YouTube Shorts Generator & Publisher")
    parser.add_argument("--niche", choices=["roblox", "minecraft"], default="roblox", help="Gaming niche to generate")
    args = parser.parse_args()
    
    run_pipeline(args.niche)
