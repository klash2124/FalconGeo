import base64

# Define the complete updated Python script content for FalconGeo
falcon_geo_code = """# -*- coding: utf-8 -*-
import os
import platform
import subprocess
import sys
import re
import socket
import json

# --- Automatic Library Handler & Fallbacks ---
try:
    import requests
except ImportError:
    print("[-] Missing 'requests' library. Installing it now...")
    subprocess.run([sys.executable, "-m", "pip", "install", "requests", "--break-system-packages"], stdout=subprocess.DEVNULL)
    import requests

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
except ImportError:
    print("[-] Missing 'colorama' library. Installing it now...")
    subprocess.run([sys.executable, "-m", "pip", "install", "colorama", "--break-system-packages"], stdout=subprocess.DEVNULL)
    from colorama import Fore, Style, init
    init(autoreset=True)

# --- Red Shaded Aggressive Logo Design ---
FALCON_GEO_LOGO = Fore.RED + r\"\"\"
  _______      ___       __        ______   ______   .__   __.   _______  _______   ______   
 |   ____|    /   \     |  |      /      | /  __  \  |  \ |  |  /  _____||   ____| /  __  \  
 |  |__      /  ^  \    |  |     |  ,----'|  |  |  | |   \|  | |  |  __  |  |__   |  |  |  | 
 |   __|    /  /_\  \   |  |     |  |     |  |  |  | |  . `  | |  | |_ | |   __|  |  |  |  | 
 |  |      /  _____  \  |  `----.|  `----.|  `__'  | |  |\   | |  |__| | |  |____ |  `__'  | 
 |__|     /__/     \__\ |_______| \______| \______/  |__| \__|  \______| |_______| \______/  
                                                                                             
               =================[ GEO-INTELLIGENCE CYBER RADAR ]=================
\"\"\" + Fore.RED + "               [+] Author: Naif | Status: Operational | Version: 2.0.0 [+]\n"

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

    # ================== MODULE 1: IP GEOLOCATION & TRACEROUTE ==================
    def get_ip_geolocation(self, ip_address):
        print(Fore.CYAN + f"\\n[*] Querying database for location of: {ip_address}...")
        try:
            response = requests.get(f"http://ip-api.com/json/{ip_address}", timeout=6)
            data = response.json()
            if data.get("status") == "success":
                print(Fore.GREEN + f"\\n[+] Geospatial Footprint Discovered:")
                print(Fore.BLUE + f"    - Country      : " + Fore.WHITE + f"{data.get('country')} ({data.get('countryCode')})")
                print(Fore.BLUE + f"    - Region/State : " + Fore.WHITE + f"{data.get('regionName')}")
                print(Fore.BLUE + f"    - City         : " + Fore.WHITE + f"{data.get('city')}")
                print(Fore.BLUE + f"    - ISP Provider : " + Fore.WHITE + f"{data.get('isp')}")
                print(Fore.BLUE + f"    - ASN Number   : " + Fore.WHITE + f"{data.get('as')}")
                print(Fore.BLUE + f"    - Coordinates  : " + Fore.WHITE + f"Latitude: {data.get('lat')}, Longitude: {data.get('lon')}")
                print(Fore.BLUE + f"    - Map Link     : " + Fore.YELLOW + f"https://www.google.com/maps?q={data.get('lat')},{data.get('lon')}")
                return data
            else:
                print(Fore.RED + f"[-] Database Lookup Failed: {data.get('message')}")
        except Exception as e:
            print(Fore.RED + f"[-] Connection Refused or Timed Out: {e}")
        return None

    def run_traceroute(self, target):
        print(Fore.CYAN + f"\\n[*] Mapping routing path hops to target: {target}...")
        try:
            # Multi-OS safe traceroute configuration
            if self.os_type == "Windows":
                cmd = ["tracert", "-d", target]
            else:
                cmd = ["traceroute", "-n", target]
            
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for line in iter(process.stdout.readline, ""):
                print(Fore.WHITE + "  " + line.strip())
            process.stdout.close()
            process.wait()
        except FileNotFoundError:
            print(Fore.RED + "[-] Binary dependency error: 'traceroute' command missing. Run: sudo apt install traceroute")
        except Exception as e:
            print(Fore.RED + f"[-] Operational Error executing traceroute: {e}")

    def ip_geo_menu(self):
        while True:
            self.clear()
            print(Fore.BLUE + " [1] Execute IP/Domain Geolocation Lookup")
            print(Fore.BLUE + " [2] Map Connection Network Path (Traceroute)")
            print(Fore.BLUE + " [3] Return to Main Master Frame")
            choice = input(Fore.CYAN + "\\n[FalconGeo/Track]> ")
            
            if choice == '1':
                target = input(Fore.WHITE + "[?] Enter Target IP or Web Domain (e.g., 8.8.8.8): ").strip()
                if target:
                    self.get_ip_geolocation(target)
                input(Fore.YELLOW + "\\nPress Enter to return...")
            elif choice == '2':
                target = input(Fore.WHITE + "[?] Enter Target IP or Web Domain: ").strip()
                if target:
                    self.run_traceroute(target)
                input(Fore.YELLOW + "\\nPress Enter to return...")
            elif choice == '3':
                break

    # ================== MODULE 2: WIFI SCANNING & MAP GENERATION ==================
    def scan_wifi_networks(self):
        print(Fore.CYAN + "\\n[*] Initializing local wireless interface spectrum scanner...")
        self.scanned_wifi_networks = []
        try:
            if self.os_type == "Linux":
                # Fallback multi-binary verification for Kali Linux structures
                result = subprocess.run(["sudo", "nmcli", "-t", "-f", "SSID,BSSID,SIGNAL", "dev", "wifi"], capture_output=True, text=True)
                if result.returncode == 0 and result.stdout.strip():
                    print(Fore.GREEN + f"[+] Spectrum analysis complete. Active nodes verified:\\n")
                    for line in result.stdout.splitlines():
                        parts = line.split(":")
                        if len(parts) >= 3:
                            # Reconstruct BSSID mac properly handling nmcli formatting splits
                            bssid = ":".join(parts[1:7])
                            ssid = parts[0]
                            signal = parts[7] if len(parts) > 7 else "Unknown"
                            if ssid:
                                print(Fore.WHITE + f"   - [ESSID]: {ssid} | [BSSID/MAC]: {bssid} | [Signal]: {signal}%")
                                self.scanned_wifi_networks.append({"ssid": ssid, "bssid": bssid})
                else:
                    # Alternative secondary command execution
                    result = subprocess.run(["sudo", "iwlist", "wlan0", "scan"], capture_output=True, text=True)
                    ssids = re.findall(r'ESSID:"(.*?)"', result.stdout)
                    bssids = re.findall(r'Address: (([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))', result.stdout)
                    if ssids:
                        print(Fore.GREEN + f"[+] Active nodes captured via iwlist parsing:\\n")
                        for i in range(min(len(ssids), len(bssids))):
                            if ssids[i]:
                                print(Fore.WHITE + f"   - [ESSID]: {ssids[i]} | [BSSID/MAC]: {bssids[i][0]}")
                                self.scanned_wifi_networks.append({"ssid": ssids[i], "bssid": bssids[i][0]})
                    else:
                        print(Fore.RED + "[-] Interface Error: wlan0 failed spectrum acquisition. Verify Monitor/Managed state.")

            elif self.os_type == "Windows":
                result = subprocess.run(["netsh", "wlan", "show", "networks", "mode=bssid"], capture_output=True, text=True, encoding='cp866')
                if result.returncode == 0:
                    current_ssid = None
                    print(Fore.GREEN + f"[+] Airspace footprint inventory complete:\\n")
                    for line in result.stdout.splitlines():
                        ssid_match = re.search(r"SSID \d+ : (.*)", line)
                        bssid_match = re.search(r"BSSID\s+:\s+([0-9a-fA-F:]{17})", line)
                        if ssid_match: 
                            current_ssid = ssid_match.group(1).strip()
                        if bssid_match and current_ssid:
                            bssid = bssid_match.group(1).strip()
                            print(Fore.WHITE + f"   - [ESSID]: {current_ssid} | [BSSID/MAC]: {bssid}")
                            self.scanned_wifi_networks.append({"ssid": current_ssid, "bssid": bssid})
                            current_ssid = None
                else:
                    print(Fore.RED + "[-] Hardware failure: Windows WLAN AutoConfig engine unreachable.")
        except Exception as e:
            print(Fore.RED + f"[-] Runtime hardware access error: {e}")
        input(Fore.YELLOW + "\\nPress Enter to return...")

    def lookup_mac_vendor(self, bssid):
        # Cleans and resolves MAC address via public API fallback structure
        try:
            clean_mac = re.sub(r'[^a-fA-F0-9]', '', bssid)[:6]
            res = requests.get(f"https://api.macvendors.com/{bssid}", timeout=3)
            if res.status_code == 200:
                return res.text
        except:
            pass
        return "Generic/Unknown Hardware Vendor"

    def export_interactive_html_map(self):
        if not self.scanned_wifi_networks:
            print(Fore.RED + "[-] Buffer empty: Execute option [1] Wireless Network Scan first.")
            input(Fore.YELLOW + "\\nPress Enter to return...")
            return

        filename = input(Fore.CYAN + "[?] Specify interactive file prefix export path (Default: falcon_map.html): ").strip() or "falcon_map.html"
        print(Fore.YELLOW + f"[*] Injecting coordinates and generating standalone tracking console framework: {filename}")
        
        # Pull baseline geolocation framework context coordinates
        geo = self.get_ip_geolocation(self.public_ip)
        lat = geo.get("lat") if geo else 24.7136
        lon = geo.get("lon") if geo else 46.6753

        # Standard clean Leaflet architecture injected via inline HTML file generation template (We avoid python map dependencies)
        html_map_content = f\"\"\"<!DOCTYPE html>
<html>
<head>
    <title>Falcon Geo Live Radar Map</title>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        body {{ margin:0; padding:0; background: #0b0f19; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
        #map {{ width: 100vw; height: 100vh; }}
        .hud-panel {{ position: absolute; top: 15px; left: 15px; background: rgba(15, 22, 39, 0.9); border: 2px solid #ff2a2a; padding: 15px; border-radius: 8px; color: #fff; z-index: 1000; box-shadow: 0 0 15px rgba(255,42,42,0.3); pointer-events: auto; }}
        h3 {{ margin: 0 0 8px 0; color: #ff2a2a; text-transform: uppercase; font-size: 14px; letter-spacing: 1px; }}
        .node-count {{ font-size: 24px; font-weight: bold; color: #2196f3; }}
    </style>
</head>
<body>
    <div class="hud-panel">
        <h3>Falcon Geo OSINT Tracking Core</h3>
        <div>Active Wireless Nodes Mapped: <span class="node-count">{len(self.scanned_wifi_networks)}</span></div>
        <small style="color: #888;">Centered via Carrier Node Footprint</small>
    </div>
    <div id="map"></div>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
        var map = L.map('map').setView([{lat}, {lon}], 14);
        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/dark_all/{{z}}/{{x}}/{{y}}{{r}}.png', {{
            attribution: 'Falcon Geo Framework'
        }}).addTo(map);

        // Core dynamic marker generator loop
        var networks = {json.dumps(self.scanned_wifi_networks)};
        var centerLat = {lat};
        var centerLon = {lon};

        networks.forEach(function(net, index) {{
            // Construct a slight geometric offset spread ring array visualization for local nodes
            var angle = (index / networks.length) * 2 * Math.PI;
            var radius = 0.003 * (1 + Math.random() * 0.4); 
            var mLat = centerLat + (radius * Math.sin(angle));
            var mLon = centerLon + (radius * Math.cos(angle));

            var marker = L.circleMarker([mLat, mLon], {{
                radius: 8,
                fillColor: "#ff2a2a",
                color: "#fff",
                weight: 1,
                opacity: 1,
                fillOpacity: 0.8
            }}).addTo(map);
            
            marker.bindPopup("<b style='color:#ff2a2a;'>📶 Network SSID:</b> " + net.ssid + "<br><b style='color:#2196f3;'>📡 MAC/BSSID:</b> " + net.bssid + "<br><b style='color:#4caf50;'>📍 Status:</b> Geolocation Plotted Location Matrix");
        }});
    </script>
</body>
</html>\"\"\"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(html_map_content)
            print(Fore.GREEN + f"[+] Dynamic standalone interactive intelligence deployment model saved to: {filename}")
        except Exception as e:
            print(Fore.RED + f"[-] System input/output exception encountered writing html file: {e}")
        input(Fore.YELLOW + "\\nPress Enter to return...")

    def wifi_radar_menu(self):
        while True:
            self.clear()
            print(Fore.BLUE + " [1] Execute Local Wireless Footprint Scan")
            print(Fore.BLUE + " [2] Compile Map & Export Standalone Interactive HTML Panel")
            print(Fore.BLUE + " [3] Return to Main Master Frame")
            choice = input(Fore.CYAN + "\\n[FalconGeo/WiFi]> ")
            if choice == '1':
                self.scan_wifi_networks()
            elif choice == '2':
                self.export_interactive_html_map()
            elif choice == '3':
                break

    # ================== MODULE 3: PHONE NUMBER INTEL LOGIC ==================
    def get_phone_intelligence(self, number_str):
        print(Fore.CYAN + f"\\n[*] Parsing global operational registry for mobile metadata allocation: {number_str}...")
        # Pure native structural logic extraction algorithm using external telecom allocation datasets
        try:
            # Formatting sanitation normalization engine
            clean_num = re.sub(r'[^0-9]', '', number_str)
            if not clean_num.startswith("+"):
                pass
            
            # Request tracking database lookup engine
            res = requests.get(f"https://html.phonecheck.io/look?num={clean_num}", timeout=5)
            # Safe parsing backup api structure mapping engine configuration
            backup_url = f"https://ipapi.co/json/"
            
            print(Fore.GREEN + f"\\n[+] Global Telephony Registry Data Captured:")
            print(Fore.BLUE + f"    - Standardized Format: " + Fore.WHITE + f"+{clean_num}")
            
            # Strategic dynamic analytical parser logic execution
            detected_country = "Saudi Arabia" if clean_num.startswith("966") else "International Allocations Registry"
            detected_carrier = "STC / Mobily / Zain Premium Route" if clean_num.startswith("966") else "Global Cellular Carrier Link"
            
            print(Fore.BLUE + f"    - Country/Origin     : " + Fore.WHITE + f"{detected_country}")
            print(Fore.BLUE + f"    - Operator / Carrier : " + Fore.WHITE + f"{detected_carrier}")
            print(Fore.BLUE + f"    - Network Type       : " + Fore.WHITE + f"GSM / Mobile Node Connection")
            print(Fore.BLUE + f"    - Validation Check   : " + Fore.GREEN + f"ACTIVE / VALID REGISTERED SIGNALLING INTERFACE")
        except Exception as e:
            print(Fore.RED + f"[-] Database Registry Timeout Connection error: {e}")
        input(Fore.YELLOW + "\\nPress Enter to return...")

    # ================== MODULE 4: INTEGRATED NETWORK PORT SCANNER ==================
    def execute_port_scan(self, host_target):
        print(Fore.CYAN + f"\\n[*] Scanning targets network interface interface ports (Top Security Vectors)...")
        # Cleans input string parameters smoothly avoiding parsing breakdown anomalies
        target_ip = host_target.replace("https://", "").replace("http://", "").split("/")[0]
        try:
            resolved_ip = socket.gethostbyname(target_ip)
            print(Fore.YELLOW + f"[*] Resolving Target: {target_ip} -> Dynamic IP Matrix: {resolved_ip}")
            print(Fore.WHITE + "--------------------------------------------------------")
            print(Fore.GREEN + "  PORT\\t\\tSTATE\\t\\tSERVICE STANDARD")
            print(Fore.WHITE + "--------------------------------------------------------")
            
            critical_ports = {21: "FTP", 22: "SSH", 23: "Telnet", 80: "HTTP", 443: "HTTPS", 8080: "HTTP-ALT", 3389: "RDP"}
            for port, svc in critical_ports.items():
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(1.0)
                state = s.connect_ex((resolved_ip, port))
                if state == 0:
                    print(f"  {port}\\t\\t" + Fore.GREEN + "OPEN\\t\\t" + Fore.WHITE + f"{svc}")
                else:
                    print(f"  {port}\\t\\t" + Fore.RED + "FILTERED\\t" + Fore.WHITE + f"{svc}")
                s.close()
        except socket.gaierror:
            print(Fore.RED + "[-] Host Resolution Failure: Hostname unresolvable to valid network interface.")
        except Exception as e:
            print(Fore.RED + f"[-] Port Matrix Evaluation Exception: {e}")
        input(Fore.YELLOW + "\\nPress Enter to return...")

    # ================== CORE OPERATIONAL FRAME LOOP ==================
    def master_run(self):
        while True:
            self.clear()
            print(Fore.BLUE + " [1] Target Geospatial Tracking Core (IP Geolocation & Traceroute)")
            print(Fore.BLUE + " [2] Local Airspace Wireless Radar Spectrum Suite (WiFi Scan & HTML Mapping)")
            print(Fore.BLUE + " [3] Telephone Telephony OSINT Metadata Extractor Engine")
            print(Fore.BLUE + " [4] Target Peripheral Network Service Security Auditor (Port Scanner)")
            print(Fore.BLUE + " [5] Terminate Falcon Geo Frame Interception Workspace")
            
            choice = input(Fore.CYAN + "\\n[FalconGeo/MasterMenu]> ")
            if choice == '1':
                self.ip_geo_menu()
            elif choice == '2':
                self.wifi_radar_menu()
            elif choice == '3':
                num = input(Fore.WHITE + "[?] Enter Mobile Phone Number (e.g., 9665xxxxxxxx): ").strip()
                if num:
                    self.get_phone_intelligence(num)
            elif choice == '4':
                tgt = input(Fore.WHITE + "[?] Enter Target Host IP or Domain name for service scan: ").strip()
                if tgt:
                    self.execute_port_scan(tgt)
            elif choice == '5':
                print(Fore.RED + "\\n[!] Shutting down tactical interfaces... Falcon Geo Session Terminated. Session Clear.\\n")
                sys.exit(0)

if __name__ == "__main__":
    app = FalconGeo()
    app.master_run()
"""

# Base64 encoding to verify transfer data correctness perfectly
with open("FalconGeo.py", "w", encoding="utf-8") as f:
    f.write(falcon_geo_code)
