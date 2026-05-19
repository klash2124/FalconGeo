import os
import platform
import subprocess
import sys
import time
import re
import requests
import socket
import simplekml

# --- Falcon Geo ASCII Logo ---
FALCON_GEO_LOGO = r"""

  /\\      / \\
 / /\\    / /\\ \\
[ FALCON GEO: GEO-INTELLIGENCE ]
/ /  \\  / /  \\ \\
[ MAPPING & TRACKING ]
/ /    \\/ /    \\ \\
[ STATUS: ACTIVE ]
/ /      \\ \\
/ /        \\ \\
/_/          \\_\\
\ \        / /
 \ \      / /
  \ \    / /
   \ \  / /
    \ \/ /
     \/ /

[+] Falcon Geo is LIVE & READY [+] الصقر الجغرافي نشط وجاهز
"""

class FalconGeo:
    def __init__(self):
        self.os_type = platform.system()
        self.is_kali = self._check_kali()
        self.current_hostname = platform.node()
        self.local_ip = self._get_local_ip()
        self.public_ip = self._get_public_ip()
        self.scanned_wifi_networks = [] # To store scanned networks for KML export

    def _check_kali(self):
        return os.path.exists("/etc/kali-release")

    def _get_local_ip(self):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "UNKNOWN_LOCAL_IP"

    def _get_public_ip(self):
        try:
            return requests.get("https://api.ipify.org").text
        except Exception:
            return "UNKNOWN_PUBLIC_IP"

    def display_info(self):
        print(FALCON_GEO_LOGO)
        print(f"\n[+] Operating System: {self.os_type}")
        if self.is_kali:
            print("[+] Distribution: Kali Linux")
        print(f"[+] Current Hostname: {self.current_hostname}")
        print(f"[+] Current Local IP Address: {self.local_ip}")
        print(f"[+] Current Public IP Address: {self.public_ip}")
        print("\n[+] Initializing Geo-Intelligence Module...")

    def get_ip_geolocation(self, ip_address):
        try:
            response = requests.get(f"http://ip-api.com/json/{ip_address}")
            data = response.json()
            if data["status"] == "success":
                print(f"\n[+] Geolocation for {ip_address}:")
                print(f"    Country: {data.get("country")}")
                print(f"    Region: {data.get("regionName")}")
                print(f"    City: {data.get("city")}")
                print(f"    ISP: {data.get("isp")}")
                print(f"    Latitude: {data.get("lat")}, Longitude: {data.get("lon")}")
                return data
            else:
                print(f"[-] Could not get geolocation for {ip_address}: {data.get("message")}")
        except Exception as e:
            print(f"[-] Error getting geolocation for {ip_address}: {e}")
        return None

    def run_traceroute(self, target):
        print(f"\n[+] Running traceroute to {target}...")
        try:
            if self.os_type == "Linux":
                command = ["traceroute", target]
            elif self.os_type == "Windows":
                command = ["tracert", target]
            else:
                print("[-] Traceroute not supported on this OS.")
                return

            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            for line in iter(process.stdout.readline, ""):
                print(line.strip())
            process.stdout.close()
            process.wait()

            if process.returncode != 0:
                print(f"[-] Traceroute failed with error: {process.stderr.read().strip()}")

        except FileNotFoundError:
            print(f"[-] Error: Traceroute command not found. Please install it (e.g., sudo apt install traceroute on Linux).")
        except Exception as e:
            print(f"[-] Error running traceroute: {e}")

    def ip_geolocation_and_traceroute_menu(self):
        while True:
            print("\n--- Falcon Geo: IP & Traceroute Module ---")
            print("1. Get Geolocation for an IP/Domain")
            print("2. Run Traceroute to an IP/Domain")
            print("3. Back to Main Menu")

            choice = input("Enter your choice: ")

            if choice == \'1\':
                target = input("Enter IP address or domain: ")
                self.get_ip_geolocation(target)
            elif choice == \'2\':
                target = input("Enter IP address or domain: ")
                self.run_traceroute(target)
            elif choice == \'3\':
                break
            else:
                print("[-] Invalid choice. Please try again.")

    def scan_wifi_networks(self):
        print("\n[+] Scanning for Wi-Fi networks...")
        self.scanned_wifi_networks = [] # Clear previous scan results
        try:
            if self.os_type == "Linux":
                result = subprocess.run(["nmcli", "device", "wifi", "list", "--rescan", "yes"], capture_output=True, text=True)
                if result.returncode == 0:
                    print(result.stdout)
                    # Parse nmcli output for KML export
                    lines = result.stdout.splitlines()
                    if len(lines) > 1: # Skip header
                        for line in lines[1:]:
                            parts = line.split()
                            if len(parts) >= 8:
                                ssid = parts[0]
                                bssid = parts[1]
                                # Attempt to get geolocation for BSSID (requires external service/database)
                                # For now, we'll use a placeholder or public IP's location
                                self.scanned_wifi_networks.append({"ssid": ssid, "bssid": bssid, "lat": None, "lon": None})
                else:
                    print("[-] Error running nmcli. Trying iwlist...")
                    result = subprocess.run(["sudo", "iwlist", "wlan0", "scan"], capture_output=True, text=True)
                    if result.returncode == 0:
                        print(result.stdout)
                        # Parse iwlist output for KML export (more complex)
                        # Placeholder for parsing
                    else:
                        print(f"[-] Error scanning Wi-Fi on Linux: {result.stderr}")
                        print("[*] Ensure your wireless adapter is in monitor mode or try \'sudo apt install network-manager\' or \'sudo apt install wireless-tools\'.")

            elif self.os_type == "Windows":
                result = subprocess.run(["netsh", "wlan", "show", "networks", "mode=bssid"], capture_output=True, text=True, encoding=\'cp866\')
                if result.returncode == 0:
                    print(result.stdout)
                    # Parse netsh output for KML export
                    current_ssid = None
                    for line in result.stdout.splitlines():
                        ssid_match = re.search(r"SSID \d+ : (.*)", line)
                        bssid_match = re.search(r"BSSID\s+:\s+([0-9a-fA-F:]{17})", line)
                        if ssid_match: current_ssid = ssid_match.group(1).strip()
                        if bssid_match and current_ssid:
                            bssid = bssid_match.group(1).strip()
                            self.scanned_wifi_networks.append({"ssid": current_ssid, "bssid": bssid, "lat": None, "lon": None})
                            current_ssid = None # Reset for next network
                else:
                    print(f"[-] Error scanning Wi-Fi on Windows: {result.stderr}")
                    print("[*] Ensure WLAN AutoConfig service is running.")
            else:
                print("[-] Wi-Fi scanning not supported on this OS.")
        except FileNotFoundError:
            print("[-] Error: Required command not found. (nmcli/iwlist on Linux, netsh on Windows).")
        except Exception as e:
            print(f"[-] Error during Wi-Fi scan: {e}")

    def export_wifi_to_kml(self, filename="wifi_networks.kml"):
        if not self.scanned_wifi_networks:
            print("[-] No Wi-Fi networks scanned yet. Please run a scan first.")
            return

        print(f"[+] Exporting {len(self.scanned_wifi_networks)} Wi-Fi networks to {filename}...")
        kml = simplekml.Kml()

        # Get current public IP's location as a fallback for networks without specific BSSID geolocation
        public_ip_geo = self.get_ip_geolocation(self.public_ip)
        fallback_lat = public_ip_geo.get("lat") if public_ip_geo else 0
        fallback_lon = public_ip_geo.get("lon") if public_ip_geo else 0

        for network in self.scanned_wifi_networks:
            # For a more accurate BSSID geolocation, an external API like WiGLE would be needed.
            # For this example, we'll use the public IP's location as a placeholder if no specific geo is available.
            lat = network.get("lat") or fallback_lat
            lon = network.get("lon") or fallback_lon

            if lat and lon:
                pnt = kml.newpoint(name=network["ssid"], coords=[(lon, lat)])
                pnt.description = f"SSID: {network['ssid']}\nBSSID: {network['bssid']}"
            else:
                print(f"[-] Could not get location for network: {network['ssid']}. Skipping KML entry.")

        try:
            kml.save(filename)
            print(f"[+] KML file saved successfully to {filename}")
        except Exception as e:
            print(f"[-] Error saving KML file: {e}")

    def wifi_radar_menu(self):
        while True:
            print("\n--- Falcon Geo: WiFi Radar & Mapping Module ---")
            print("1. Scan for Wi-Fi Networks")
            print("2. Export Scanned Networks to KML")
            print("3. Back to Main Menu")

            choice = input("Enter your choice: ")

            if choice == \'1\':
                self.scan_wifi_networks()
            elif choice == \'2\':
                filename = input("Enter KML filename (e.g., wifi_map.kml): ")
                self.export_wifi_to_kml(filename if filename else "wifi_networks.kml")
            elif choice == \'3\':
                break
            else:
                print("[-] Invalid choice. Please try again.")

    def main_menu(self):
        while True:
            print("\n--- Falcon Geo Main Menu ---")
            print("1. Display System Info")
            print("2. IP Geolocation & Traceroute")
            print("3. WiFi Radar & Mapping")
            print("4. Exit")

            choice = input("Enter your choice: ")

            if choice == \'1\':
                self.display_info()
            elif choice == \'2\':
                self.ip_geolocation_and_traceroute_menu()
            elif choice == \'3\':
                self.wifi_radar_menu()
            elif choice == \'4\':
                print("[+] Exiting Falcon Geo. Stay geographically aware!")
                sys.exit(0)
            else:
                print("[-] Invalid choice. Please try again.")

    def run(self):
        self.display_info()
        self.main_menu()

if __name__ == "__main__":
    falcon_geo = FalconGeo()
    falcon_geo.run()
