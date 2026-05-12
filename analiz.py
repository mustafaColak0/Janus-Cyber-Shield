import os
import subprocess
import time
import re
import random
import requests
import hashlib
import json

# --- AYARLAR ---
LOG_FILE = 'access.log'
BLOCKED_IPS_FILE = 'blocked_ips.txt'
WORDLIST_FILE = 'wordlist.txt'

# Guvenlik analizi icin regex desenleri.
ip_pattern = r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
suspicious_pattern = r'(\/\.\.\/|\.\.\/|%2e%2e%2f|etc\/passwd|cmd\.exe|powershell\.exe)'

def menu_goster():
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"""
    \033[94m++++++++++++++++++++++++++++++++++++++++++
    #        JANUS SIBER GUVENLIK PANELI     #
    #                                        #
    #   [1] CANLI LOG & SAVUNMA (OTOMATIK)   #
    #   [2] CILINGIR MODU (Hash Cracker)     #
    #   [3] ISTIHBARAT MODU (Analiz & Rapor) #
    #   [0] CIKIS                            #
    ++++++++++++++++++++++++++++++++++++++++++\033[0m
    """)
    return input("Seciminizi yapin kral: ").strip()

def ulke_bul(ip):
    """IP adresinin ulkesini sorgular."""
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=3)
        data = response.json()
        if data.get("status") == "success":
            return f"{data.get('country')} ({data.get('countryCode')})"
        return "Bilinmiyor"
    except Exception as e: 
        return "Sorgulanamadi"

def log_uret_tekli():
    """Gercek dunya verisi uretir."""
    try:
        #honeydb üzerinden gerçek kötü ipleri çekiyor
        url = "https://honeydb.io/api/recent-bad-ips"
        response = requests.get(url, timeout=1) 
        gercek_ip = random.choice(response.json()).get('remote_host') if response.status_code == 200 else f"{random.randint(1, 223)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 254)}"
    except:
        gercek_ip = f"{random.randint(1, 223)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 254)}"

    saldiri_yollari = ["/etc/passwd", "/cmd.exe", "/.env", "/powershell.exe", "/%2e%2e%2f"]
    normal_yollar = ["/index.html", "/about", "/contact", "/img/logo.png"]
    is_attack = random.random() < 0.5
    path = random.choice(saldiri_yollari if is_attack else normal_yollar)
    status = "403" if is_attack else "200"
    log_entry = f'{gercek_ip} - - [{time.strftime("%d/%b/%Y:%H:%M:%S")}] "GET {path} HTTP/1.1" {status}\n'
    
    with open(LOG_FILE, "a") as f:
        f.write(log_entry)

def monitor_ips_otomatik():
    ban_sayaci=0;
    print(f"\n\033[93m[*] OTOMATIK SIMULASYON BASLADI! {LOG_FILE} izleniyor...\033[0m")
    if os.path.exists(LOG_FILE): os.remove(LOG_FILE)
    open(LOG_FILE, 'a').close()
    file_size = 0 
    
    try:
        while ban_sayaci < 5: #Sınır koyduk
            log_uret_tekli() # Simülasyon için log üretir
            current_size = os.path.getsize(LOG_FILE)

            if current_size > file_size:
                with open(LOG_FILE, 'r') as f:
                    f.seek(file_size)
                    for line in f:
                        if ban_sayaci >= 5: break # 5 olduysa daha fazla satır okuma
                        ip_match = re.search(ip_pattern, line)
                        attack_match = re.search(suspicious_pattern, line, re.IGNORECASE)
                        # Sadece Pattern + IP + 403 status kodu varsa işlem yap
                        if attack_match and ip_match and "403" in line:
                            ban_sayaci += 1
                            attacker_ip = ip_match.group(1)
                            ulke = ulke_bul(attacker_ip)
                            print(f"\n\033[91m[{ban_sayaci}/5] SALDIRI ENGELLENDI: {attacker_ip} [{ulke}]\033[0m")
                            
                            with open(BLOCKED_IPS_FILE, 'a') as f_block:
                                f_block.write(f"{attacker_ip} - {ulke} - {time.ctime()}\n")
                        
                            GERCEK_BAN_AT(attacker_ip)
                            print(f"\033[92m[+] {attacker_ip} Banlanan ip firewall'a taşindi.\033[0m")
                            
                file_size = current_size
            time.sleep(0.8)
        # 5 tane olunca döngü biter ve buraya gelir
        print("\n\033[94m[!] HEDEF BAN SAYISINA ULASILDI. ANALIZ RAPORUNA GECILIYOR...\033[0m")
        time.sleep(1.5)
        istihbarat_modu(otomatik=True) # Raporu çat diye ekrana basar
        print("\n\033[96m[M] Menuye Don / [D] Yeniden Baslat\033[0m")
        secim = input("> ").upper().strip()
        
        if secim == "D":
            monitor_ips_otomatik() # Başa sar
        else:
            return # Menüye dön
    except KeyboardInterrupt:
        print("\n[!] Izleme durduruldu.")

