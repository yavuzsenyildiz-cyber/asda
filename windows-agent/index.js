const axios = require('axios');
const wol = require('wake_on_lan');
require('dotenv').config();

const BACKEND_URL = process.env.BACKEND_URL || 'http://localhost:3000';
const DEVICE_ID = process.env.DEVICE_ID;
const TOKEN = process.env.AGENT_TOKEN;
const POLL_INTERVAL = parseInt(process.env.POLL_INTERVAL || '5000');
const TARGET_MAC = process.env.TARGET_MAC; // Açılacak bilgisayarın MAC adresi

if (!DEVICE_ID || !TOKEN) {
  console.error('❌ DEVICE_ID ve AGENT_TOKEN ortam değişkenleri gerekli!');
  process.exit(1);
}

const api = axios.create({
  baseURL: BACKEND_URL,
  headers: {
    Authorization: `Bearer ${TOKEN}`,
    'Content-Type': 'application/json',
  },
});

// WoL paketini gönder
async function wakeOnLan(macAddress) {
  return new Promise((resolve, reject) => {
    wol.wake(macAddress, (error) => {
      if (error) {
        console.error(`❌ WoL gönderme hatası (${macAddress}):`, error);
        reject(error);
      } else {
        console.log(`✅ WoL paketı gönderildi: ${macAddress}`);
        resolve(true);
      }
    });
  });
}

// Sunucudan yeni komutları dinle
async function pollCommands() {
  try {
    // Burada WebSocket kullanılabilir, şimdilik polling yapalım
    // İleride: Socket.io veya native WebSocket implemente edilebilir
    console.log('📡 Sunucuyu dinleniyor...');
  } catch (error) {
    console.error('Poll hatası:', error.message);
  }
}

// Bilgisayarı aç komutu (manuel test için)
async function powerOnComputer(macAddress) {
  try {
    console.log(`💻 Bilgisayar açılıyor: ${macAddress}`);
    await wakeOnLan(macAddress || TARGET_MAC);
    console.log('✅ Bilgisayar açma komutu gönderildi!');
  } catch (error) {
    console.error('❌ Hata:', error.message);
  }
}

// Cihaz kaydını al
async function registerDevice() {
  try {
    const response = await api.post('/api/auth/login', {
      deviceId: DEVICE_ID,
    });
    console.log('✅ Cihaz kaydedildi:', response.data);
  } catch (error) {
    console.error('❌ Cihaz kaydı hatası:', error.message);
  }
}

// Ana döngü
async function main() {
  console.log('🚀 Windows Agent başlatılıyor...');
  console.log(`📍 Backend: ${BACKEND_URL}`);
  console.log(`🖥️  Device ID: ${DEVICE_ID}`);

  // Cihazı kaydet
  await registerDevice();

  // Komutları dinlemeye başla
  setInterval(pollCommands, POLL_INTERVAL);

  // Test: Eğer MAC adresi belirtilmişse, 10 saniye sonra aç
  if (TARGET_MAC) {
    console.log(`⏰ 10 saniye içinde bilgisayar açılacak: ${TARGET_MAC}`);
    setTimeout(() => {
      powerOnComputer(TARGET_MAC);
    }, 10000);
  }
}

main().catch(console.error);

// API: REST endpoint'i (test için)
if (process.env.ENABLE_LOCAL_API === 'true') {
  const express = require('express');
  const app = express();
  app.use(express.json());

  app.post('/power-on', async (req, res) => {
    const { mac } = req.body;
    try {
      await wakeOnLan(mac || TARGET_MAC);
      res.json({ success: true, message: 'Bilgisayar açılıyor' });
    } catch (error) {
      res.status(500).json({ error: error.message });
    }
  });

  app.listen(3001, () => {
    console.log('🔌 Local API: http://localhost:3001');
  });
}
