import os
from http.server import SimpleHTTPRequestHandler, HTTPServer

# Define the directory you want to serve pages from
# You can change this to the directory you want to use
web_directory = "c:\\tmp"

# Change to the specified directory
os.chdir(web_directory)

# Create a custom handler that serves pages from the specified directory
class CustomHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=os.getcwd(), **kwargs)

# Set the port number you want the server to listen on
port = 8000

# Create the server with the specified port and custom handler
with HTTPServer(("", port), CustomHandler) as httpd:
    print(f"Serving on port {port} from directory {web_directory}")

    # Start the server
    httpd.serve_forever()
