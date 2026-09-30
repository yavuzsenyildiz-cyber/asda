# Kurulum Rehberi

## 📋 Gereksinimler

- Node.js 16+
- npm veya yarn
- Xcode (iOS geliştirme için)
- Windows bilgisayarın MAC adresi

## 🔧 Adım 1: MAC Adresini Bul

### Windows'ta:
```bash
ipconfig /all
```

Bulduğunuz MAC adresini not alın. Örnek: `00:11:22:33:44:55`

### MAC Adresinizi Etkinleştir

1. BIOS/UEFI'ye gir
2. "Wake on LAN" veya "Power on by PCI-E" seçeneğini aktif et
3. Ağ kartı ayarlarında "Wake on Magic Packet"ı aç

## 🖥️ Adım 2: Backend Sunucusunu Kurulum

```bash
cd backend
npm install
npm start
```

Sunucu `http://localhost:3000`'de çalışacak.

### Üretim Ortamına Deploy

Heroku, Railway, AWS Lambda vb. ile deploy edebilirsiniz.

**Environment Variables:**
```
PORT=3000
JWT_SECRET=guzlu-anahtari-degistir
NODE_ENV=production
```

## 💻 Adım 3: Windows Agent Kurulum

### .env Dosyasını Düzenle

```bash
cd windows-agent
```

`.env` dosyasını aç ve düzenle:

```env
BACKEND_URL=http://your-backend-url
DEVICE_ID=unique-device-id-123
AGENT_TOKEN=jwt-token-from-backend
TARGET_MAC=00:11:22:33:44:55
```

**Device ID ve Token Almak:**

1. Backend çalışırken, curl ile test et:

```bash
curl -X POST http://localhost:3000/api/auth/register-device \
  -H "Content-Type: application/json" \
  -d '{
    "deviceName": "Ev PC",
    "macAddress": "00:11:22:33:44:55"
  }'
```

Yanıt:
```json
{
  "deviceId": "550e8400-e29b-41d4-a716-446655440000",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

2. Bu değerleri `.env` dosyasına kopyala

3. Agent'ı başlat:

```bash
npm install
npm start
```

### Windows Service Olarak Kurulum (İsteğe bağlı)

NSSM kullanarak otomatik başlatma:

```bash
# NSSM indir: https://nssm.cc/download
nssm install RemotePCAgent "C:\Program Files\nodejs\node.exe" "C:\path\to\index.js"
nssm start RemotePCAgent
```

## 📱 Adım 4: iOS Uygulamasını Kurulum

1. Xcode'da `ios/RemotePCApp.xcodeproj` aç
2. Signing & Capabilities'de kişisel hesabını seç
3. İlk değeri değiştir:
   - Uygulamayı çalıştır: Cmd+R

### Backend URL'sini Yapılandır

Uygulamadaki Ayarlar → Sunucu Değiştir:

```
http://your-backend-url:3000
```

## 🧪 Test

### 1. Backend Sağlığını Kontrol Et

```bash
curl http://localhost:3000/api/health
```

Yanıt:
```json
{"status":"ok","timestamp":"..."}
```

### 2. Cihaz Kaydını Test Et

```bash
curl -X POST http://localhost:3000/api/auth/register-device \
  -H "Content-Type: application/json" \
  -d '{
    "deviceName": "Test PC",
    "macAddress": "00:11:22:33:44:55"
  }'
```

### 3. Bilgisayarı Aç Komutu Gönder

```bash
TOKEN="your-token-here"
curl -X POST http://localhost:3000/api/device/power-on \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json"
```

## 🔒 Güvenlik Notları

1. **JWT_SECRET değiştir**: Production'da güçlü bir anahtar kullan
2. **HTTPS kullan**: Backend'i HTTPS ile serve et
3. **Network segmentation**: Agent ve backend'i güvenli ağda tut
4. **Firewall**: Yalnızca gerekli portları aç

## 🐛 Sorun Giderme

### WoL paketleri gönderilmiyor
- BIOS'ta "Wake on LAN" aktif olduğundan emin ol
- MAC adresini doğru gir
- Aynı ağda olduğundan emin ol

### Backend bağlantısı başarısız
- Backend URL'sini doğru gir
- Firewall ayarlarını kontrol et
- `BACKEND_URL` ortam değişkenini kontrol et

### iOS uygulaması bağlanmıyor
- Telefon ve sunucunun aynı ağda olup olmadığını kontrol et
- Backend URL'sini doğru gir
- Token'ın geçerli olduğundan emin ol
