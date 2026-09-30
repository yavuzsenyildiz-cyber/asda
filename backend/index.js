const express = require('express');
const cors = require('cors');
require('dotenv').config();
const jwt = require('jsonwebtoken');
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = process.env.PORT || 3000;
const JWT_SECRET = process.env.JWT_SECRET || 'your-secret-key-change-this';

app.use(cors());
app.use(express.json());

// In-memory storage (production'da database kullanın)
const devices = new Map();
const sessions = new Map();

// Middleware: JWT doğrulama
const authenticateToken = (req, res, next) => {
  const authHeader = req.headers['authorization'];
  const token = authHeader && authHeader.split(' ')[1];

  if (!token) return res.sendStatus(401);

  jwt.verify(token, JWT_SECRET, (err, user) => {
    if (err) return res.sendStatus(403);
    req.user = user;
    next();
  });
};

// ============ AUTH ============

// Cihaz kaydet
app.post('/api/auth/register-device', (req, res) => {
  const { deviceName, macAddress } = req.body;

  if (!deviceName || !macAddress) {
    return res.status(400).json({ error: 'deviceName ve macAddress gerekli' });
  }

  const deviceId = uuidv4();
  const token = jwt.sign({ deviceId }, JWT_SECRET, { expiresIn: '30d' });

  devices.set(deviceId, {
    id: deviceId,
    deviceName,
    macAddress,
    createdAt: new Date(),
  });

  res.json({
    deviceId,
    token,
    message: 'Cihaz kaydedildi',
  });
});

// Cihaz oturum aç
app.post('/api/auth/login', (req, res) => {
  const { deviceId } = req.body;

  if (!deviceId || !devices.has(deviceId)) {
    return res.status(401).json({ error: 'Geçersiz deviceId' });
  }

  const token = jwt.sign({ deviceId }, JWT_SECRET, { expiresIn: '30d' });

  res.json({
    token,
    device: devices.get(deviceId),
  });
});

// ============ DEVICE CONTROL ============

// Bilgisayarı aç (iOS'tan gelen istek)
app.post('/api/device/power-on', authenticateToken, (req, res) => {
  const deviceId = req.user.deviceId;
  const device = devices.get(deviceId);

  if (!device) {
    return res.status(404).json({ error: 'Cihaz bulunamadı' });
  }

  // Agent'a mesaj gönder
  const commandId = uuidv4();
  sessions.set(commandId, {
    deviceId,
    command: 'power-on',
    status: 'pending',
    createdAt: new Date(),
  });

  // WebSocket üzerinden agent'a gönderecek
  // (aşağıda WebSocket implementasyonu yapılacak)

  res.json({
    commandId,
    status: 'sent',
    message: 'Açma komutu gönderildi',
  });
});

// Komut durumunu kontrol et
app.get('/api/device/command-status/:commandId', authenticateToken, (req, res) => {
  const { commandId } = req.params;
  const session = sessions.get(commandId);

  if (!session) {
    return res.status(404).json({ error: 'Komut bulunamadı' });
  }

  res.json(session);
});

// Cihazları listele
app.get('/api/devices', authenticateToken, (req, res) => {
  const deviceId = req.user.deviceId;
  const device = devices.get(deviceId);

  if (!device) {
    return res.status(404).json({ error: 'Cihaz bulunamadı' });
  }

  res.json(device);
});

// ============ HEALTH CHECK ============

app.get('/api/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date() });
});

// ============ SERVER START ============

app.listen(PORT, () => {
  console.log(`🚀 Backend sunucusu http://localhost:${PORT} adresinde çalışıyor`);
});

module.exports = { app, devices, sessions };
