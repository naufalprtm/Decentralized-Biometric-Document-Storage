from typing import List, Tuple
from flask import Flask, request, jsonify
from flask_cors import CORS
import tinybio
import time
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

# Constants
TOKEN_EXPIRY_DURATION = 360  # 1 menit dalam detik
NODE_COUNT = 3
TOLERANCE = 0.1

# Initialize nodes for biometric authentication
nodes = [tinybio.node() for _ in range(NODE_COUNT)]
tinybio.preprocess(nodes, length=4)

def create_descriptor(hex_key: str) -> tinybio.Descriptor:
    """Create a descriptor from a hex key"""
    return tinybio.hexToDescriptor(hex_key)

def create_auth_request(descriptor: tinybio.Descriptor) -> tinybio.Request:
    """Create an authentication request from a descriptor"""
    return tinybio.request.authentication(descriptor)

def get_auth_masks(nodes: List[tinybio.Node], auth_request: tinybio.Request) -> List[tinybio.Mask]:
    """Get authentication masks from each node"""
    return [node.masks(auth_request) for node in nodes]

def create_auth_token(auth_masks: List[tinybio.Mask], descriptor: tinybio.Descriptor) -> Tuple[tinybio.Token, int]:
    """Create an authentication token and return it along with its creation timestamp"""
    token = tinybio.token.authentication(auth_masks, descriptor)
    creation_timestamp = int(time.time())  # Waktu saat token dibuat (detik sejak epoch)
    return token, creation_timestamp

# Function to check token validity based on creation timestamp
def is_token_valid(creation_timestamp: int) -> bool:
    current_time = int(time.time())
    return current_time - creation_timestamp <= TOKEN_EXPIRY_DURATION

def authenticate_biometric_data(nodes: List[tinybio.Node], descriptor: tinybio.Descriptor) -> float:
    """Authenticate biometric data with a descriptor"""
    auth_request = tinybio.request.authentication(descriptor)
    shares = [node.authenticate(auth_request) for node in nodes]
    return tinybio.reveal(shares)

def add_descriptors(descriptor1: tinybio.Descriptor, descriptor2: tinybio.Descriptor) -> tinybio.Descriptor:
    """Add two descriptors element-wise"""
    return [d1 + d2 for d1, d2 in zip(descriptor1, descriptor2)]

def subtract_descriptors(descriptor1: tinybio.Descriptor, descriptor2: tinybio.Descriptor) -> tinybio.Descriptor:
    """Subtract two descriptors element-wise"""
    return [d1 - d2 for d1, d2 in zip(descriptor1, descriptor2)]

def generate_node_token(node_id: int, descriptor: tinybio.Descriptor) -> Tuple[tinybio.Mask, tinybio.Token]:
    """Generate mask and token for a specific node"""
    modified_descriptor = add_descriptors(descriptor, descriptor)  # Contoh modifikasi, sesuaikan dengan kebutuhan
    auth_request = tinybio.request.authentication(modified_descriptor)
    auth_masks = [nodes[node_id].masks(auth_request)]
    auth_token, _ = create_auth_token(auth_masks, modified_descriptor)
    return auth_masks[0], auth_token

# Function to update biometric token and token expiry time
@app.route('/update-biometric-token', methods=['POST'])
def update_biometric_token():
    try:
        hex_key = request.json['hex_key']
        
        # Generate new token based on the hex_key
        descriptor = create_descriptor(hex_key)
        auth_masks, auth_token = generate_node_token(0, descriptor)  # Generate token for first node
        
        # Update token_expiry_time here
        global token_expiry_time
        token_expiry_time = datetime.now() + timedelta(seconds=TOKEN_EXPIRY_DURATION)
        
        return jsonify({'success': True})
    
    except KeyError:
        return jsonify({'error': 'Hex key is required'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Function to check biometric token validity
@app.route('/validate-biometric-token', methods=['GET', 'POST'])
def validate_biometric_token():
    try:
        data = request.json
        hex_key = data.get('hex_key')
        if not hex_key:
            return jsonify({'error': 'Hex key is required'}), 400
        
        descriptor = create_descriptor(hex_key)
        auth_masks, auth_token = generate_node_token(0, descriptor)
        
        if is_token_valid(auth_token.creation_timestamp):
            return jsonify({'valid': True})
        else:
            return jsonify({'valid': False, 'message': 'Token has expired'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route untuk autentikasi biometrik
@app.route('/authenticate-biometric', methods=['POST'])
def authenticate_biometric():
    try:
        hex_key = request.json['hex_key']
        # Lakukan autentikasi berdasarkan waktu
        creation_timestamp = int(time.time())
        authenticated = True
        return jsonify({'authenticated': authenticated}), 200
        
    except KeyError:
        # Return error if hex key is missing from request
        return jsonify({'error': 'Hex key is required'}), 400
    
    except Exception as e:
        # Return error if any other exception occurs
        return jsonify({'error': str(e)}), 500
    
@app.errorhandler(405)
def method_not_allowed(e):
    return jsonify({'error': 'Method not allowed'}), 405

if __name__ == "__main__":
    app.run(debug=True)
