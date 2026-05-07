#  Janus Cyber Shield v1.0

Janus Cyber Shield, Python tabanlı geliştirilmiş, gerçek zamanlı ağ güvenliği analizi ve gelişmiş hash kırma yeteneklerine sahip bir **Siber Güvenlik Paneli**'dir. Hem savunma (Mavi Takım) hem de saldırı (Kırmızı Takım) konseptlerini tek bir arayüzde birleştirir.

## Temel Özellikler

* **🔍 Canlı Log & Otomatik Savunma:** `access.log` dosyalarını gerçek zamanlı izleyerek `etc/passwd`, `powershell` ve `SQL Injection` gibi saldırı girişimlerini anında tespit eder.
* Honeypot Veritabanı İzleme: Sistem, honeypot.db dosyasını (tuzak veritabanını) canlı olarak dinliyor. Oraya birisi "yanlış kapıyı çalmaya" çalıştığı an (SQL Injection veya yetkisiz erişim denemesi), sistem bunu anlık yakalıyor.
* Log Analizine Dayalı Savunma: `access.log` dosyaları, bu honeypot'a gelen ham trafik kayıtlarıdır. Yani sistem, honeypot'a gelen bu canlı "log akışını" analiz ederek saldırganı deşifre ediyor.
* **🚫 Otomatik Güvenlik Duvarı:** Tespit edilen saldırgan IP adreslerini Windows Firewall (netsh) üzerinden otomatik olarak mühürler.
* **🔐 Çilingir Modu (Hash Cracker):** MD5, SHA-256 ve SHA-512 algoritmalarını destekleyen hibrit bir kırma motoru kullanır.
* **🤖 AI Siber Analiz Raporu:** Kırılamayan karmaşık hash yapıları için Llama 3/TinyLlama modelleri üzerinden teknik risk raporları ve güvenlik önerileri sunar.
* **🌍 Coğrafi İstihbarat:** Saldırgan IP adreslerinin fiziksel konumlarını (Ülke/Kod) otomatik olarak sorgular.

## 🛠️ Kurulum ve Çalıştırma (Windows)

Proje, bağımlılık sorunlarını minimize etmek adına **EXE** olarak paketlenmiştir.

1.  `Releases` kısmından en güncel `JANUS_PANEL.zip` dosyasını indirin.
2.  ZIP dosyasını bir klasöre çıkarın.
3.  `JANUS_PANEL.exe` dosyasını çalıştırın.

> **Önemli:** Programın çalışması için `wordlist.txt` ve `access.log` dosyalarının exe ile aynı dizinde bulunması gerekmektedir.

## 🐧 Linux Kurulum ve Çalıştırma
Janus v2.0, Linux tabanlı sistemlerde (Ubuntu, Debian, Kali, vb.) yerel Python ortamı üzerinden tam performansla çalışır.

1.Gereksinimlerin Kurulması 
Sistemin savunma yapabilmesi için:

```
sudo apt update && sudo apt install python3 python3-pip ufw -y
```

2.Bağımlılıkların Yüklenmesi
Proje klasörüne gidin ve gerekli kütüphaneleri yükleyin:

```
pip3 install requests python-dotenv
```
3.Savunma Sistemini Hazırlama (Önemli)
Janus'un IP engelleme yapabilmesi için Linux güvenlik duvarının aktif olması gerekir:

```
sudo ufw enable
```

4.Janus'u Başlatma
Sistem dosyalarına müdahale ve Firewall kuralı ekleme yetkisi için Janus Linux'ta root yetkisiyle çalıştırılmalıdır:

```
sudo python3 analiz.py
```

## 💻 Teknolojiler

* **Dil:** Python 3.12+
* **Kütüphaneler:** Requests, Hashlib, Subprocess, Re, Time,random
* **AI Entegrasyonu:** Ollama API (Llama 3 / TinyLlama)
* **Paketleme:** PyInstaller

## 📸 Ekran Görüntüleri
<img width="513" height="282" alt="menü" src="https://github.com/user-attachments/assets/d1b89d75-4cc9-4c9d-bed4-c74a10389c84" />
<img width="573" height="162" alt="attack" src="https://github.com/user-attachments/assets/1dc7669b-ddee-4fd5-953f-1ced4d2d168c" />
<img width="1093" height="591" alt="ekran" src="https://github.com/user-attachments/assets/4653c1a0-d81d-4e75-abd3-565223de9276" />
<img width="946" height="186" alt="waf" src="https://github.com/user-attachments/assets/724b48ac-7213-4671-844a-4adb7f777b2e" />
<img width="1102" height="311" alt="hash" src="https://github.com/user-attachments/assets/b8154da9-ac83-45b8-92a0-0b262bd62c34" />

| :--- :--- ------------------------------------------------------------------------------------------------------------- :--- :--- |


## ⚠️ Yasal Uyarı
Bu araç tamamen eğitim ve siber güvenlik farkındalığı amacıyla geliştirilmiştir. Yetkisiz sistemlerde kullanılması yasal sorumluluk doğurabilir.
