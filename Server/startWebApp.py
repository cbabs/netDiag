from waitress import serve

import logging
logger = logging.getLogger('waitress')
logger.setLevel(logging.INFO)

import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from Server import app

serve(app,  host='0.0.0.0', port=8443)