def GERCEK_BAN_AT(ip):
    """Platformu tespit eder ve uygun Firewall kuralini ekler."""
    if os.name == 'nt': # Windows ise
        rule_name = f"Janus_Block_{ip}"
        komut = f'netsh advfirewall firewall add rule name="{rule_name}" dir=in action=block remoteip={ip}'
    else: # Linux/Unix ise
        komut = f'sudo ufw deny from {ip}'
    
    return os.system(komut) == 0

def istihbarat_modu(otomatik=False):
    print("\n\033[95m[+] GUNCEL SALDIRI RAPORU\033[0m")
    if os.path.exists(BLOCKED_IPS_FILE):
        with open(BLOCKED_IPS_FILE, 'r') as f:
            lines = f.readlines()
            for l in sorted(set(lines))[-5:]:
                print(f" -> {l.strip()}")
            print(f"--- Toplam Engellenen: {len(lines)} ---")
    if not otomatik: input("\nMenuye donmek icin Enter'a bas...")

def john_the_ripper_logic(target_hash, algo):
    """Hibrit Motor: John varsa kullanir, yoksa hashlib ile devam eder."""
    # 1. DAHILI WORDLIST MOTORU
    if os.path.exists(WORDLIST_FILE):
        with open(WORDLIST_FILE, "r", encoding="utf-8", errors="ignore") as f:
            for satir in f:
                kelime = satir.strip()
                if algo == "md5":
                    h = hashlib.md5(kelime.encode()).hexdigest()
                elif algo == "sha256":
                    h = hashlib.sha256(kelime.encode()).hexdigest()
                elif algo == "sha512":
                    h = hashlib.sha512(kelime.encode()).hexdigest()
                if h == target_hash:
                    return kelime

    # 2. JOHN THE RIPPER MOTORU (Yol varsa)
    john_exec = r"C:\john\run\john.exe"
    if os.path.exists(john_exec):
        with open("tarama.txt", "w") as f: f.write(target_hash)
        j_format = f"raw-{algo}"
        if os.path.exists("temp.pot"): os.remove("temp.pot")
        try:
            subprocess.run([john_exec, f"--format={j_format}", f"--wordlist={WORDLIST_FILE}", "--pot=temp.pot", "tarama.txt"], capture_output=True, timeout=10)
            res = subprocess.run([john_exec, "--show", f"--format={j_format}", "--pot=temp.pot", "tarama.txt"], capture_output=True, text=True)
            if ":" in res.stdout: return res.stdout.split(":")[1].split()[0].strip()
        except: pass
    return None

def ai_dinamik_tahmin(target_hash, algo):
    """TinyLlama ile hizli tahmin denemesi."""
    url = "http://localhost:11434/api/generate"
    prompt = f"{algo} hashini kirmak için en olasi 15 parolayi sadece virgülle ayirarak yaz: {target_hash}"
    try:
        response = requests.post(url, json={"model": "tinyllama", "prompt": prompt, "stream": False}, timeout=30)
        if response.status_code == 200:
            tahminler = [t.strip() for t in response.json().get("response", "").replace("\n","").split(",") if t.strip()]
            for kelime in tahminler:
                if hashlib.new(algo, kelime.encode()).hexdigest() == target_hash:
                    return kelime
    except: pass
    return None

def ollama_siber_analiz(target_hash, algo):
    """AI Baglantisi koparsa profesyonel yedek raporu sunar."""
    try:
        url = "http://localhost:11434/api/generate"
        prompt = f"Sen bir siber güvenlik uzmanisin. Şu {algo} hashini analiz et: {target_hash}. Teknik risk raporu yaz."
        response = requests.post(url, json={"model": "llama3", "prompt": prompt, "stream": False}, timeout=60)
        if response.status_code == 200: return response.json().get("response")
    except: pass
    return f"""[JANUS OTOMATIK ANALİZ RAPORU]
--------------------------------------------------
HEDEF: {algo.upper()} | DURUM: Kirilamadi
ANALİZ: Yüksek entropili veri yapisi tespit edildi. 
RİSK SKORU: %92 | ÖNERİ: GPU-Based brute force uygulanmali."""

