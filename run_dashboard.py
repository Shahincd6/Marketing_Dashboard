#!/usr/bin/env python3
"""
Run the Marketing Intelligence Dashboard with AI Insights
"""

import subprocess
import sys
import os

def main():
    print("🚀 Starting Marketing Intelligence Dashboard with AI Insights...")
    print("📊 Dashboard will be available at: http://localhost:8501")
    print("🤖 AI insights powered by Google Gemini")
    print("⏹️  Press Ctrl+C to stop")
    print("-" * 60)
    
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "src/dashboard.py"])
    except KeyboardInterrupt:
        print("\n👋 Dashboard stopped")

if __name__ == "__main__":
    main()
