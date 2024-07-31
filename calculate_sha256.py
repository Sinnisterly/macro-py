import hashlib

def calculate_checksum(file_path, algorithm='sha256'):
    hash_func = hashlib.new(algorithm)
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()

checksum = calculate_checksum('D:\Projects\macro-py\file.zip')
print(f"SHA-256 Checksum: {checksum}")
