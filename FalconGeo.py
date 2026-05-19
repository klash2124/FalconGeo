import os
import platform
import subprocess
import sys
import re
import socket

# --- فحص وتثبيت المكتبات تلقائياً ---
try:
    import requests
    import simplekml
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    print("[-] Missing libraries. Please run in terminal:")
    print("pip install requests simplekml colorama")
    sys.exit(1)

# --- شعار الأداة ---
FALCON_GEO_LOGO = Fore.RED + r"""
  /\      / \ / /\    / /\ \
 [ FALCON GEO: GEO-INTELLIGENCE ]
 / /  \  / /  \ \
 [ MAPPING & TRACKING ]
 / /    \/ /    \ \
 [ STATUS: ACTIVE ]
 / /      \ \/ /        \ \
 /_/          \_\
""" + Fore.CYAN + "[+] Falcon Geo is LIVE & READY [+]\n[+] الصقر الجغرافي نشط وجاهز"

class FalconGeo:
    def __init__(self):
        self.os_type = platform.system()
        self.is_kali = os.path.exists("/etc/kali-release")
        self.current_hostname = platform.node()
        self.local_ip = self._get_local_ip()
        self.public_ip = self._get_public_ip()
        self.scanned_wifi_networks = []

    def _get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except: return "127.0.0.1"

    def _get_public_ip(self):
        try:
            return requests.get("https://api.ipify.org", timeout=5).text
        except: return "UNKNOWN"

    def clear(self):
        os.system('cls' if self.os_type == 'Windows' else 'clear')
        print(FALCON_GEO_LOGO)
        print(Fore.WHITE + "-" * 45)

    def display_info(self):
        self.clear()
        print(Fore.YELLOW + f"[*] OS: {self.os_type} | Hostname: {self.current_hostname}")
        if self.is_kali:
            print(Fore.YELLOW + "[*] Distribution: Kali Linux")
        print(Fore.YELLOW + f"[*] Local IP: {self.local_ip}")
        print(Fore.YELLOW + f"[*] Public IP: {self.public_ip}")
        print(Fore.WHITE + "-" * 45)

    # ================== 1. وحدة التتبع الجغرافي ==================
    def get_ip_geolocation(self, ip_address):
        print(Fore.CYAN + f"\n[*] Fetching Geolocation for: {ip_address}...")
        try:
            response = requests.get(f"http://ip-api.com/json/{ip_address}")
            data = response.json()
            if data.get("status") == "success":
                print(Fore.GREEN + f"[+] Location Found:")
                print(f"    - Country: {data.get('country')}")
                print(f"    - Region: {data.get('regionName')}")
                print(f"    - City: {data.get('city')}")
                print(f"    - ISP: {data.get('isp')}")
                print(f"    - Lat/Lon: {data.get('lat')}, {data.get('lon')}")
                return data
            else:
                print(Fore.RED + f"[-] Error: {data.get('message')}")
        except Exception as e:
            print(Fore.RED + f"[-] Network Error: {e}")
        return None

    def run_traceroute(self, target):
        print(Fore.CYAN + f"\n[*] Running traceroute to {target}...")
        try:
            cmd = ["tracert", target] if self.os_type == "Windows" else ["traceroute", target]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for line in iter(process.stdout.readline, ""):
                print(Fore.WHITE + line.strip())
            process.stdout.close()
            process.wait()
        except FileNotFoundError:
            print(Fore.RED + "[-] Traceroute command not found. (Install: sudo apt install traceroute)")
        except Exception as e:
            print(Fore.RED + f"[-] Error: {e}")

    def ip_geo_menu(self):
        self.clear()
        print(Fore.BLUE + "1. Get Geolocation for IP/Domain")
        print(Fore.BLUE + "2. Run Traceroute to IP/Domain")
        print(Fore.BLUE + "3. Back")
        choice = input(Fore.CYAN + "\n[FalconGeo/Track]> ")
        
        if choice == '1':
            target = input("[?] Enter IP or Domain: ")
            self.get_ip_geolocation(target)
            input(Fore.YELLOW + "\nPress Enter to continue...")
        elif choice == '2':
            target = input("[?] Enter IP or Domain: ")
            self.run_traceroute(target)
            input(Fore.YELLOW + "\nPress Enter to continue...")

    # ================== 2. وحدة رادار الواي فاي ==================
    def scan_wifi_networks(self):
        print(Fore.CYAN + "\n[*] Scanning for Wi-Fi networks...")
        self.scanned_wifi_networks = []
        try:
            if self.os_type == "Linux":
                result = subprocess.run(["sudo", "iwlist", "wlan0", "scan"], capture_output=True, text=True)
                if result.returncode == 0:
                    print(Fore.GREEN + "[+] Scan Complete. Found networks:")
                    ssids = re.findall(r'ESSID:"(.*?)"', result.stdout)
                    bssids = re.findall(r'Address: (([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))', result.stdout)
                    
                    for i in range(min(len(ssids), len(bssids))):
                        if ssids[i]: # تجنب الشبكات المخفية
                            print(Fore.WHITE + f"    - SSID: {ssids[i]} | BSSID: {bssids[i][0]}")
                            self.scanned_wifi_networks.append({"ssid": ssids[i], "bssid": bssids[i][0], "lat": None, "lon": None})
                else:
                    print(Fore.RED + "[-] Error scanning Wi-Fi. Run as Root or ensure wlan0 is active.")

            elif self.os_type == "Windows":
                result = subprocess.run(["netsh", "wlan", "show", "networks", "mode=bssid"], capture_output=True, text=True, encoding='cp866')
                if result.returncode == 0:
                    current_ssid = None
                    for line in result.stdout.splitlines():
                        ssid_match = re.search(r"SSID \d+ : (.*)", line)
                        bssid_match = re.search(r"BSSID\s+:\s+([0-9a-fA-F:]{17})", line)
                        if ssid_match: 
                            current_ssid = ssid_match.group(1).strip()
                        if bssid_match and current_ssid:
                            bssid = bssid_match.group(1).strip()
                            print(Fore.WHITE + f"    - SSID: {current_ssid} | BSSID: {bssid}")
                            self.scanned_wifi_networks.append({"ssid": current_ssid, "bssid": bssid, "lat": None, "lon": None})
                            current_ssid = None
                else:
                    print(Fore.RED + "[-] Error scanning Wi-Fi on Windows.")
        except Exception as e:
            print(Fore.RED + f"[-] Error: {e}")
        input(Fore.YELLOW + "\nPress Enter to continue...")

    def export_wifi_to_kml(self):
        if not self.scanned_wifi_networks:
            print(Fore.RED + "[-] No Wi-Fi networks scanned. Please run a scan first.")
            input(Fore.YELLOW + "\nPress Enter to continue...")
            return

        filename = input(Fore.CYAN + "[?] Enter filename (e.g., wifi.kml): ") or "wifi_networks.kml"
        print(Fore.YELLOW + f"[*] Exporting {len(self.scanned_wifi_networks)} networks to {filename}...")
        
        kml = simplekml.Kml()
        public_ip_geo = self.get_ip_geolocation(self.public_ip)
        
        # حماية ضد الفشل في جلب الموقع
        fallback_lat = public_ip_geo.get("lat") if public_ip_geo else 0.0
        fallback_lon = public_ip_geo.get("lon") if public_ip_geo else 0.0

        for net in self.scanned_wifi_networks:
            lat = net.get("lat") or fallback_lat
            lon = net.get("lon") or fallback_lon
            
            pnt = kml.newpoint(name=net["ssid"], coords=[(lon, lat)])
            pnt.description = f"SSID: {net['ssid']}\nBSSID: {net['bssid']}"

        try:
            kml.save(filename)
            print(Fore.GREEN + f"[+] Saved successfully to {filename}")
        except Exception as e:
            print(Fore.RED + f"[-] Error saving KML: {e}")
        input(Fore.YELLOW + "\nPress Enter to continue...")

    def wifi_radar_menu(self):
        self.clear()
        print(Fore.BLUE + "1. Scan for Wi-Fi Networks")
        print(Fore.BLUE + "2. Export Scanned Networks to KML (Google Earth)")
        print(Fore.BLUE + "3. Back")
        choice = input(Fore.CYAN + "\n[FalconGeo/WiFi]> ")
        
        if choice == '1': self.scan_wifi_networks()
        elif choice == '2': self.export_wifi_to_kml()

    # ================== القائمة الرئيسية ==================
    def run(self):
        while True:
            self.display_info()
            print(Fore.BLUE + "1. IP Geolocation & Traceroute")
            print(Fore.BLUE + "2. WiFi Radar & KML Mapping")
            print(Fore.BLUE + "3. Exit")
            
            choice = input(Fore.CYAN + "\n[FalconGeo]> ")
            if choice == '1': self.ip_geo_menu()
            elif choice == '2': self.wifi_radar_menu()
            elif choice == '3':
                print(Fore.RED + "[!] Exiting Falcon Geo. Goodbye!")
                sys.exit(0)

if __name__ == "__main__":
    app = FalconGeo()
    app.run()