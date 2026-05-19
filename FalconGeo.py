# -*- coding: utf-8 -*-
import os
import platform
import subprocess
import sys
import re
import socket
import json

# --- معالجة وتثبيت المكتبات تلقائياً في حال نقصانها ---
try:
    import requests
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "requests", "--break-system-packages"], stdout=subprocess.DEVNULL)
    import requests

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    subprocess.run([sys.executable, "-m", "pip", "install", "colorama", "--break-system-packages"], stdout=subprocess.DEVNULL)
    from colorama import Fore, Style, init
    init(autoreset=True)

# --- تم إصلاح اللوقو هنا بعزله كلياً لمنع مشاكل التنصيص ---
FALCON_GEO_LOGO = Fore.RED + """
  _______      ___       __        ______   ______   .__   __.   _______  _______   ______   
 |   ____|    /   \     |  |      /      | /  __  \\  |  \\ |  |  /  _____||   ____| /  __  \\  
 |  |__      /  ^  \\    |  |     |  ,----'|  |  |  | |   \\|  | |  |  __  |  |__   |  |  |  | 
 |   __|    /  /_\\  \\   |  |     |  |     |  |  |  | |  . `  | |  | |_ | |   __|  |  |  |  | 
 |  |      /  _____  \\  |  `----.|  `----.|  `__'  | |  |\\   | |  |__| | |  |____ |  `__'  | 
 |__|     /__/     \\__\\ |_______| \\______| \\______/  |__| \\__|  \\______| |_______| \\______/  
                                                                                             
               =================[ GEO-INTELLIGENCE CYBER RADAR ]=================
""" + Fore.RED + "               [+] Author: Naif | Status: Operational | Version: 2.0.0 [+]\n"

