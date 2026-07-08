import http.server, socketserver, os
os.chdir("/Users/dhiren/Downloads/Deccan/Adobe-Freelance-Leads/input_assets")
h = http.server.SimpleHTTPRequestHandler
socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("127.0.0.1", 8899), h) as s:
    print("serving input_assets on 8899")
    s.serve_forever()
