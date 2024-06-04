import tinybio
import time
from datetime import datetime, timedelta
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
class TinyBioIntegration:
    def __init__(self, node_count):
        self.nodes = [tinybio.node() for _ in range(node_count)]
        tinybio.preprocess(self.nodes, length=4)
        self.token_expiry_time = None

    def create_descriptor(self, hex_key: str) -> tinybio.Descriptor:
        """Create a descriptor from a hex key"""
        return tinybio.hexToDescriptor(hex_key)

    def create_auth_request(self, descriptor: tinybio.Descriptor) -> tinybio.Request:
        """Create an authentication request from a descriptor"""
        return tinybio.request.authentication(descriptor)

    def get_auth_masks(self, auth_request: tinybio.Request) -> list:
        """Get authentication masks from each node"""
        return [node.masks(auth_request) for node in self.nodes]

    def create_auth_token(self, auth_masks: list, descriptor: tinybio.Descriptor) -> tuple:
        """Create an authentication token and return it along with its creation timestamp"""
        token = tinybio.token.authentication(auth_masks, descriptor)
        creation_timestamp = int(time.time())  # Waktu saat token dibuat (detik sejak epoch)
        return token, creation_timestamp

    def is_token_valid(self, creation_timestamp: int, token_expiry_duration: int) -> bool:
        current_time = int(time.time())
        return current_time - creation_timestamp <= token_expiry_duration

    def validate_biometric_token(self, hex_key: str, token_expiry_duration: int) -> bool:
        try:
            descriptor = self.create_descriptor(hex_key)
            auth_request = self.create_auth_request(descriptor)
            auth_masks = self.get_auth_masks(auth_request)
            auth_token, creation_timestamp = self.create_auth_token(auth_masks, descriptor)

            if self.is_token_valid(creation_timestamp, token_expiry_duration):
                return True
            else:
                return False
        except Exception as e:
            print("Error validating biometric token:", e)
            return False

    def update_biometric_token(self, hex_key: str) -> bool:
        try:
            descriptor = self.create_descriptor(hex_key)
            auth_masks, auth_token = self.generate_node_token(0, descriptor)  # Generate token for first node
            
            # Update token_expiry_time here
            self.token_expiry_time = datetime.now() + timedelta(seconds=TOKEN_EXPIRY_DURATION)
            
            return True
        except Exception as e:
            print("Error updating biometric token:", e)
            return False

    def authenticate_biometric(self, hex_key: str) -> bool:
        try:
            descriptor = self.create_descriptor(hex_key)
            auth_request = self.create_auth_request(descriptor)
            shares = [node.authenticate(auth_request) for node in self.nodes]
            return tinybio.reveal(shares)
        except Exception as e:
            print("Error authenticating biometric:", e)
            return False
        
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
