# API Dokümantasyonu

## Base URL
```
http://localhost:3000/api
```

## Authentication

Tüm korunan endpoint'ler JWT token gerektirir:

```
Authorization: Bearer <token>
```

## Endpoint'ler

### 1. Cihaz Kaydı

**POST** `/auth/register-device`

Yeni bir cihaz kaydeder ve JWT token döner.

**Request Body:**
```json
{
  "deviceName": "Ev PC",
  "macAddress": "00:11:22:33:44:55"
}
```

**Response (200):**
```json
{
  "deviceId": "550e8400-e29b-41d4-a716-446655440000",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "message": "Cihaz kaydedildi"
}
```

---

### 2. Giriş

**POST** `/auth/login`

Kayıtlı bir cihazla giriş yapar.

**Request Body:**
```json
{
  "deviceId": "550e8400-e29b-41d4-a716-446655440000"
}
```

**Response (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "device": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "deviceName": "Ev PC",
    "macAddress": "00:11:22:33:44:55",
    "createdAt": "2024-01-15T10:30:00Z"
  }
}
```

---

### 3. Bilgisayarı Aç

**POST** `/device/power-on`

Bilgisayarı açma komutu gönderir.

**Headers:**
```
Authorization: Bearer <token>
```

**Request Body:**
```json
{}
```

**Response (200):**
```json
{
  "commandId": "cmd-123-456-789",
  "status": "sent",
  "message": "Açma komutu gönderildi"
}
```

---

### 4. Komut Durumunu Kontrol Et

**GET** `/device/command-status/:commandId`

Gönderilen komutun durumunu kontrol eder.

**Headers:**
```
Authorization: Bearer <token>
```

**URL Parameters:**
- `commandId`: Komut ID'si

**Response (200):**
```json
{
  "deviceId": "550e8400-e29b-41d4-a716-446655440000",
  "command": "power-on",
  "status": "completed",
  "createdAt": "2024-01-15T10:35:00Z"
}
```

**Status Değerleri:**
- `pending`: Komut bekleniyor
- `sent`: Komut gönderildi
- `completed`: Komut tamamlandı
- `failed`: Komut başarısız

---

### 5. Cihaz Bilgisi

**GET** `/devices`

Cihaz bilgilerini getirir.

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "deviceName": "Ev PC",
  "macAddress": "00:11:22:33:44:55",
  "createdAt": "2024-01-15T10:30:00Z"
}
```

---

### 6. Health Check

**GET** `/health`

Sunucunun çalışıp çalışmadığını kontrol eder. Kimlik doğrulama gerekli değil.

**Response (200):**
```json
{
  "status": "ok",
  "timestamp": "2024-01-15T10:40:00Z"
}
```

---

## Error Responses

### 400 - Bad Request
```json
{
  "error": "deviceName ve macAddress gerekli"
}
```

### 401 - Unauthorized
```json
{
  "error": "Geçersiz deviceId"
}
```

### 403 - Forbidden
```json
{
  "error": "Token geçersiz veya süresi doldu"
}
```

### 404 - Not Found
```json
{
  "error": "Cihaz bulunamadı"
}
```

---

## cURL Örnekleri

### Cihaz Kaydı
```bash
curl -X POST http://localhost:3000/api/auth/register-device \
  -H "Content-Type: application/json" \
  -d '{
    "deviceName": "Ev PC",
    "macAddress": "00:11:22:33:44:55"
  }'
```

### Giriş
```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "deviceId": "550e8400-e29b-41d4-a716-446655440000"
  }'
```

### Bilgisayarı Aç
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
curl -X POST http://localhost:3000/api/device/power-on \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### Komut Durumu
```bash
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
curl -X GET http://localhost:3000/api/device/command-status/cmd-123-456-789 \
  -H "Authorization: Bearer $TOKEN"
```

---

## WebSocket (Gelecek Sürüm)

Gerçek zamanlı komut güncellemeleri için WebSocket desteği eklenecektir:

```javascript
const ws = new WebSocket('ws://localhost:3000/ws');

ws.onopen = () => {
  ws.send(JSON.stringify({ 
    type: 'auth', 
    token: 'eyJ...' 
  }));
};

ws.onmessage = (event) => {
  const message = JSON.parse(event.data);
  if (message.type === 'power-on') {
    console.log('Bilgisayar açılıyor...');
  }
};
```
