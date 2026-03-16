import requests
from colorama import init, Fore
import datetime

init(autoreset=True)

def ip_avla(ip="self"):
    url = f"http://ip-api.com/json/{ip}?fields=status,message,query,country,countryCode,city,isp,org,as,proxy,hosting,mobile,timezone,lat,lon"
    
    try:
        r = requests.get(url, timeout=4)
        r.raise_for_status()
        data = r.json()
        
        if data.get('status') != 'success':
            print(Fore.RED + f"Hata: {data.get('message')}")
            return
        
        # Bayrak emoji
        bayraklar = {'TR': '🇹🇷', 'US': '🇺🇸', 'DE': '🇩🇪', 'GB': '🇬🇧', 'FR': '🇫🇷', 'RU': '🇷🇺'}
        bayrak = bayraklar.get(data.get('countryCode'), '🌍')
        
        print(Fore.GREEN + f"╔═══════ IP Sorgu Sonucu {bayrak} ═══════╗")
        print(Fore.CYAN + f" IP            → {data.get('query')}")
        print(Fore.YELLOW + f" Şehir         → {data.get('city') or 'Bilinmiyor'}")
        print(Fore.YELLOW + f" Ülke          → {data.get('country')} ({data.get('countryCode')}) {bayrak}")
        print(Fore.MAGENTA + f" ISP / Sağlayıcı → {data.get('isp') or 'Gizli'}")
        print(Fore.MAGENTA + f" Organizasyon  → {data.get('org') or 'Yok'}")
        print(Fore.BLUE + f" ASN           → {data.get('as') or 'Bilinmiyor'}")
        print(Fore.BLUE + f" Zaman Dilimi  → {data.get('timezone') or 'Bilinmiyor'}")
        print(Fore.BLUE + f" Bağlantı      → {'Mobil Veri 📱' if data.get('mobile') else 'Sabit Hat 🏠'}")
        
        lat, lon = data.get('lat'), data.get('lon')
        if lat and lon:
            maps = f"https://www.google.com/maps?q={lat},{lon}"
            print(Fore.CYAN + f" Harita        → {maps}")
        
        # VPN tespiti
        vpnler = []
        if data.get('proxy'): vpnler.append("Proxy / VPN işareti tespit edildi")
        if data.get('hosting'): vpnler.append("Hosting veya veri merkezi – VPN olasılığı yüksek")
        
        vpn_list = ["NordVPN", "Mullvad", "Proton", "Cloudflare", "Tor", "Surfshark", "ExpressVPN"]
        org_isp = (data.get('org', '') + data.get('isp', '')).lower()
        
        for v in vpn_list:
            if v.lower() in org_isp:
                vpnler.append(f"Bilinen VPN sağlayıcısı: {v}")
        
        if vpnler:
            print(Fore.RED + "\n⚠ VPN / Proxy / Tor Tespit Edildi ⚠")
            for v in vpnler:
                print(Fore.RED + f" → {v}")
        else:
            print(Fore.GREEN + "\nVPN veya proxy tespit edilmedi")
        
        print(Fore.GREEN + "╚═══════════════════════════════════════════╝")
        
        # Log kaydet
        simdi = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_str = f"[{simdi}] IP: {data.get('query')} | Şehir: {data.get('city')} | Ülke: {data.get('country')} | ISP: {data.get('isp')} | VPN: {'Evet' if vpnler else 'Hayır'}\n"
        
        with open("ip_av_log.txt", "a", encoding="utf-8") as f:
            f.write(log_str)
        
        print(Fore.WHITE + "Sonuç ip_av_log.txt dosyasına kaydedildi.")
        
    except Exception as e:
        print(Fore.RED + f"Bağlantı hatası: {e}")

print(Fore.CYAN + "Ultimate IP Sorgu Aracı 🔍")
ip_gir = input(Fore.WHITE + "IP gir (boş bırak kendi IP’n sorgulansın): ").strip() or "self"
ip_avla(ip_gir)
