#!/usr/bin/env python3
"""
Autonomous YouTube Shorts Generator & Publisher
- Generates viral script using local Ollama (llama3.2)
- High quality neural voiceover via edge-tts (ChristopherNeural)
- Dynamic styled ASS retention subtitles (TikTok / Shorts style)
- Composes 1080x1920 9:16 vertical video using FFmpeg
- Posts to n8n Webhook to auto-upload to YouTube & notify Telegram
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

BASE_DIR = "/Users/priyanxs/Downloads/automation"
FFMPEG_PATH = os.path.join(BASE_DIR, "bin/ffmpeg")
OLLAMA_URL = "http://localhost:11434/api/generate"
N8N_BASE_URL = "http://localhost:5678"
USER_CHAT_ID = "7268016860"

def get_niche_prompt(niche):
    if niche.lower() == "roblox":
        return """You are a top viral Roblox YouTuber creating addictive YouTube Shorts.
Generate an insane 40-50 word story, mind-blowing glitch, or hilarious secret in Roblox.
The hook MUST grab viewers within the first 3 seconds (e.g. "Only 1% of Roblox players know this secret glitch...").
Keep pacing fast, mysterious, and engaging.

Respond ONLY with valid JSON in this exact structure:
{
  "title": "Viral Title Under 50 Chars 💀 #Shorts #Roblox",
  "script": "The 40-50 word high-energy voiceover narration...",
  "description": "Engaging description with emojis.\\n\\n#Roblox #RobloxShorts #RobloxMemes #Shorts #Gaming #Viral",
  "tags": "roblox, roblox shorts, roblox memes, roblox funny, roblox glitch, gaming"
}"""
    else:  # minecraft
        return """You are a top viral Minecraft YouTuber creating addictive YouTube Shorts.
Generate an insane 40-50 word secret fact, hidden crafting trick, or mind-blowing mechanic in Minecraft.
The hook MUST grab viewers within the first 3 seconds (e.g. "Did you know you can survive any fall in Minecraft without water?").
Keep pacing fast, energetic, and engaging.

Respond ONLY with valid JSON in this exact structure:
{
  "title": "Viral Title Under 50 Chars ⛏️ #Shorts #Minecraft",
  "script": "The 40-50 word high-energy voiceover narration...",
  "description": "Mindblowing Minecraft secret you never knew!\\n\\n#Minecraft #MinecraftShorts #MinecraftMemes #Shorts #Gaming #Viral",
  "tags": "minecraft, minecraft shorts, minecraft facts, minecraft secrets, gaming, viral"
}"""

def query_ollama(niche):
    print(f"[{niche.upper()}] Querying Ollama (llama3.2) for viral script...")
    prompt = get_niche_prompt(niche)
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
        
        # Ensure #Shorts tag in title
        title = meta.get("title", f"Insane {niche.capitalize()} Moments! 🎮 #Shorts")
        if "#shorts" not in title.lower():
            title = f"{title[:45]} #Shorts"
        meta["title"] = title
        
        # Format tags
        tags = meta.get("tags", f"{niche}, shorts, gaming")
        if isinstance(tags, list):
            tags = ", ".join(tags)
        meta["tags"] = str(tags)
        
        return meta

def generate_voiceover(text, voice="en-US-ChristopherNeural", rate="+15%"):
    print("Generating high-quality neural voiceover with edge-tts...")
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
Style: Default,Arial Black,72,&H0000FFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,6,2,2,40,40,480,1

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

        chunk_size = 4
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
    return 15.0

def compose_short(niche, audio_path, ass_path, output_mp4):
    print(f"[{niche.upper()}] Composing vertical short with FFmpeg...")
    bg_video = os.path.join(BASE_DIR, f"assets/{niche}/bg1.webm")
    if not os.path.exists(bg_video):
        raise FileNotFoundError(f"Background video not found at: {bg_video}")

    bg_dur = get_duration(bg_video)
    audio_dur = get_duration(audio_path)

    max_start = max(0, bg_dur - audio_dur - 1)
    start_time = random.uniform(0, max_start) if max_start > 0 else 0

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
        "-shortest",
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
    print("=" * 60)
    print(f"🚀 Starting autonomous short creation for: {niche.upper()} at {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    os.makedirs(os.path.join(BASE_DIR, "output"), exist_ok=True)
    timestamp = int(time.time())
    
    # 1. Generate Script
    meta = query_ollama(niche)
    print(f"Title: {meta['title']}")
    print(f"Script: {meta['script']}")
    
    # 2. Voiceover & Subtitles
    audio_file, vtt_file = generate_voiceover(meta['script'])
    ass_file = os.path.join(BASE_DIR, "temp_subs.ass")
    vtt_to_ass(vtt_file, ass_file)
    
    # 3. Render Video
    output_video = os.path.join(BASE_DIR, f"output/{niche}_short_{timestamp}.mp4")
    compose_short(niche, audio_file, ass_file, output_video)
    
    # 4. Save metadata JSON
    meta_path = os.path.join(BASE_DIR, f"output/{niche}_short_{timestamp}.json")
    with open(meta_path, 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=2)
        
    # 5. Upload via n8n
    success = publish_to_youtube_via_n8n(niche, output_video, meta)
    
    # 6. Clean up temporary files
    for tmp in [audio_file, vtt_file, ass_file]:
        if os.path.exists(tmp):
            try:
                os.remove(tmp)
            except Exception:
                pass
                
    if success:
        print(f"✅ Finished successfully! Short uploaded to {niche.upper()} YouTube channel!")
    else:
        print(f"⚠️ Video rendered at {output_video}, but webhook returned non-200.")
    print("=" * 60)
    return success

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Autonomous YouTube Shorts Generator & Publisher")
    parser.add_argument("--niche", choices=["roblox", "minecraft"], default="roblox", help="Gaming niche to generate")
    args = parser.parse_args()
    
    run_pipeline(args.niche)
