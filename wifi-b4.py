#!/usr/bin/env python3
"""
WiFi Security Analysis Tool - Educational Purpose Only
Developer: babar (Instagram: @the_babarrrr)
Tool: wifi-b4
"""

import sys
import os
import subprocess
import time
import socket
import threading
from datetime import datetime
import re

# Third-party imports
try:
    import pyfiglet
    from termcolor import colored, cprint
    from colorama import init, Fore, Back, Style
    import scapy.all as scapy
    import nmap
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

# Initialize colorama
init(autoreset=True)

class WiFiSecurityTool:
    """Educational WiFi Security Analysis Tool"""
    
    def __init__(self):
        self.developer = "babar"
        self.instagram = "@the_babarrrr"
        self.tool_name = "wifi-b4"
        self.version = "1.0"
        self.nm = nmap.PortScanner()
        
    def check_root(self):
        """Check if running as root (required for monitor mode)"""
        return os.geteuid() == 0
    
    def print_banner(self):
        """Display tool banner"""
        os.system('clear' if os.name == 'posix' else 'cls')
        
        banner = pyfiglet.figlet_format("wifi-b4", font="slant")
        print(colored(banner, 'cyan'))
        
        print(colored("=" * 60, 'yellow'))
        print(colored(f"Developer: {self.developer}", 'green'))
        print(colored(f"Instagram: {self.instagram}", 'green'))
        print(colored(f"Version: {self.version}", 'green'))
        print(colored("Purpose: Educational WiFi Security Analysis", 'red'))
        print(colored("=" * 60, 'yellow'))
        print(colored("⚠️  USE ONLY ON NETWORKS YOU OWN OR HAVE PERMISSION ⚠️", 'red'))
        print()
    
    def show_menu(self):
        """Display main menu"""
        menu_options = {
            '1': 'Scan WiFi Networks',
            '2': 'Network Information',
            '3': 'Connected Devices Scan',
            '4': 'Deauthentication Attack Test (Educational)',
            '5': 'WiFi Adapter Information',
            '6': 'Check Network Security',
            '7': 'Monitor Network Traffic',
            '8': 'WiFi Signal Strength',
            '9': 'About',
            '0': 'Exit'
        }
        
        print(colored("\n=== MAIN MENU ===", 'cyan'))
        for key, value in menu_options.items():
            print(colored(f"[{key}]", 'yellow') + f" {value}")
        print()
        
        choice = input(colored("Select option: ", 'green'))
        return choice
    
    def get_wifi_interfaces(self):
        """Get available WiFi interfaces"""
        try:
            if os.name == 'posix':
                interfaces = subprocess.check_output(['iwconfig'], stderr=subprocess.DEVNULL).decode()
                wifi_interfaces = []
                for line in interfaces.split('\n'):
                    if 'IEEE 802.11' in line:
                        interface = line.split()[0]
                        wifi_interfaces.append(interface)
                return wifi_interfaces
            return []
        except:
            return []
    
    def scan_networks(self):
        """Scan for available WiFi networks"""
        print(colored("\n[+] Scanning WiFi Networks...", 'yellow'))
        
        try:
            # Try using nmap
            self.nm.scan(hosts='192.168.1.0/24', arguments='-sn')
            
            networks = []
            for host in self.nm.all_hosts():
                if 'mac' in self.nm[host]['addresses']:
                    networks.append({
                        'ip': host,
                        'mac': self.nm[host]['addresses']['mac'],
                        'hostname': self.nm[host].hostname() if self.nm[host].hostname() else 'Unknown'
                    })
            
            if networks:
                print(colored("\n=== NETWORKS FOUND ===", 'cyan'))
                for idx, net in enumerate(networks, 1):
                    print(f"{idx}. IP: {net['ip']}")
                    print(f"   MAC: {net['mac']}")
                    print(f"   Hostname: {net['hostname']}")
                    print()
            else:
                # Alternative using arp-scan if available
                try:
                    result = subprocess.check_output(['arp-scan', '--localnet'], stderr=subprocess.DEVNULL).decode()
                    print(result)
                except:
                    print(colored("[-] No networks found or insufficient permissions", 'red'))
                    print(colored("[!] Try running with sudo", 'yellow'))
            
            return networks
            
        except Exception as e:
            print(colored(f"[-] Error scanning networks: {e}", 'red'))
            return []
    
    def network_info(self):
        """Get detailed network information"""
        print(colored("\n[+] Gathering Network Information...", 'yellow'))
        
        # Get IP address
        try:
            hostname = socket.gethostname()
            ip_address = socket.gethostbyname(hostname)
            print(colored(f"\nHostname: {hostname}", 'green'))
            print(colored(f"IP Address: {ip_address}", 'green'))
        except:
            pass
        
        # Get gateway
        try:
            if os.name == 'posix':
                route = subprocess.check_output(['ip', 'route']).decode()
                for line in route.split('\n'):
                    if 'default' in line:
                        gateway = line.split()[2]
                        print(colored(f"Gateway: {gateway}", 'green'))
                        break
        except:
            pass
        
        # Get DNS servers
        try:
            with open('/etc/resolv.conf', 'r') as f:
                for line in f:
                    if 'nameserver' in line:
                        dns = line.split()[1]
                        print(colored(f"DNS Server: {dns}", 'green'))
        except:
            pass
        
        # WiFi interface info
        interfaces = self.get_wifi_interfaces()
        if interfaces:
            print(colored(f"\nWiFi Interfaces: {', '.join(interfaces)}", 'green'))
            
            for interface in interfaces:
                try:
                    info = subprocess.check_output(['iwconfig', interface], stderr=subprocess.DEVNULL).decode()
                    # Extract ESSID
                    essid_match = re.search(r'ESSID:"([^"]*)"', info)
                    if essid_match:
                        print(colored(f"Connected to: {essid_match.group(1)}", 'green'))
                except:
                    pass
    
    def scan_devices(self):
        """Scan devices connected to network"""
        print(colored("\n[+] Scanning Connected Devices...", 'yellow'))
        
        try:
            # Use arp-scan for device discovery
            result = subprocess.check_output(['arp-scan', '--localnet'], stderr=subprocess.DEVNULL).decode()
            lines = result.split('\n')[2:-3]  # Skip header and footer
            
            if lines:
                print(colored("\n=== CONNECTED DEVICES ===", 'cyan'))
                for line in lines:
                    parts = line.split()
                    if len(parts) >= 3:
                        ip = parts[0]
                        mac = parts[1]
                        vendor = ' '.join(parts[2:])
                        print(f"IP: {ip} | MAC: {mac} | Vendor: {vendor}")
            else:
                print(colored("[-] No devices found", 'red'))
                
        except Exception as e:
            print(colored(f"[-] Error scanning devices: {e}", 'red'))
            print(colored("[!] Try installing arp-scan: apt install arp-scan", 'yellow'))
    
    def deauth_test(self):
        """Educational demonstration of deauthentication attack"""
        print(colored("\n⚠️  EDUCATIONAL DEMONSTRATION ONLY ⚠️", 'red'))
        print(colored("This shows how deauthentication attacks work for security awareness", 'yellow'))
        
        if not self.check_root():
            print(colored("[-] Root privileges required for this feature", 'red'))
            return
        
        interfaces = self.get_wifi_interfaces()
        if not interfaces:
            print(colored("[-] No WiFi interfaces found", 'red'))
            return
        
        print(colored("\nAvailable WiFi Interfaces:", 'green'))
        for idx, iface in enumerate(interfaces, 1):
            print(f"{idx}. {iface}")
        
        try:
            choice = int(input(colored("\nSelect interface number: ", 'green'))) - 1
            if 0 <= choice < len(interfaces):
                interface = interfaces[choice]
                print(colored(f"\n[+] Selected interface: {interface}", 'green'))
                print(colored("[!] This feature requires monitor mode", 'yellow'))
                print(colored("[!] For educational purposes only - understand WiFi vulnerabilities", 'cyan'))
                
                # Show warning and instructions
                print(colored("\nTo enable monitor mode (for learning):", 'yellow'))
                print(f"sudo airmon-ng start {interface}")
                print("sudo airodump-ng <monitor_interface>")
                print("sudo aireplay-ng -0 0 -a <target_mac> <monitor_interface>")
                
            else:
                print(colored("[-] Invalid selection", 'red'))
        except:
            pass
    
    def wifi_adapter_info(self):
        """Display WiFi adapter information"""
        print(colored("\n[+] WiFi Adapter Information...", 'yellow'))
        
        try:
            if os.name == 'posix':
                # Get wireless info
                iwconfig = subprocess.check_output(['iwconfig'], stderr=subprocess.DEVNULL).decode()
                print(colored("\n=== WIRELESS INTERFACES ===", 'cyan'))
                print(iwconfig)
                
                # Get interface details
                interfaces = self.get_wifi_interfaces()
                for iface in interfaces:
                    print(colored(f"\n=== Details for {iface} ===", 'cyan'))
                    try:
                        iw_info = subprocess.check_output(['iw', 'dev', iface, 'info'], stderr=subprocess.DEVNULL).decode()
                        print(iw_info)
                    except:
                        pass
                        
        except Exception as e:
            print(colored(f"[-] Error getting adapter info: {e}", 'red'))
    
    def check_network_security(self):
        """Basic network security check"""
        print(colored("\n[+] Performing Network Security Check...", 'yellow'))
        
        # Check if WPA3 is supported (simplified check)
        interfaces = self.get_wifi_interfaces()
        if interfaces:
            for iface in interfaces:
                try:
                    info = subprocess.check_output(['iwconfig', iface], stderr=subprocess.DEVNULL).decode()
                    if 'Encryption key:off' in info:
                        print(colored("⚠️  Warning: Open network detected - Unencrypted!", 'red'))
                    elif 'Security' in info:
                        print(colored("✓ Network is encrypted", 'green'))
                except:
                    pass
        
        # Check for common vulnerabilities
        print(colored("\nCommon WiFi Security Recommendations:", 'cyan'))
        print("1. Use WPA3 encryption when available")
        print("2. Use strong passwords (12+ characters, mixed case, symbols)")
        print("3. Disable WPS (WiFi Protected Setup)")
        print("4. Enable MAC address filtering (for additional security)")
        print("5. Keep router firmware updated")
        print("6. Hide SSID (though not a primary security measure)")
        
        # Check open ports on gateway
        try:
            # Get gateway IP
            gateway = None
            route = subprocess.check_output(['ip', 'route']).decode()
            for line in route.split('\n'):
                if 'default' in line:
                    gateway = line.split()[2]
                    break
            
            if gateway:
                print(colored(f"\nScanning gateway ({gateway}) for open ports...", 'yellow'))
                # Quick port scan of common ports
                common_ports = [22, 23, 80, 443, 8080]
                for port in common_ports:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((gateway, port))
                    if result == 0:
                        print(colored(f"⚠️  Port {port} is open on gateway - Check router admin interface", 'red'))
                    sock.close()
        except:
            pass
    
    def monitor_traffic(self):
        """Monitor network traffic (educational)"""
        print(colored("\n[+] Starting Network Traffic Monitor...", 'yellow'))
        print(colored("[!] Press Ctrl+C to stop", 'cyan'))
        
        def packet_handler(packet):
            if packet.haslayer(scapy.IP):
                ip_src = packet[scapy.IP].src
                ip_dst = packet[scapy.IP].dst
                protocol = packet[scapy.IP].proto
                
                proto_name = "TCP" if protocol == 6 else "UDP" if protocol == 17 else f"Other({protocol})"
                print(colored(f"{proto_name}: {ip_src} -> {ip_dst}", 'green'))
        
        try:
            scapy.sniff(prn=packet_handler, store=0, count=100)
        except KeyboardInterrupt:
            print(colored("\n[+] Monitoring stopped", 'yellow'))
        except Exception as e:
            print(colored(f"[-] Error: {e}", 'red'))
            print(colored("[!] Try running with sudo", 'yellow'))
    
    def signal_strength(self):
        """Display WiFi signal strength"""
        print(colored("\n[+] Measuring WiFi Signal Strength...", 'yellow'))
        
        interfaces = self.get_wifi_interfaces()
        for iface in interfaces:
            try:
                # Get signal strength
                result = subprocess.check_output(['iwconfig', iface], stderr=subprocess.DEVNULL).decode()
                quality_match = re.search(r'Quality=(\d+)/(\d+)', result)
                level_match = re.search(r'Signal level=(-?\d+) dBm', result)
                
                if quality_match:
                    current = int(quality_match.group(1))
                    total = int(quality_match.group(2))
                    percentage = (current / total) * 100
                    
                    # Color code based on strength
                    if percentage > 70:
                        color = 'green'
                        status = "Excellent"
                    elif percentage > 40:
                        color = 'yellow'
                        status = "Good"
                    else:
                        color = 'red'
                        status = "Poor"
                    
                    print(colored(f"\nInterface: {iface}", 'cyan'))
                    print(colored(f"Signal: {percentage:.1f}% - {status}", color))
                    
                    if level_match:
                        print(colored(f"Signal Level: {level_match.group(1)} dBm", 'white'))
                        
            except Exception as e:
                print(colored(f"[-] Could not get signal for {iface}", 'red'))
    
    def about(self):
        """Display about information"""
        print(colored("\n=== ABOUT wifi-b4 ===", 'cyan'))
        print(colored("Developer: babar", 'green'))
        print(colored("Instagram: @the_babarrrr", 'green'))
        print(colored("Version: 1.0", 'green'))
        print()
        print(colored("Purpose:", 'yellow'))
        print("This tool is designed for educational purposes to help understand")
        print("WiFi security concepts, network analysis, and potential vulnerabilities.")
        print()
        print(colored("Features:", 'yellow'))
        print("• WiFi network scanning")
        print("• Device discovery")
        print("• Network traffic monitoring")
        print("• Security assessment")
        print("• Signal strength analysis")
        print()
        print(colored("Legal Notice:", 'red'))
        print("This tool should only be used on networks you own or have")
        print("explicit permission to test. Unauthorized network access")
        print("is illegal and unethical.")
        print()
        input(colored("Press Enter to continue...", 'green'))
    
    def run(self):
        """Main execution loop"""
        if not self.check_root():
            print(colored("⚠️  Warning: Not running as root. Some features may be limited.", 'yellow'))
            print(colored("For full functionality, run with: sudo python3 wifi_b4.py", 'yellow'))
            time.sleep(2)
        
        while True:
            self.print_banner()
            choice = self.show_menu()
            
            if choice == '1':
                self.scan_networks()
                input(colored("\nPress Enter to continue...", 'green'))
            
            elif choice == '2':
                self.network_info()
                input(colored("\nPress Enter to continue...", 'green'))
            
            elif choice == '3':
                self.scan_devices()
                input(colored("\nPress Enter to continue...", 'green'))
            
            elif choice == '4':
                self.deauth_test()
                input(colored("\nPress Enter to continue...", 'green'))
            
            elif choice == '5':
                self.wifi_adapter_info()
                input(colored("\nPress Enter to continue...", 'green'))
            
            elif choice == '6':
                self.check_network_security()
                input(colored("\nPress Enter to continue...", 'green'))
            
            elif choice == '7':
                self.monitor_traffic()
                input(colored("\nPress Enter to continue...", 'green'))
            
            elif choice == '8':
                self.signal_strength()
                input(colored("\nPress Enter to continue...", 'green'))
            
            elif choice == '9':
                self.about()
            
            elif choice == '0':
                print(colored("\n[+] Exiting... Stay secure!", 'green'))
                sys.exit(0)
            
            else:
                print(colored("[-] Invalid option", 'red'))
                time.sleep(1)

def main():
    """Entry point"""
    try:
        tool = WiFiSecurityTool()
        tool.run()
    except KeyboardInterrupt:
        print(colored("\n\n[!] Interrupted by user", 'yellow'))
        sys.exit(0)
    except Exception as e:
        print(colored(f"\n[!] Error: {e}", 'red'))
        sys.exit(1)

if __name__ == "__main__":
    main()