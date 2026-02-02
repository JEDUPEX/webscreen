import pygame
import base64
import io
from . import main

def update_screen(surface):
    """
    Saves a pygame Surface to a base64 encoded string.
    """
    # 1. Create a BytesIO object to act as an in-memory file
    image_buffer = io.BytesIO()

    # 2. Save the Pygame surface to the buffer in a specific format (PNG works well)
    # This function expects a file-like object as the second argument
    pygame.image.save(surface, image_buffer, "PNG")

    # 3. Get the bytes from the buffer and encode them in Base64
    image_bytes = image_buffer.getvalue()
    base64_bytes = base64.b64encode(image_bytes)

    # 4. Convert the base64 bytes to a standard string
    base64_string = base64_bytes.decode('utf-8')
    
    # Optional: Add a data URI prefix for web use (e.g., in HTML)
    data_uri = f"data:image/png;base64,{base64_string}"

    main.SCREEN_DATA = data_uri