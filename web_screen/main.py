import asyncio
import websockets
import http.server
import socketserver
import functools
import threading
from pathlib import Path
import json
from . import __version__
from .controls import process_input,configure

DIRECTORY = Path(__file__).resolve().parent
HOST = "127.0.0.1"
SCREEN_DATA = ""

async def screen_handler(websocket):
    try:
        while True:
            await websocket.send(SCREEN_DATA)
            # Non-blocking sleep to allow other tasks to run
            await asyncio.sleep(0) 
    except websockets.exceptions.ConnectionClosedOK:
        print("Client disconnected normally")
    except Exception as e:
        print(f"Error: {e}")
        
async def input_handler(websocket):
    path = websocket.request.path
    try:
        async for message in websocket:
            if path == '/input':
                actions = json.loads(message)
                await process_input(actions)
    except Exception:
        pass
        
# WebSocket Server Logic
async def handler(websocket):
    await asyncio.gather(
        screen_handler(websocket),
        input_handler(websocket),
    )
        
async def start_websocket_server():
    # Start the WebSocket server on port 8765
    async with websockets.serve(handler, HOST, 8765):
        print(f"WebSocket server started on ws://{HOST}:8765")
        await asyncio.Future()  # Run forever

# HTTP Server Logic for the HTML file
def start_http_server():
    PORT = 8000
    Handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=DIRECTORY)
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Web Screen started at http://{HOST}:{PORT}")
        try:
            httpd.serve_forever()
        except:
            exit()

def start_websocket_server_in_thread():
    # The asyncio event loop and server logic run entirely within this thread
    async def server_main():
        async with websockets.serve(handler, HOST, 8765):
            await asyncio.Future()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(server_main())
    try:
        loop.run_forever()
    except:
        exit()

def start_screen(width,height):
    configure(width,height)
    # Run the HTTP server in a separate thread
    http_thread = threading.Thread(target=start_http_server)
    http_thread.daemon = True # Allows the thread to exit with the main program
    http_thread.start()

    # Run the WebSocket server in the main asyncio loop
    websocket_thread = threading.Thread(target=start_websocket_server_in_thread)
    websocket_thread.daemon = True
    websocket_thread.start()
    
if __name__ == "__main__":
    Print(f'Web screen verision {__version__}')
    #start_screen()
