# 🎮 Roblox YouTube Shorts AI Automation (100% Free)

[![n8n](https://img.shields.io/badge/Workflow-n8n-orange.svg)](https://n8n.io)
[![Ollama](https://img.shields.io/badge/AI-Ollama%20(Llama%203.2)-blue.svg)](https://ollama.com)
[![Docker](https://img.shields.io/badge/Container-Docker-2496ED.svg)](https://docker.com)
[![Telegram](https://img.shields.io/badge/Trigger-Telegram%20Bot-blue.svg)](https://telegram.org)
[![YouTube](https://img.shields.io/badge/Platform-YouTube%20Shorts-red.svg)](https://youtube.com)

Automated YouTube Shorts publisher for **Roblox** gaming videos using self-hosted **n8n**, local **Ollama AI (Llama 3.2)**, and a **Telegram Bot**.

Zero paid APIs, 100% free and private.

---

## 🚀 How It Works

```
[User sends Roblox Video to Telegram Bot]
                   │
                   ▼
     [Local Telegram Poller / Trigger]
                   │
                   ▼
     [Ollama Local AI (Llama 3.2)]
       - Viral Hook Title with emojis & #Shorts #Roblox
       - Engaging 2-sentence description
       - High-reach gaming tags & hashtags
                   │
                   ▼
    [YouTube Data API v3 (OAuth2)]
       - Uploads video as YouTube Short (Gaming Category 20)
                   │
                   ▼
  [Telegram Bot replies with direct Shorts URL]
```

---

## 📁 Repository Structure

- `workflow.json` — Pre-built, ready-to-import n8n workflow.
- `docker-compose.yml` — Docker Compose configuration for running n8n with local Ollama access.
- `telegram_poller.js` — Lightweight polling daemon that forwards Telegram videos to n8n without needing public URLs.
- `.env.example` — Template for your environment variables and keys.

---

## 🛠️ Quick Start Guide

### 1. Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed & running.
- [Ollama](https://ollama.com/) installed on your machine.
- A Telegram account (to create a free bot via `@BotFather`).
- A Google Cloud Project with **YouTube Data API v3** enabled.

### 2. Start Ollama
```bash
ollama run llama3.2
```

### 3. Launch n8n with Docker
```bash
docker compose up -d
```
Open **`http://localhost:5678`** in your browser.

### 4. Configure Credentials in n8n
1. **Telegram API:** Paste your Bot Token from `@BotFather`.
2. **YouTube OAuth2 API:**
   - Create an OAuth 2.0 Client ID (Web Application) in [Google Cloud Console](https://console.cloud.google.com/).
   - Add Authorized Redirect URI: `http://localhost:5678/rest/oauth2-credential/callback`.
   - Connect your YouTube Google Account in n8n.

### 5. Import Workflow
1. Go to **Workflows** -> **Import from File**.
2. Select `workflow.json`.
3. Link your Telegram and YouTube credentials to the nodes.
4. Toggle to **Active / Published**!

### 6. Run the Telegram Poller Daemon
```bash
node telegram_poller.js
```

---

## 📱 Usage
1. Open your Telegram bot.
2. Send any Roblox video (you can optionally add a caption topic like *"Blox fruits insane combo"* or leave it blank).
3. The AI generates viral titles, tags, and uploads the video directly to your YouTube channel as a Short, then replies with the video link!

---

## 📄 License
MIT License. Created by [Priyanshu](https://github.com/priyanxs).
