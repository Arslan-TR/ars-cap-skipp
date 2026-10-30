# WS Eklentisi — Uzaktan Kontrol Modu

[English](README.md) | **Türkçe**

GitHub: https://github.com/Arslan-TR/ars-cap-skipp

Bu eklenti, captcha çözücünün WebSocket üzerinden uzaktan kontrol edilmesini sağlar. `extension/` klasöründeki temel eklentinin **üzerine** kopyalanmak üzere tasarlanmıştır.

Eklenti kullanıldığında, temel eklenti kendi kaynaklarınız üzerinde, üçüncü taraf hizmetlere para ödemeden kişisel bir captcha çözüm hizmeti gibi çalışır. CaptchaPlugin sunucusuna bağlanır ve gelen görevleri bekler. Görev gelince bir sekme açar, captcha'yı çözer ve token'ı geri gönderir. Bir eklenti örneği tek iş parçacığında çalışır, ancak aynı anda istediğiniz sayıda tarayıcı bağlayabilirsiniz.

Görevler standart 2captcha veya AntiCaptcha API biçiminde gönderilir. API açıklaması: https://captchaplugin.com/api.php

## Gereksinimler

- Chrome 116+
- Paketlenmemiş eklenti olarak yüklenmiş temel eklenti
- https://captchaplugin.com/keys.php adresinden bir API anahtarı

## API anahtarı alma

1. https://captchaplugin.com/ adresinde kayıt olun
2. https://captchaplugin.com/keys.php sayfasından bir anahtar üretin
3. Anahtarı eklenti açılır penceresine (Reports sekmesi) yapıştırın, ardından WS mode'u açın

## Kurulum

1. `extension/` klasörünü `chrome://extensions` içinden paketlenmemiş eklenti olarak yükleyin.
2. Bu klasördeki tüm dosyaları `extension/` dizininin **üzerine** kopyalayın:
   ```
   ws/background_ws.js         → extension/ws/background_ws.js
   ws/offscreen.html           → extension/ws/offscreen.html
   ws/offscreen.js             → extension/ws/offscreen.js
   ws/recaptcha_frame_watch.js → extension/ws/recaptcha_frame_watch.js
   manifest.json               → extension/manifest.json
   ```
3. `chrome://extensions` içinden eklentiyi yeniden yükleyin (yenile simgesi).
4. API anahtarınızı açılır pencereye yapıştırın ve WS mode'u açın.

## Neler değişir

Temel eklentiye göre bu eklenti:

- WS taslağını (`ws/background_ws.js`) tam WebSocket uygulamasıyla değiştirir
- `manifest.json` dosyasına gerekli izinleri ekler: `tabs`, `debugger`, `offscreen`
- Asgari Chrome sürümünü 111'den 116'ya çıkarır

## Nasıl çalışır

WS modu açıldığında arka plan betiği, CaptchaPlugin sunucusuyla kalıcı bir WebSocket bağlantısı tutan bir offscreen belge (`ws/offscreen.html`) açar. Bir çözüm görevi geldiğinde Chrome Debugger API'si ile kontrollü bir sekme açılır, reCAPTCHA ağ istekleri yakalanır, doğrulama sayfası enjekte edilir ve çözülen token geri döner.

## Güvenlik notu

- Eklenti `wss://ws.captcharaptor.com` adresine bağlanır; `ws/offscreen.js` içinde üst proje hizmetine ait ortak bir istemci anahtarı bulunur. Bu bir sır olarak değerlendirilmemelidir ve bu depoya ait değildir.
- Ek izinler (`debugger`, `tabs`, `<all_urls>`) çok geniştir. Yalnızca güvendiğiniz bir tarayıcı profilinde kurun.
