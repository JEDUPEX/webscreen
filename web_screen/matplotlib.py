import matplotlib.pyplot as plt
import io
import base64
from . import main

def update_screen():
    global SCREEN_DATA
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches="tight")
    plt.close()
    
    # 3. Rewind the buffer to the beginning
    buf.seek(0)
    
    # 4. Encode the bytes to Base64 and decode to a UTF-8 string
    base64_string = base64.b64encode(buf.read()).decode('utf-8')
    
    
    data_uri = f"data:image/png;base64,{base64_string}"
    main.SCREEN_DATA = data_uri

if __name__ == "__main__":
    plt.figure() # Needed to manage figures explicitly if using plt interface
    plt.plot([0, 1, 2, 3], [0, 4, 1, 4])
    plt.title("Sample Matplotlib Plot")