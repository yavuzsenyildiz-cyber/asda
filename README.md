# Remote PC Power On

Telefondan (iOS) uzaktan Windows bilgisayarını açan sistem.

## 📋 Mimari

```
iOS App (Swift UI) 
    ↓ (HTTPS API)
Backend Server (Node.js)
    ↓ (WebSocket)
Windows Agent (Node.js)
    ↓ (WoL Paket)
Windows PC
```

## 📁 Yapı

- `backend/` - REST API Server
- `windows-agent/` - Windows tarafında çalışan agent
- `ios/` - iOS uygulaması (Swift)
- `docs/` - Dokümantasyon

## 🚀 Kurulum

### Backend
```bash
cd backend
npm install
npm start
```

### Windows Agent
```bash
cd windows-agent
npm install
npm start
```

### iOS
Xcode'da açıp çalıştır.

## 🔧 Konfigürasyon

Ayrıntılar için `docs/setup.md`'e bakın.
