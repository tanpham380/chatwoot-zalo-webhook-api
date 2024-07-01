
import base64
import hashlib
import os




# AUTHENCATIONCODE = os.getenv('ZALO_SUCCESS_SECRET')

def generate_code_verifier(length=43):
    """
    Generates a high-entropy cryptographic random string (code verifier).
    The length of the string should be between 43 and 128 characters.
    """

    return base64.urlsafe_b64encode(os.urandom(length)).decode('utf-8').rstrip('=')

def generate_code_challenge(code_verifier):
    """
    Creates a code challenge derived from the code verifier using SHA-256 and base64-url encoding.
    """
    sha256_hash = hashlib.sha256(code_verifier.encode('ascii')).digest()

    base64_encoded = base64.urlsafe_b64encode(sha256_hash).decode('ascii').rstrip('=')
    return base64_encoded




def generate_signature(json_input, api_key, request_body):
    """
    Generates a SHA256 signature from a dictionary of data and an API key.

    Args:
        data (dict): The data to be included in the signature.
        api_key (str): The API key to be used for the signature.

    Returns:
        str: The generated signature as a hexadecimal string.
    """
    


    app_id = json_input['app_id']
    timestamp = json_input['timestamp']
    concatenated_string = app_id + request_body.decode("utf-8") + timestamp + api_key
    sha256_hash = hashlib.sha256(concatenated_string.encode()).hexdigest()
    return sha256_hash

def verify_oa_secret_key(json_data, headers, request_body):
    """Verify the Zalo webhook signature."""
    try:
        secret_key = os.getenv("ZALO_WEBHOOK_VERIFY_TOKEN")
        if not secret_key:
            return False

        calculated_mac = generate_signature(json_data, secret_key, request_body)
        received_mac = headers.get("X-ZEvent-Signature", "").lower()  # Case-insensitive
        
        if calculated_mac == received_mac:
            return True
        else:
            return False
    except Exception as e:
        return False
    
