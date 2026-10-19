// Multi-Bot Telegram Polling Daemon for n8n Automation
const https = require('https');
const http = require('http');

const BOTS = [
  {
    name: 'Robolox Bot',
    token: '8939167204:AAGQYnH7YkOT0sKl-SlDAF1G8ct20beldWQ',
    webhookUrl: 'http://localhost:5678/webhook/tg-shorts-trigger/webhook',
    secretToken: 'g5w7ZkEcaWCN1ez2_1',
    offset: 0
  },
  {
    name: 'Minecraft Bot',
    token: '8890257065:AAG2Vun6d10ALBZ0k41QMxWFPWdCiTAjzjw',
    webhookUrl: 'http://localhost:5678/webhook/tg-mc-shorts-trigger/webhook',
    secretToken: '9kzFFroLmI4gNTsc_1',
    offset: 0
  }
];

function deleteWebhook(bot) {
  return new Promise((resolve) => {
    https.get(`https://api.telegram.org/bot${bot.token}/deleteWebhook`, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        console.log(`[${bot.name}] Webhook cleared:`, data);
        resolve();
      });
    }).on('error', () => resolve());
  });
}

function forwardToN8n(bot, update) {
  return new Promise((resolve) => {
    const postData = JSON.stringify(update);
    const req = http.request(bot.webhookUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(postData),
        'x-telegram-bot-api-secret-token': bot.secretToken
      }
    }, (res) => {
      let resBody = '';
      res.on('data', chunk => resBody += chunk);
      res.on('end', () => {
        console.log(`[${bot.name}] Forwarded update ${update.update_id} to n8n (status ${res.statusCode})`);
        resolve();
      });
    });

    req.on('error', (err) => {
      console.error(`[${bot.name}] Error forwarding:`, err.message);
      resolve();
    });

    req.write(postData);
    req.end();
  });
}

function pollBot(bot) {
  const url = `https://api.telegram.org/bot${bot.token}/getUpdates?offset=${bot.offset}&timeout=30`;
  https.get(url, (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', async () => {
      try {
        const json = JSON.parse(data);
        if (json.ok && Array.isArray(json.result) && json.result.length > 0) {
          for (const update of json.result) {
            console.log(`[${bot.name}] Received update ${update.update_id}`);
            bot.offset = update.update_id + 1;
            await forwardToN8n(bot, update);
          }
        }
      } catch (e) {
        console.error(`[${bot.name}] Parse error:`, e.message);
      }
      setTimeout(() => pollBot(bot), 1000);
    });
  }).on('error', (err) => {
    console.error(`[${bot.name}] Poll error:`, err.message);
    setTimeout(() => pollBot(bot), 3000);
  });
}

async function start() {
  console.log('Starting Multi-Bot Telegram Polling Daemon...');
  for (const bot of BOTS) {
    await deleteWebhook(bot);
    pollBot(bot);
    console.log(`Started polling for ${bot.name}`);
  }
}

start();
