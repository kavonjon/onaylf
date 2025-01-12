import hashlib
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()


def generate_registration_code():
    # List of simple words for generating the code
    words = str(os.getenv('WORDS')).split(',')
    
    # Use current year as seed
    current_year = str(datetime.now().year)
    
    # Create a deterministic hash based on the year
    hash_obj = hashlib.sha256(current_year.encode())
    hash_value = int(hash_obj.hexdigest(), 16)
    
    # Select 5 words deterministically
    selected_words = []
    for i in range(5):
        index = hash_value % len(words)
        selected_words.append(words[index])
        hash_value = hash_value // len(words)
    
    return " ".join(selected_words)