# 🚀 Hızlı Başlangıç

5 dakikada telefondan bilgisayarınızı açın!

## Adım 1: Windows MAC Adresini Bul

Windows PowerShell'i aç ve çalıştır:

```powershell
ipconfig /all
```

Çıktıda `Physical Address` bulup not al. Örnek:
```
00-11-22-33-44-55
```

## Adım 2: BIOS'ta Wake-on-LAN Aktif Et

1. Bilgisayarı yeniden başlat
2. Startup sırasında **Del** veya **F2** tuşuna bas (marka'ya göre değişir)
3. Network → Wake-on-LAN → **Enable**
4. Kaydet ve çık

## Adım 3: Backend'i Çalıştır

```bash
cd backend
npm install
npm start
```

Tarayıcıda test et:
```
http://localhost:3000/api/health
```

## Adım 4: Cihaz Kaydı

Terminal'de çalıştır (MAC adresini değiştir):

```bash
curl -X POST http://localhost:3000/api/auth/register-device \
  -H "Content-Type: application/json" \
  -d '{
    "deviceName": "Ev PC",
    "macAddress": "00:11:22:33:44:55"
  }'
```

**Çıktı:**
```json
{
  "deviceId": "550e8400-e29b-41d4-a716-446655440000",
  "token": "eyJ...",
  "message": "Cihaz kaydedildi"
}
```

Bu değerleri kaydet!

## Adım 5: Windows Agent'ı Kur

```bash
cd windows-agent
npm install
```

`.env` dosyasını düzenle:

```env
BACKEND_URL=http://localhost:3000
DEVICE_ID=550e8400-e29b-41d4-a716-446655440000
AGENT_TOKEN=eyJ...
TARGET_MAC=00:11:22:33:44:55
ENABLE_LOCAL_API=true
```

Agent'ı başlat:

```bash
npm start
```

## Adım 6: iOS Uygulamasını Kur

1. Xcode aç: `ios/RemotePCApp.xcodeproj`
2. `RemotePCApp` scheme'ini seç
3. **Run** (Cmd+R)

## Adım 7: Test Et

### iOS'tan:
1. Device ID'yi gir: `550e8400-e29b-41d4-a716-446655440000`
2. **Giriş Yap**
3. **Kontrol** sekmesine git
4. **Aç** butonuna bas

### Windows'ta:
Bilgisayar açılmalı! 🎉

Eğer açılmazsa, [Sorun Giderme](./setup.md#-sorun-giderme) bölümüne bak.

---

## 🔥 Bonus: Deploy Etme (Opsiyonel)

### Heroku'ya Deploy

```bash
# Heroku CLI'ı indir: https://devcenter.heroku.com/articles/heroku-cli

heroku create your-remote-pc-app
heroku config:set JWT_SECRET=your-secret
git push heroku main
```

Backend URL'si: `https://your-remote-pc-app.herokuapp.com`

### Railway'e Deploy

1. [Railway.app](https://railway.app) git up
2. `backend/` klasörünü import et
3. ENV variables'ı ayarla
4. Deploy

---

## 💡 İpuçları

- **Güvenlik**: Production'da `JWT_SECRET`'ı değiştir
- **Uzaktan Erişim**: Backend'i ngrok ile tunnel'la test etmek için:
  ```bash
  ngrok http 3000
  ```
- **Logs**: Windows Agent'da `npm run dev` kullan (auto-restart)

---

## ❓ Soru mı var?

- [API Dökümentasyonu](./api.md)
- [Kurulum Rehberi](./setup.md)
