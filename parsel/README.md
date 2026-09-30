# Parsel Takip

Emlak ve ihale ilanlarından parsel toplayan, filtreleyen ve beğendiklerini seçmene yarayan yerel uygulama.

## Çalıştırma

```bash
pip install -r requirements.txt
python app.py          # http://127.0.0.1:5000
```

İlk açılışta arayüz boş görünmesin diye **örnek veriler** eklenir (arayüzde "Örnek" etiketli, gerçek ilan değil). "Örnek verileri sil" ile kaldır.

## Ne yapar

- Filtre: il, tür (satılık / ihale), kaynak, fiyat, m², serbest arama. Sıralama: fiyat, alan, m² fiyatı, ihale son tarihi.
- Her parselde **Seç / Ele / Not**. "Seçilenler" sekmesi ve CSV indirme.
- "Şimdi tara" ile `sources.yaml` içindeki açık kaynakları tarar. Aynı ilan tekrar eklenmez, seçim ve notlar korunur.
- "Elle parsel ekle" ile herhangi bir linki listeye ekleyebilirsin.

## Kaynak ekleme (sources.yaml)

`sources.yaml` içindeki Emlakjet, Hepsiemlak ve TOKİ kayıtları **örnek şablondur ve gerçek sitelerde test edilmedi**. Bunları kullanmak için:

1. Sitenin ilan listesi sayfasını tarayıcıda aç, "Öğeyi İncele" ile ilan kutusunun ve fiyat/alan/konum öğelerinin CSS seçicilerini bul.
2. `sources.yaml`'daki seçicileri düzelt, `enabled: true` yap.
3. Arayüzden "Şimdi tara"ya bas, "Tarama durumu" bölümünden sonucu ve hataları gör.

Milli Emlak, belediye ihaleleri, EKAP ve UYAP icra satışları için de aynı şekilde kaynak eklenir. Giriş gerektiren sayfalar desteklenmez.

## Sınırlar

- Tarayıcı `robots.txt`'e uyar ve istekler arasında bekler. Site erişimi engellerse (403/429) o kaynak atlanır, hata durum bölümünde görünür.
- sahibinden gibi bazı siteler otomatik veri çekmeyi kullanım şartlarında yasaklar ve teknik olarak engeller. Kullanım şartlarına uymak sana aittir; bu tür siteler için elle ekleme daha güvenlidir.
- Testler: `python tests/test_scraper.py` (sayı ayrıştırma ve yerel sahte siteyle tarama).
