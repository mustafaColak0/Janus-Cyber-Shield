# 🛡️ Janus Cyber Shield v1.0

Janus Cyber Shield, Python tabanlı geliştirilmiş, gerçek zamanlı ağ güvenliği analizi ve gelişmiş hash kırma yeteneklerine sahip bir **Siber Güvenlik Paneli**'dir. Hem savunma (Mavi Takım) hem de saldırı (Kırmızı Takım) konseptlerini tek bir arayüzde birleştirir.

## 🚀 Temel Özellikler

* **🔍 Canlı Log & Otomatik Savunma:** `access.log` dosyalarını gerçek zamanlı izleyerek `etc/passwd`, `powershell` ve `SQL Injection` gibi saldırı girişimlerini anında tespit eder.
* **🚫 Otomatik Güvenlik Duvarı:** Tespit edilen saldırgan IP adreslerini Windows Firewall (netsh) üzerinden otomatik olarak mühürler.
* **🔐 Çilingir Modu (Hash Cracker):** MD5, SHA-256 ve SHA-512 algoritmalarını destekleyen hibrit bir kırma motoru kullanır.
* **🤖 AI Siber Analiz Raporu:** Kırılamayan karmaşık hash yapıları için Llama 3/TinyLlama modelleri üzerinden teknik risk raporları ve güvenlik önerileri sunar.
* **🌍 Coğrafi İstihbarat:** Saldırgan IP adreslerinin fiziksel konumlarını (Ülke/Kod) otomatik olarak sorgular.

## 🛠️ Kurulum ve Çalıştırma

Proje, bağımlılık sorunlarını minimize etmek adına **EXE** olarak paketlenmiştir.

1.  `Releases` kısmından en güncel `JANUS_PANEL.zip` dosyasını indirin.
2.  ZIP dosyasını bir klasöre çıkarın.
3.  `JANUS_PANEL.exe` dosyasını çalıştırın.

> **Önemli:** Programın çalışması için `wordlist.txt` ve `access.log` dosyalarının exe ile aynı dizinde bulunması gerekmektedir.

## 💻 Teknolojiler

* **Dil:** Python 3.12+
* **Kütüphaneler:** Requests, Hashlib, Subprocess, Re, Time,random
* **AI Entegrasyonu:** Ollama API (Llama 3 / TinyLlama)
* **Paketleme:** PyInstaller

## 📸 Ekran Görüntüleri
<img width="752" height="591" alt="waf" src="https://github.com/user-attachments/assets/0b11d4bc-a83a-448f-b5ab-b33a682b3222" />
<img width="752" height="591" alt="waf" src="https://github.com/user-attachments/assets/dde1b33b-160d-44ae-98e7-0cd84c35b7f6" />
<img width="1093" height="591" alt="ekran" src="https://github.com/user-attachments/assets/6368a9eb-8392-48b6-b664-32fa243c9f03" />


| Menü Yapısı | Saldırı Tespiti |
| :--- | :--- |
| ![Janus Menu](https://github.com/mustafaColak0/Janus-Cyber-Shield/raw/main/menu_ss.png) | ![Attack Detect](https://github.com/mustafaColak0/Janus-Cyber-Shield/raw/main/attack_ss.png) |

## ⚠️ Yasal Uyarı
Bu araç tamamen eğitim ve siber güvenlik farkındalığı amacıyla geliştirilmiştir. Yetkisiz sistemlerde kullanılması yasal sorumluluk doğurabilir.
