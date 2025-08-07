#!/usr/bin/env python3
"""
Website Image Scraper - Startup Script
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ All packages installed successfully!")
    except subprocess.CalledProcessError:
        print("❌ Failed to install packages. Please run: pip install -r requirements.txt")
        sys.exit(1)

def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        'flask',
        'requests', 
        'beautifulsoup4'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            if package == 'beautifulsoup4':
                try:
                    __import__('bs4')
                except ImportError:
                    missing_packages.append(package)
            else:
                missing_packages.append(package)
    
    return missing_packages

def main():
    print("🖼️  Website Image Scraper")
    print("=" * 50)
    
    # Check if requirements are met
    missing = check_requirements()
    if missing:
        print(f"⚠️  Missing packages: {', '.join(missing)}")
        response = input("Would you like to install them now? (y/n): ").lower()
        if response in ['y', 'yes']:
            install_requirements()
        else:
            print("Please install the required packages and try again.")
            sys.exit(1)
    
    # Start the application
    print("🚀 Starting the web application...")
    print("📍 Open your browser and go to: http://localhost:8080")
    print("🛑 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        # Import and run the Flask app
        from app import app
        app.run(debug=False, port=8080, host='127.0.0.1')
    except ImportError:
        print("❌ Could not import the main application. Make sure app.py exists.")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 Application stopped. Goodbye!")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 