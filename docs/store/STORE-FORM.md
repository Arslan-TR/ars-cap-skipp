# Store form — ARS-SKIPP: AI Captcha Image Solver v0.2.3600

Everything below is final text to paste into the Chrome Web Store developer dashboard.

## Audit

- Manifest: MV3. Name 34 chars (max 75). Summary 113 chars (max 132). Version `0.2.3600`. Icons 16/32/48/128 present.
- Permissions: `storage`, `alarms`, `idle`, `declarativeNetRequest` — all used (see Privacy → justifications). Removed nothing; no unused permissions found.
- Host permissions: `*://*.google.com/recaptcha/*` (used by content scripts and the background image fetch). Content scripts also match `*://*.recaptcha.net/recaptcha/*`.
- Remote code: none. All JS, WASM, ONNX models and the SQLite database ship in the package; `importScripts` only loads packaged files.
- Network requests: none by default. With Reports enabled (opt-in, off by default): `https://captcharaptor.com/upload.php` and `/status.php`. Challenge images are fetched from Google's reCAPTCHA pages.
- Data handled → CWS data types: **Website content** (challenge images/text). Nothing else.
- Package: upload only `extension/` contents. The `ws-addon/` overlay uses `debugger`/`tabs`/`<all_urls>` and a third-party WebSocket service; **do not** submit it to the store.

## Store listing

- Language: English
- Description:
  ```
  ARS-SKIPP solves image captcha challenges for you, right inside your browser.

  When a reCAPTCHA v2 image challenge appears, the extension opens the checkbox, recognises the tiles with neural networks that run on your own CPU, clicks the matching ones and presses Verify. No account, no API key, no subscription.

  Features
  - Handles 3x3 and 4x4 image grids (bicycles, buses, crosswalks, fire hydrants, motorcycles, parking meters, stairs, taxis, tractors, traffic lights and more)
  - Runs on your device: the AI models and a database of known image hashes are bundled in the extension
  - Adjustable delays between clicks, dynamic-tile reveal and verify, with random jitter
  - Master switch and per-feature switches in the popup
  - Interface languages bundled: Arabic, German, English, Spanish, French, Indonesian, Japanese, Malay, Portuguese, Russian, Chinese

  How it works
  1. Each challenge image is hashed and looked up in a bundled database of known answers.
  2. Unknown images are classified by ONNX neural networks running locally.
  3. Matching tiles are clicked and the challenge is verified.

  Privacy
  Solving happens entirely in your browser. Nothing is uploaded unless you turn on the optional Reports feature (off by default), which sends challenge images to captcharaptor.com to improve the models. Full policy: https://github.com/Arslan-TR/ars-cap-skipp/blob/main/docs/PRIVACY.md

  First use: loading the models can take 5-15 seconds. If nothing happens after installing, restart the browser.

  Open source (MIT): https://github.com/Arslan-TR/ars-cap-skipp
  ```
- Category: Tools
- Icon: `extension/icon/128.png` (128x128 PNG)
- Screenshots: `docs/store/screenshot-1.jpg` … `screenshot-5.jpg` (1280x800 JPEG). Source templates and the render script are in `docs/store/src/` and `scripts/render_store_assets.py`.
- Small promo tile: `docs/store/promo-440x280.jpg`
- Marquee promo tile: `docs/store/marquee-1400x560.jpg`
- YouTube video: empty
- Official URL: empty
- Homepage URL: https://github.com/Arslan-TR/ars-cap-skipp
- Support URL: https://github.com/Arslan-TR/ars-cap-skipp/issues
- Mature content: No

## Privacy

- Single purpose:
  ```
  Automatically solves captcha image challenges (reCAPTCHA v2 image grids) in the user's browser using neural networks that run on the device.
  ```
- Permission justifications:
  - `storage`:
    ```
    Saves the user's settings (switches and click delays), a local log of challenge images used by the optional Reports feature, and the Reports configuration. Nothing narrower can persist these between browser sessions.
    ```
  - `alarms`:
    ```
    Schedules the periodic check that runs the optional Reports upload. The upload only happens if the user has turned Reports on (off by default).
    ```
  - `idle`:
    ```
    Triggers the same optional Reports check when the computer becomes idle, so uploads do not compete with the user's browsing. Does nothing unless Reports is enabled.
    ```
  - `declarativeNetRequest`:
    ```
    Adds a single dynamic rule that appends hl=en to reCAPTCHA frame requests so the challenge text is shown in English. The recognition models only understand English labels.
    ```
  - Host permission `*://*.google.com/recaptcha/*`:
    ```
    The solver runs only inside reCAPTCHA frames. The extension needs access to these frames to read the challenge images and tiles and to fetch the challenge images for recognition. No other sites are accessed.
    ```
- Remote code: No
- Data types to check: **Website content** — everything else unchecked
- Certifications: all three checked
- Privacy policy URL: https://github.com/Arslan-TR/ars-cap-skipp/blob/main/docs/PRIVACY.md

## Distribution

- Free of charge · Public · All regions

## Test instructions

```
No account or sign-in is needed.
1. Install the extension and restart the browser (the AI models load on first use, which can take 5-15 seconds).
2. Open https://www.google.com/recaptcha/api2/demo
3. The extension clicks the "I'm not a robot" checkbox and, if an image challenge appears, selects the matching tiles and presses Verify. This uses the host permission, declarativeNetRequest (the frame is requested with hl=en) and storage.
4. Click the extension icon: switch features on or off, open "Timeouts" to change delays (saved with storage).
5. Open "Reports": the switch is off by default; with it off nothing is uploaded (alarms and idle only run the optional upload check).
```

## Before you submit (human steps)

- Register the developer account (one-time US$5) and **verify the contact e-mail** under Account → Settings.
- Keep the GitHub repository **public** so the privacy-policy link opens.
- Build the package: `python scripts/build_zip.py`, then upload `dist/ars-skipp-v0.2.3600.zip` (manifest.json is at the zip root).
- Bump `version` in `extension/manifest.json` for every later upload.
