#!/usr/bin/env python3
"""
NetSpiderAI-Tor Entry Point
"""
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gui.main_window import MainWindow

if __name__ == "__main__":
    app = MainWindow()
    app.mainloop()
