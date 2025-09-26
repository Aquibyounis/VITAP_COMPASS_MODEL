import random
import string

def generate_session_id(length=24):
    """Generate a unique session ID with letters and digits."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