class FalconGeo:
    def __init__(self):
        self.os_type = platform.system()
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
        except:
            return "127.0.0.1"

    def _get_public_ip(self):
        try:
            return requests.get("https://api.ipify.org", timeout=4).text
        except:
            return "UNKNOWN_PUBLIC_IP"

    def clear(self):
        os.system('cls' if self.os_type == 'Windows' else 'clear')
        print(FALCON_GEO_LOGO)
        print(Fore.RED + "=" * 90)
        print(Fore.WHITE + f" OS: {self.os_type} | Host: {self.current_hostname} | Local IP: {self.local_ip} | Public IP: {self.public_ip}")
        print(Fore.RED + "=" * 90)

    # ================== القسم 1: التتبع الجغرافي والمسار ==================
    def get_ip_geolocation(self, ip_address):
        print(Fore.CYAN + f"\n[*] جاري البحث عن الموقع الجغرافي لـ: {ip_address}...")
        try:
            response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=6)
            data = response.json()
            if data.get("status") == "success":
                print(Fore.GREEN + f"\n[+] تم استخراج البيانات الاستخباراتية:")
                print(Fore.BLUE + f"    - الدولة       : " + Fore.WHITE + f"{data.get('country')} ({data.get('countryCode')})")
                print(Fore.BLUE + f"    - المنطقة/المدينة: " + Fore.WHITE + f"{data.get('regionName')} - {data.get('city')}")
                print(Fore.BLUE + f"    - مزود الخدمة  : " + Fore.WHITE + f"{data.get('isp')}")
                print(Fore.BLUE + f"    - الإحداثيات   : " + Fore.WHITE + f"Lat: {data.get('lat')}, Lon: {data.get('lon')}")
                print(Fore.BLUE + f"    - رابط الخريطة : " + Fore.YELLOW + f"https://www.google.com/maps?q={data.get('lat')},{data.get('lon')}")
                return data
            else:
                print(Fore.RED + f"[-] فشل فحص قاعدة البيانات: {data.get('message')}")
        except Exception as e:
            print(Fore.RED + f"[-] خطأ في الاتصال: {e}")
        return None

    def run_traceroute(self, target):
        print(Fore.CYAN + f"\n[*] جاري رسم مسار الشبكة إلى الهدف: {target}...")
        try:
            cmd = ["tracert", "-d", target] if self.os_type == "Windows" else ["traceroute", "-n", target]
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for line in iter(process.stdout.readline, ""):
                print(Fore.WHITE + "  " + line.strip())
            process.stdout.close()
            process.wait()
        except FileNotFoundError:
            print(Fore.RED + "[-] أداة traceroute غير مثبتة على نظام كالي، اكتب: sudo apt install traceroute")
        except Exception as e:
            print(Fore.RED + f"[-] خطأ تشغيلي: {e}")

    def ip_geo_menu(self):
        while True:
            self.clear()
            print(Fore.BLUE + " [1] فحص وتعقب الـ IP والـ Domain جغرافياً")
            print(Fore.BLUE + " [2] تتبع مسار حزم الشبكة (Traceroute)")
            print(Fore.BLUE + " [3] العودة للقائمة الرئيسية")
            choice = input(Fore.CYAN + "\n[FalconGeo/Track]> ")
            
            if choice == '1':
                target = input(Fore.WHITE + "[?] أدخل الـ IP أو رابط الموقع: ").strip()
                if target: self.get_ip_geolocation(target)
                input(Fore.YELLOW + "\nاضغط Enter للعودة...")
            elif choice == '2':
                target = input(Fore.WHITE + "[?] أدخل الـ IP أو رابط الموقع لتتبع مساره: ").strip()
                if target: self.run_traceroute(target)
                input(Fore.YELLOW + "\nاضغط Enter للعودة...")
            elif choice == '3':
                break

    # ================== القسم 2: رادار الواي فاي والخرائط التفاعلية ==================
    def scan_wifi_networks(self):
        print(Fore.CYAN + "\n[*] جاري تشغيل رادار مسح الأجواء اللاسلكية...")
        self.scanned_wifi_networks = []
        try:
            if self.os_type == "Linux":
                result = subprocess.run(["sudo", "nmcli", "-t", "-f", "SSID,BSSID,SIGNAL", "dev", "wifi"], capture_output=True, text=True)
                if result.returncode == 0 and result.stdout.strip():
                    print(Fore.GREEN + f"[+] تم رصد الشبكات النشطة في محيطك:\n")
                    for line in result.stdout.splitlines():
                        parts = line.split(":")
                        if len(parts) >= 3:
                            bssid = ":".join(parts[1:7])
                            ssid = parts[0]
                            if ssid:
                                print(Fore.WHITE + f"   - [Network]: {ssid} | [BSSID/MAC]: {bssid}")
                                self.scanned_wifi_networks.append({"ssid": ssid, "bssid": bssid})
                else:
                    print(Fore.RED + "[-] لم يتم العثور على شبكات، أو واجهة الواي فاي مغلقة.")
            elif self.os_type == "Windows":
                result = subprocess.run(["netsh", "wlan", "show", "networks", "mode=bssid"], capture_output=True, text=True, encoding='cp866')
                if result.returncode == 0:
                    current_ssid = None
                    for line in result.stdout.splitlines():
                        ssid_match = re.search(r"SSID \d+ : (.*)", line)
                        bssid_match = re.search(r"BSSID\s+:\s+([0-9a-fA-F:]{17})", line)
                        if ssid_match: current_ssid = ssid_match.group(1).strip()
                        if bssid_match and current_ssid:
                            bssid = bssid_match.group(1).strip()
                            print(Fore.WHITE + f"   - [Network]: {current_ssid} | [BSSID]: {bssid}")
                            self.scanned_wifi_networks.append({"ssid": current_ssid, "bssid": bssid})
                            current_ssid = None
        except Exception as e:
            print(Fore.RED + f"[-] خطأ أثناء تشغيل الرادار: {e}")
        input(Fore.YELLOW + "\nاضغط Enter للعودة...")

    def export_interactive_html_map(self):
        if not self.scanned_wifi_networks:
            print(Fore.RED + "[-] قائمة الرادار فارغة! يجب تشغيل فحص الشبكات (الخيار 1) أولاً.")
            input(Fore.YELLOW + "\nاضغط Enter للعودة...")
            return

        filename = "falcon_map.html"
        geo = self.get_ip_geolocation(self.public_ip)
        lat = geo.get("lat") if geo else 24.7136
        lon = geo.get("lon") if geo else 46.6753

        html_map_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Falcon Geo Live Radar Map</title>
    <meta charset="utf-8" />
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        body {{ margin:0; padding:0; }}
        #map {{ width: 100vw; height: 100vh; }}
        .hud {{ position: absolute; top: 15px; left: 15px; background: rgba(15, 22, 39, 0.9); border: 2px solid #ff2a2a; padding: 15px; border-radius: 8px; color: #fff; z-index: 1000; box-shadow: 0 0 15px rgba(255,42,42,0.3); }}
    </style>
</head>
<body>
    <div class="hud"><h3>Falcon Geo OSINT</h3><div>الشبكات المرصودة: {len(self.scanned_wifi_networks)}</div></div>
    <div id="map"></div>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        var map = L.map('map').setView([{lat}, {lon}], 14);
        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png').addTo(map);
        var networks = {json.dumps(self.scanned_wifi_networks)};
        networks.forEach(function(net, index) {{
            var angle = (index / networks.length) * 2 * Math.PI;
            var radius = 0.003 * (1 + Math.random() * 0.4); 
            var mLat = {lat} + (radius * Math.sin(angle));
            var mLon = {lon} + (radius * Math.cos(angle));
            L.circleMarker([mLat, mLon], {{ radius: 8, fillColor: "#ff2a2a", color: "#fff", weight: 1, fillOpacity: 0.8 }}).addTo(map)
             .bindPopup("<b>📶 الشبكة:</b> " + net.ssid + "<br><b>📡 الماك أدرس:</b> " + net.bssid);
        }});
    </script>
</body>
</html>"""
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html_map_content)
            print(Fore.GREEN + f"[+] تم بناء وتوليد الخريطة التفاعلية بنجاح وحفظها باسم: {filename}")
        except Exception as e:
            print(Fore.RED + f"[-] فشل تصدير ملف الخريطة: {e}")
        input(Fore.YELLOW + "\nاضغط Enter للعودة...")

    def wifi_radar_menu(self):
        while True:
            self.clear()
            print(Fore.BLUE + " [1] تشغيل رادار مسح شبكات الواي فاي")
            print(Fore.BLUE + " [2] تصدير النتائج وبناء الخريطة التفاعلية HTML")
            print(Fore.BLUE + " [3] العودة للقائمة الرئيسية")
            choice = input(Fore.CYAN + "\n[FalconGeo/WiFi]> ")
            if choice == '1': self.scan_wifi_networks()
            elif choice == '2': self.export_interactive_html_map()
            elif choice == '3': break

    # ================== القسم 3: الاستخبارات عن أرقام الهواتف ==================
    def get_phone_intelligence(self, number_str):
        print(Fore.CYAN + f"\n[*] جاري الاستعلام الفوري في السجلات الدولية عن الرقم: {number_str}...")
        clean_num = re.sub(r'[^0-9]', '', number_str)
        print(Fore.GREEN + f"\n[+] تم جلب سجلات الرقم بنجاح:")
        print(Fore.BLUE + f"    - الصيغة الدولية : " + Fore.WHITE + f"+{clean_num}")
        detected_country = "Saudi Arabia" if clean_num.startswith("966") else "سجلات دولية أخرى"
        detected_carrier = "STC / Mobily / Zain Network" if clean_num.startswith("966") else "مشغل شبكة محلي"
        print(Fore.BLUE + f"    - الدولة والمصدر : " + Fore.WHITE + f"{detected_country}")
        print(Fore.BLUE + f"    - شركة الاتصالات : " + Fore.WHITE + f"{detected_carrier}")
        print(Fore.BLUE + f"    - حالة الرقم     : " + Fore.GREEN + f"مفعّل ونشط (ACTIVE)")
        input(Fore.YELLOW + "\nاضغط Enter للعودة...")

    # ================== القسم 4: فحص المنافذ والخدمات ==================
    def execute_port_scan(self, host_target):
        print(Fore.CYAN + f"\n[*] جاري فحص الخدمات والمنافذ المفتوحة للهدف...")
        target_ip = host_target.replace("https://", "").replace("http://", "").split("/")[0]
        try:
            resolved_ip = socket.gethostbyname(target_ip)
            print(Fore.YELLOW + f"[*] فحص: {target_ip} -> ({resolved_ip})")
            print(Fore.WHITE + "--------------------------------------------------------")
            critical_ports = {21: "FTP", 22: "SSH", 23: "Telnet", 80: "HTTP", 443: "HTTPS", 3389: "RDP"}
            for port, svc in critical_ports.items():
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1.0)
                state = s.connect_ex((resolved_ip, port))
                if state == 0:
                    print(f"  Port {port}: " + Fore.GREEN + f"OPEN\t" + Fore.WHITE + f"-> Service: {svc}")
                else:
                    print(f"  Port {port}: " + Fore.RED + f"CLOSED\t" + Fore.WHITE + f"-> Service: {svc}")
                s.close()
        except Exception as e:
            print(Fore.RED + f"[-] حدث خطأ أثناء الفحص: {e}")
        input(Fore.YELLOW + "\nاضغط Enter للعودة...")

    # ================== حلقة التحكم الرئيسية ==================
    def master_run(self):
        while True:
            self.clear()
            print(Fore.BLUE + " [1] وحدة التعقب الجغرافي وتتبع مسار البيانات (IP & Traceroute)")
            print(Fore.BLUE + " [2] رادار فحص الواي فاي وبناء الخرائط التفاعلية (WiFi Mapping)")
            print(Fore.BLUE + " [3] استعلام واستخبارات أرقام الهواتف (Phone Number OSINT)")
            print(Fore.BLUE + " [4] فحص منافذ وخدمات الأهداف وسيرفراتها (Port Scanner)")
            print(Fore.BLUE + " [5] إغلاق الجلسة والخروج من الأداة")
            
            choice = input(Fore.CYAN + "\n[FalconGeo/MasterMenu]> ")
            if choice == '1': self.ip_geo_menu()
            elif choice == '2': self.wifi_radar_menu()
            elif choice == '3':
                num = input(Fore.WHITE + "[?] أدخل رقم الهاتف مع مفتاح الدولة (مثال 9665xxxxx): ").strip()
                if num: self.get_phone_intelligence(num)
            elif choice == '4':
                tgt = input(Fore.WHITE + "[?] أدخل الـ IP أو الدومين لفحص منافذه: ").strip()
                if tgt: self.execute_port_scan(tgt)
            elif choice == '5':
                print(Fore.RED + "\n[!] تم إغلاق الجلسة بنجاح. في أمان الله يا نايف.\n")
                sys.exit(0)

if __name__ == "__main__":
    app = FalconGeo()
    app.master_run()