import sys
import os

# Add project directory to the system path
sys.path.insert(0, os.path.dirname(__file__))

from app import app as application
