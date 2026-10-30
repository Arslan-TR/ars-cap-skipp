# ARS-SKIPP — Ücretsiz Yapay Zekâ reCAPTCHA Çözücü

[English](README.md) | **Türkçe**

[![Lisans: MIT](https://img.shields.io/badge/lisans-MIT-blue.svg)](LICENSE)
![Manifest V3](https://img.shields.io/badge/Chrome-Manifest%20V3-1d4ed8)
![Chrome 111+](https://img.shields.io/badge/Chrome-111%2B-3b82f6)

GitHub: https://github.com/Arslan-TR/ars-cap-skipp

reCAPTCHA görsel doğrulamalarını, tarayıcının içinde ve kendi işlemcinizde (CPU) çalışan ONNX sinir ağlarıyla otomatik çözen bir Chrome eklentisidir. Temel eklenti ücretsizdir; API anahtarı veya kayıt gerekmez.

## İçindekiler

- [Ekran görüntüleri](#ekran-görüntüleri)
- [Özellikler](#özellikler)
- [Desteklenen doğrulamalar](#desteklenen-doğrulamalar)
- [Gereksinimler](#gereksinimler)
- [Kurulum](#kurulum)
- [Kullanım](#kullanım)
- [Ayarlar](#ayarlar)
- [Nasıl çalışır](#nasıl-çalışır)
- [Proje yapısı](#proje-yapısı)
- [Veri toplama ve gizlilik](#veri-toplama-ve-gizlilik)
- [WS eklentisi](#ws-eklentisi)
- [Sorun giderme](#sorun-giderme)
- [Lisans](#lisans)

## Ekran görüntüleri

<p align="center">
  <img src="docs/store/screenshot-1.jpg" width="760" alt="ARS-SKIPP görsel doğrulamayı çözerken, açılır pencere açık">
</p>

| Açılır pencere | Zaman aşımları |
|----------------|----------------|
| <img src="docs/store/screenshot-2.jpg" alt="Çözücü anahtarlarının bulunduğu ana açılır pencere"> | <img src="docs/store/screenshot-3.jpg" alt="Gecikme ayarlarının bulunduğu Timeouts sayfası"> |

| Raporlar (varsayılan kapalı) | Nasıl çalışır |
|------------------------------|---------------|
| <img src="docs/store/screenshot-4.jpg" alt="Varsayılan olarak kapalı Reports sayfası"> | <img src="docs/store/screenshot-5.jpg" alt="Çözücünün çalışma adımları: özet arama, cihaz üzerinde yapay zekâ, tıkla ve doğrula"> |

## Özellikler

- reCAPTCHA v2 görsel doğrulamalarını (3×3 ve 4×4 ızgara) cihaz üzerindeki yapay zekâ modelleriyle yerel olarak çözer.
- reCAPTCHA onay kutusunu kendiliğinden açar ve kullanıcı müdahalesi olmadan çözmeye başlar.
- Algısal özet (perceptual hash) önbelleği: Çıkarım çalışmadan önce, doğrulanmış cevaplara sahip bilinen görsellerin bulunduğu paketli SQLite veritabanına (`extension/db/captcha.sqlite`) bakılır. Bu hem hızı hem doğruluğu artırır.
- Tıklamaların sabit aralıklarla olmaması için rastgele sapmalı (jitter), ayarlanabilir gecikmeler.
- Site bazlı devre dışı bırakma listesi.
- Mavi, koyu temalı açılır pencere; 11 dilde çeviri (ar, de, en, es, fr, id, ja, ms, pt, ru, zh).
- Yalnızca `*.google.com/recaptcha/*` ve `*.recaptcha.net/recaptcha/*` çerçevelerinde çalışır.

## Desteklenen doğrulamalar

Çok sınıflı ızgara modeli (`models/grid.onnx`) şu nesne türlerini tanır:

`bisiklet`, `otobüs`, `baca`, `yaya geçidi`, `yangın musluğu`, `motosiklet`, `parkmetre`, `merdiven`, `taksi`, `traktör`, `trafik lambası`

Motosiklet 4×4 durumu için ayrı bir `motorcycles_b1` modeli bulunur. `models/type.onnx`, 3×3 doğrulamalarda kareleri tek tek sınıflandırır.

## Gereksinimler

- Google Chrome 111 veya üzeri (ya da Manifest V3 destekleyen başka bir Chromium tarayıcı).
- Yaklaşık 110 MB disk alanı (modeller ve WASM çalışma zamanları pakete dahildir).
- İlk açılışta modeller yüklenirken eklenti 5–15 saniye bekleyebilir.

## Kurulum

### Temel eklenti (Chrome 111+)

1. Depoyu klonlayın veya indirin:
   ```bash
   git clone https://github.com/Arslan-TR/ars-cap-skipp.git
   ```
2. `chrome://extensions` sayfasını açın.
3. Sağ üstten **Geliştirici modu**nu açın.
4. **Paketlenmemiş öğe yükle**ye tıklayın.
5. `extension/` klasörünü seçin.
6. Kurulumdan sonra çözücü tepki vermezse tarayıcıyı yeniden başlatın.

### WS eklentisi (Chrome 116+, isteğe bağlı)

WS eklentisi, otomatik iş akışları için WebSocket tabanlı uzaktan kontrol ekler. Temel eklentinin üzerine kurulur. Bkz. [`ws-addon/README.tr.md`](ws-addon/README.tr.md).

## Kullanım

1. Herhangi bir reCAPTCHA içeren sayfayı açın.
2. Varsayılan ayarlarla eklenti onay kutusuna kendisi tıklar ve görsel doğrulamayı çözer.
3. Özellikleri tek tek açıp kapatmak için eklenti simgesine tıklayın:

| Açılır pencere anahtarı | Ne yapar |
|-------------------------|----------|
| Solver enabled | Ana açma/kapama anahtarı |
| reCAPTCHA support | reCAPTCHA çerçevelerinin işlenmesini açar |
| Auto-click buttons | Onay kutusuna ve Verify düğmesine otomatik tıklar |
| Solve image challenges | Görsel doğrulamalarda yapay zekâ modellerini çalıştırır |
| WS mode | Uzaktan kontrol modu (yalnızca WS eklentisi ve 32 karakterlik anahtarla görünür) |

Açılır pencerede ayrıca **Timeouts** (Zaman aşımları) ve **Reports** (Raporlar) sayfaları ile bu depoya giden bir bağlantı bulunur.

## Ayarlar

Açılır penceredeki **Timeouts** sayfasını açın:

| Ayar | Varsayılan | Açıklama |
|------|------------|----------|
| Between tile clicks | 300 ms | Tek tek kare tıklamaları arasındaki bekleme (yalnızca 3×3) |
| Dynamic reveal → click | 850 ms | Yeni bir dinamik kare görselinin belirmesinden tıklamaya kadar bekleme (tanıma için harcanan süre buna sayılır) |
| Last click → verify | 850 ms | Son kare tıklaması ile Verify düğmesine basma arasındaki bekleme |
| Disabled sites | — | Eklentinin çalışmayacağı alan adları |

Her zaman aşımına, her tetiklendiğinde rastgele 0–300 ms eklenir. 3×3 doğrulamada kareler rastgele sırayla tıklanır.

## Nasıl çalışır

1. MAIN dünyasında çalışan bir içerik betiği (`eventhook/loader.js`) sayfanın `addEventListener` fonksiyonunu sarar; ikinci içerik betiği (`eventhook.js`, `captcha/recaptcha.js`) reCAPTCHA çerçevelerindeki doğrulama arayüzünü okur.
2. Her görselin algısal özeti çıkarılır (`captcha/phash-browser.js`) ve `sql.js` ile paketli SQLite önbelleğinde aranır. Önbellekte bulunursa doğrulanmış cevap, çıkarım yapılmadan döner.
3. Bulunamazsa görseller, `onnxruntime-web` (WASM, CPU) ile tarayıcıda çalışan ONNX modellerine verilir: `models/type.onnx` her karede hedef nesne olup olmadığına karar verir (3×3); `models/grid.onnx` her kare konumunu puanlar (4×4).
4. Eşleşen kareler tıklanır, ardından ayarlanan gecikmeden sonra Verify'a basılır.
5. Karşılaşılan görseller ve cevapları IndexedDB'de saklanır ve periyodik olarak uzak bir sunucuya yüklenir (aşağıya bakın).

## Proje yapısı

```
ARS-SKIPP/
├── extension/                 Temel Manifest V3 eklentisi (bu klasörü yükleyin)
│   ├── manifest.json
│   ├── background.js          Servis çalışanı, depolama, rapor kayıtları
│   ├── background_sqlite.js   SQLite önbellek erişimi
│   ├── uploader.js            Veri seti yükleyici (raporlar)
│   ├── captcha/               Doğrulama algılama, pHash, yapay zekâ çıkarımı
│   ├── eventhook/, eventhook.js  reCAPTCHA çerçeveleri için olay kancaları
│   ├── lib/                   sql.js (WASM içinde SQLite)
│   ├── libs/onnxruntime-web/  ONNX Runtime Web
│   ├── models/                grid.onnx, type.onnx, motorcycles_b1.onnx (+ meta)
│   ├── db/captcha.sqlite      Doğrulanmış cevaplı bilinen görsel özetleri
│   ├── popup.html/css/js      Açılır pencere arayüzü
│   ├── reports.html/js        Raporlar sayfası
│   ├── ws/background_ws.js    WS taslağı (eklenti tarafından değiştirilir)
│   ├── _locales/              11 dilde arayüz çevirisi
│   └── icon/                  Mavi eklenti simgeleri
├── ws-addon/                  İsteğe bağlı WebSocket uzaktan kontrol katmanı
├── LICENSE
├── README.md                  İngilizce sürüm
└── README.tr.md               Bu dosya (Türkçe)
```

## Veri toplama ve gizlilik

Kurmadan önce lütfen okuyun.

- **Raporlar varsayılan olarak kapalıdır (isteğe bağlı).** Çözme işlemi tamamen sizin makinenizde olur ve hiçbir şey yüklenmez.
- Raporları açarsanız (açılır pencere → **Reports** → **Enable reports**), eklenti IndexedDB'de tuttuğu doğrulama görsellerini, seçilen kareleri ve çözüm sonucunu, eğitim veri setini büyütmek için periyodik olarak `captcharaptor.com` adresine (özgün üst proje sunucusu) yükler.
- Her tarayıcı profili için rastgele bir rapor anahtarı üretilir ve yerelde saklanır. Bir hesaba bağlı değildir. Raporlar açıkken anahtar, her yüklemede sunucuya gönderilir (`X-Auth-Key` başlığı ve istek adresi içinde).
- Açılır pencere metni bunu belirtir: modeller yerelde çalışır ve Reports açılmadıkça hiçbir şey yüklenmez.
- Raporlar açıkken çözdüğünüz reCAPTCHA içeren sayfalar yüklemeye konu olabilir; içeriği gizli saydığınız sayfalarda eklentiyi kullanmayın.

## WS eklentisi

`ws-addon/`, temel eklentinin üzerine bir WebSocket istemcisi ekler; böylece eklenti, 2captcha / AntiCaptcha biçimindeki görevler için kişisel bir çözüm işçisi gibi çalışabilir. Chrome 116+, ek izinler (`tabs`, `debugger`, `offscreen`, tüm URL'ler) ve üst projedeki CaptchaPlugin hizmetinden bir API anahtarı gerektirir. Ayrıntılar: [`ws-addon/README.tr.md`](ws-addon/README.tr.md).

> Eklenti `wss://ws.captcharaptor.com` adresine bağlanır. Sunucu istemci anahtarı artık kodun içine gömülü değildir: kendi anahtarınızı `chrome.storage.local` içinde `ws_auth_token` adıyla saklamanız gerekir (bkz. [`ws-addon/README.tr.md`](ws-addon/README.tr.md)). Anahtar yoksa eklenti bağlanmaz. Eklentiyi üçüncü taraf uzaktan kontrol kodu olarak değerlendirin ve yalnızca ne yaptığını anlıyorsanız kurun.

## Sorun giderme

| Sorun | Çözüm |
|-------|-------|
| Kurulumdan sonra bir şey olmuyor | Tarayıcıyı yeniden başlatın; `chrome://extensions` içinde servis çalışanı hatalarına bakın |
| İlk çözüm yavaş | Modeller yükleniyor (5–15 sn). Sonraki çözümler daha hızlıdır |
| reCAPTCHA İngilizce değil | Modeller yalnızca İngilizce etiketleri anladığı için eklenti İngilizceye geçirir |
| Bir sitede çalışmıyor | **Disabled sites** listesine ve açılır penceredeki anahtarların açık olduğuna bakın |
| Bellek kullanımı yüksek | Üç ONNX modeli büyüktür; diğer ağır sekmeleri kapatın |

## Lisans

MIT — bkz. [LICENSE](LICENSE). Lisansın gerektirdiği şekilde özgün telif bildirimi (Raptor) korunmuştur.

Depo: https://github.com/Arslan-TR/ars-cap-skipp
