#!/usr/bin/env python3
"""
Setup script for Investo
"""

import os
import sys
from pathlib import Path

def create_directories():
    """Create necessary directories"""
    directories = [
        "logs",
        "cache", 
        "reports/generated",
        "venv"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Created directory: {directory}")

def create_env_file():
    """Create .env file from example"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_example.exists() and not env_file.exists():
        env_file.write_text(env_example.read_text())
        print("✅ Created .env file from template")
        print("⚠️  Please edit .env with your actual API keys")
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("❌ .env.example not found")

def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} detected")

def main():
    """Main setup function"""
    print("🚀 Setting up Investo...")
    
    check_python_version()
    create_directories()
    create_env_file()
    
    print("\n📋 Next steps:")
    print("1. Edit .env with your API keys")
    print("2. Install dependencies: pip install -r requirements.txt")
    print("3. Run the bot: python main.py")
    print("\n🎉 Setup complete!")

if __name__ == "__main__":
    main()
