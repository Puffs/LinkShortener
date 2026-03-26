import hashlib
import base62

def convert_to_shorten_url(long_url) -> str:
    hash_obj = hashlib.md5(long_url.encode())
    short_id = base62.encode(int(hash_obj.hexdigest(), 16))[:8]
    return short_id