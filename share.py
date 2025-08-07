#!/usr/bin/env python3
"""
Image Scraper Sharing Helper
Shows all ways colleagues can access your scraper
"""

import subprocess
import socket
import sys

def get_local_ip():
    """Get local network IP address"""
    try:
        # Connect to a remote server to determine local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "Unable to determine"

def check_server_running():
    """Check if Flask server is running on port 8080"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        result = s.connect_ex(('localhost', 8080))
        s.close()
        return result == 0
    except:
        return False

def main():
    print("🕷️  IMAGE SCRAPER - SHARING OPTIONS")
    print("=" * 50)
    
    # Check if server is running
    if not check_server_running():
        print("❌ Server not running! Start it first:")
        print("   cd '/Users/nikhilprasad/Documents/SCRAPPING AGENT'")
        print("   source venv/bin/activate && python app.py")
        print()
        return
    
    print("✅ Server is running!")
    print()
    
    local_ip = get_local_ip()
    
    print("📍 ACCESS OPTIONS FOR COLLEAGUES:")
    print()
    
    print("1️⃣  SAME NETWORK ACCESS (Easiest)")
    print("   Perfect for office/home colleagues on same WiFi")
    print(f"   🔗 URL: http://{local_ip}:8080")
    print("   ✅ Works immediately, no setup needed")
    print()
    
    print("2️⃣  INTERNET ACCESS (ngrok)")
    print("   For colleagues anywhere in the world")
    print("   📋 Setup steps:")
    print("      1. Sign up: https://dashboard.ngrok.com/signup")
    print("      2. Get authtoken: https://dashboard.ngrok.com/get-started/your-authtoken")
    print("      3. Run: ngrok config add-authtoken YOUR_TOKEN")
    print("      4. Run: ngrok http 8080")
    print("   ✅ Free plan available")
    print()
    
    print("3️⃣  SECURE SHARING (Tailscale)")
    print("   Create a private network with colleagues")
    print("   📋 Setup steps:")
    print("      1. You: tailscale up")
    print("      2. Colleagues install Tailscale and join your network")
    print(f"      3. They access: http://{local_ip}:8080")
    print("   ✅ Secure and easy")
    print()
    
    print("4️⃣  SEND FILES DIRECTLY")
    print("   If internet sharing isn't needed")
    print("   📋 Steps:")
    print("      1. Run scraper yourself")
    print("      2. Download the ZIP files")
    print("      3. Send ZIP files to colleagues via email/Slack")
    print("   ✅ Simple for one-time sharing")
    print()
    
    print("🎯 RECOMMENDED:")
    print("   • Same office/home: Option 1")
    print("   • Remote colleagues: Option 2 (ngrok)")
    print("   • Security focused: Option 3 (Tailscale)")
    print()

if __name__ == "__main__":
    main() 