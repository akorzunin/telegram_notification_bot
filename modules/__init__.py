import os
from dotenv import load_dotenv
load_dotenv()
PWD = os.path.abspath(os.getcwd())
import sys
sys.path.insert(1, PWD)