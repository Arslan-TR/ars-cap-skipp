# Privacy Policy — ARS-SKIPP: AI Captcha Image Solver

*Last updated: 2026-10-30*

ARS-SKIPP solves captcha image challenges on your own device. It does not collect, sell or share personal data, and it uploads nothing unless you turn on the optional **Reports** feature.

## What the extension accesses

- **Captcha challenge content** (the tile images and instruction text of reCAPTCHA frames on `google.com/recaptcha` and `recaptcha.net/recaptcha`): read so the on-device models can decide which tiles to click. This is processed in your browser and is not sent anywhere by the solving feature.
- No browsing history, no page content outside those challenge frames, no passwords, no account data, no location, no keystrokes.

## What is stored (on your device only)

- **Settings** (switches and delay values) in Chrome's extension storage.
- **A local log** of the challenge images the extension has seen, with the answers it gave, in the extension's own IndexedDB. It exists to support the optional Reports feature; entries are deleted after a successful upload, and the image store has a size limit.
- **A random reporting key**, generated once per browser profile. It is not linked to an account or to you.

## What is sent and to whom

- **By default: nothing.** Solving uses only files bundled in the extension. The extension loads challenge images from Google's reCAPTCHA pages, the same requests the page itself makes.
- **Only if you enable Reports** (popup → Reports → *Enable reports*): the logged challenge images, the tiles that were selected, the solve result and the random reporting key are uploaded periodically to `captcharaptor.com` (`upload.php` and `status.php`), to help improve the recognition models. You can switch Reports off at any time; the upload stops immediately. No personal identifiers are included.
- No analytics, advertising or tracking services are used. No data is sold or used for any purpose other than improving the captcha-recognition models.

## Chrome Web Store disclosure

The store's Privacy tab declares **Website content** (captcha challenge images and text read from reCAPTCHA frames), handled on the device and, only with Reports enabled, uploaded as described above. No other data types are handled.

## Permissions

- `storage`: save your settings, the local log and the reporting configuration.
- `alarms`: schedule the periodic check for the optional Reports upload.
- `idle`: run that same optional check when the computer is idle.
- `declarativeNetRequest`: add the `hl=en` parameter to reCAPTCHA frame requests so challenge text is shown in English, which the models understand.
- Host access `*://*.google.com/recaptcha/*`: run the solver in reCAPTCHA frames and fetch the challenge images shown there.

## Contact

Questions or requests: https://github.com/Arslan-TR/ars-cap-skipp/issues

Source code: https://github.com/Arslan-TR/ars-cap-skipp
