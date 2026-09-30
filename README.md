# Telefondan Kapalı Windows PC'yi Uzaktan Açma

Kapalı bir PC internetten açılamaz, ağda hep açık bir "aracı" gerekir. İki kod gerektirmeyen yol:

## Yol 1: Akıllı Priz + BIOS (önerilen)

1. **BIOS ayarı:** PC'yi yeniden başlatıp BIOS'a gir (Del/F2). Şu ayarı bul ve aç:
   - `Restore on AC Power Loss` / `AC Back` / `After Power Loss` -> **Power On** (veya *Always On*)
   - Kaydet ve çık.
2. **Test:** PC'yi kapat, fişini çek, tekrar tak. PC kendiliğinden açılıyorsa ayar doğru.
3. **Akıllı priz:** Wi-Fi'li bir priz al (Tapo P100/P110, Shelly Plug S, Tuya uyumlu vb.). PC'yi prize tak.
4. **Uygulama:** Prizin iOS uygulamasını kur, hesap aç, prizi ekle. Uygulama internet üzerinden de çalışır.
5. **Kullanım:** PC'yi normal kapat (Başlat -> Kapat). Açmak için uygulamadan prizi kapat, 5 sn bekle, aç. PC açılır.

Notlar:
- PC'yi kapatırken priz açık kalmalı. Prizi sadece açmak için kapatıp açarsın.
- Laptop'ta pil yüzünden bu yöntem çalışmaz, WoL veya Yol 2 gerekir.
- Şifreli disk / güncelleme ekranı gibi durumlarda PC açılınca açılış ekranında bekleyebilir.

## Yol 2: Router'da Uzaktan Wake-on-LAN

Router hep açık olduğu için aracı olur.

1. **PC'de WoL'u aç:**
   - BIOS: `Wake on LAN` / `Power On By PCI-E` -> Enabled
   - Windows: Aygıt Yöneticisi -> Ağ bağdaştırıcısı -> Özellikler -> Güç Yönetimi -> "Bu aygıtın bilgisayarı uyandırmasına izin ver" + "Yalnızca sihirli paket"
   - Ayrıca Gelişmiş sekmesinde `Wake on Magic Packet` -> Enabled
   - Denetim Masası -> Güç Seçenekleri -> "Hızlı başlatma"yı kapat
2. **PC'yi Ethernet ile bağla** (Wi-Fi ile WoL çoğunlukla çalışmaz).
3. **MAC adresi:** PowerShell'de `getmac /v`.
4. **Router:** WoL destekleyen modelde (ASUS: Ağ Araçları -> Wake on LAN, Fritz!Box: Ev Ağı -> Ağ, Keenetic, OpenWrt `etherwake`) uzaktan erişimi aç.
5. **iOS:** Router'ın kendi uygulaması (ASUS Router, FRITZ!App, Keenetic) veya hazır bir WoL uygulaması (ör. Mocha WOL) ile PC'yi seç ve uyandır.
6. Router'ın uzaktan erişimi yoksa **Tailscale** kur (router veya ağdaki başka bir cihaz üzerinden) ve WoL'u onun üzerinden gönder.

## Hangisi?

| | Yol 1 | Yol 2 |
|---|---|---|
| Ek maliyet | Priz (~300-500 TL) | Yok (router destekliyorsa) |
| Laptop | Hayır | Evet (Ethernet) |
| Kurulum | Kolay | Orta |