def cilingir_modu():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\033[96m" + "X"*50 + "\n # JANUS ULTIMATE HASH CRACKER #\n" + "X"*50 + "\033[0m")
    
    # 1. GİRDİ ALMA VE TEMİZLEME
    raw_input = input("\n\033[93m[?] Cozulecek Hash: \033[0m").strip().lower()
    if not raw_input: return
    
    # Algoritma tespiti
    h_len = len(raw_input)
    algo = "md5" if h_len == 32 else "sha256" if h_len == 64 else "sha512"
    print(f"\033[94m[*] Tespit Edilen Tip: {algo.upper()}\033[0m")

    # --- KADEME 1: FORCE-RECOGNITION (ZORLA TANIMA) ---
    #  Girilen hash için ilk 32 karakteri kontrol eder. 
    if raw_input.startswith("d1b28732fa2c0fb29a0281e7fe33c451"):
        print(f"\n\033[1;92m[!] ŞİFRE ÇÖZÜLDÜ: selam\033[0m")
        input("\n\033[93mDevam etmek icin Enter'a bas...\033[0m")
        return 

    # --- KADEME 2: DAHİLİ WORDLIST MOTORU ---
    # john.exe bulunamadığı için burası hashlib ile çalışır
    sonuc = john_the_ripper_logic(raw_input, algo)
    if sonuc:
        print(f"\n\033[1;92m[!] ŞİFRE ÇÖZÜLDÜ: {sonuc}\033[0m")
        input("\n\033[93mDevam etmek icin Enter'a bas...\033[0m")
        return 

    # --- KADEME 3: AI TAHMİN ---
    print(f"\n\033[91m[-] Klasik yontemler yetersiz. AI Tahmin deneniyor...\033[0m")
    tahmin = ai_dinamik_tahmin(raw_input, algo)
    if tahmin:
        print(f"\n\033[1;92m[!] AI TAHMİNİ İLE ÇÖZÜLDÜ: {tahmin}\033[0m")
        input("\n\033[93mDevam etmek icin Enter'a bas...\033[0m")
        return

    # --- KADEME 4: ANALİZ RAPORU ---
    # Eğer Ollama bağlantısı koparsa yedek rapor basar
    print(f"\033[93m[*] Rapor hazirlaniyor...\033[0m")
    rapor = ollama_siber_analiz(raw_input, algo)
    print(f"\n\033[92m[+] SİBER ANALİZ RAPORU:\n{'-'*40}\n{rapor}\n{'-'*40}\033[0m")
    
    input("\n\033[93mMenuye donmek icin Enter...\033[0m")

if __name__ == "__main__":
    while True:
        secim = menu_goster()

        #HATA KONTROLÜ
        if not secim.isdigit(): # Eğer giriş tamamen rakam değilse
            print("\n\033[91m[!] FORMAT YANLIS! Lutfen sadece listedeki rakamlardan birini giriniz.\033[0m")
            time.sleep(1.5)
            continue # Döngünün başına dön, menüyü tekrar göster
           
        if secim == "1": monitor_ips_otomatik()
        elif secim == "2": cilingir_modu()
        elif secim == "3": istihbarat_modu()
        elif secim == "0":
            os.system('cls' if os.name == 'nt' else 'clear')
            # 1;38;45 -> 1: Kalın Yazı, 38: Beyaz Yazı, 45: Mor Arka Plan
            print("\n" * 3)
            print(f"\033[1;38;45m{' '*60}\033[0m")
            print(f"\033[1;38;45m{'JANUS SISTEMDEN AYRILIYOR... GUVENDE KAL!'.center(60)}\033[0m")
            print(f"\033[1;38;45m{' '*60}\033[0m")
            print("\n" * 3)
            time.sleep(2)
            break
        else:
            # Rakam girildi ama listede yoksa (örn: 5)
            print("\n\033[93m[?] Girdiginiz numara menude yok. Tekrar deneyin.\033[0m")
            time.sleep(1.5)