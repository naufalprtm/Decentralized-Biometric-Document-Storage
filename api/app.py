from flask import Flask, request, jsonify
from flask_cors import CORS
from tinybio_integration import TinyBioIntegration
from http.server import BaseHTTPRequestHandler
from os.path import dirname, abspath, join
dir = dirname(abspath(__file__))

app = Flask(__name__)
CORS(app)

# Constants
TOKEN_EXPIRY_DURATION = 300  # 5 menit dalam detik
NODE_COUNT = 3

# Initialize TinyBio integration
tinybio_integration = TinyBioIntegration(NODE_COUNT)

# Function to check biometric token validity
@app.route('/validate-biometric-token', methods=['POST'])
def validate_biometric_token():
    try:
        data = request.json
        hex_key = data.get('hex_key')
        if not hex_key:
            return jsonify({'error': 'Hex key is required'}), 400
        
        valid = tinybio_integration.validate_biometric_token(hex_key, TOKEN_EXPIRY_DURATION)
        
        if valid:
            return jsonify({'valid': True})
        else:
            return jsonify({'valid': False, 'message': 'Token has expired'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Function to update biometric token
@app.route('/update-biometric-token', methods=['POST'])
def update_biometric_token():
    try:
        hex_key = request.json['hex_key']
        
        success = tinybio_integration.update_biometric_token(hex_key)
        
        if success:
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Failed to update biometric token'}), 500
    
    except KeyError:
        return jsonify({'error': 'Hex key is required'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route untuk autentikasi biometrik
@app.route('/authenticate-biometric', methods=['POST'])
def authenticate_biometric():
    try:
        hex_key = request.json['hex_key']
        
        authenticated = tinybio_integration.authenticate_biometric(hex_key)
        
        return jsonify({'authenticated': authenticated}), 200
        
    except KeyError:
        return jsonify({'error': 'Hex key is required'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 'Method not allowed'}), 405
