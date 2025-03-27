import network
import socket
import machine

# Wi-Fi Credentials
SSID = "Your_WiFi_SSID"  # Enter your network SSID
PASSWORD = "Your_WiFi_Password"  # Enter your network password

# Relay setup
relay = machine.Pin(15, machine.Pin.OUT)
relay.value(0)  # Ensure relay starts OFF

# Connect to Wi-Fi
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(SSID, PASSWORD)

print("Connecting to Wi-Fi...", end="")
while not wlan.isconnected():
    pass

# Get IP Address and Port
ip_address = wlan.ifconfig()[0]
port = 8080  # Change this if needed

print(f"\n✅ Connected to Wi-Fi!")
print(f"🌐 Access the Web Server at: http://{ip_address}:{port}")

# Web server setup
def web_page():
    state = "ON" if relay.value() == 1 else "OFF"
    html = f"""
    <html>
    <head><title>Pico W Smart Switch</title></head>
    <body>
        <h2>Raspberry Pi Pico W - Smart Home</h2>
        <p>Relay is currently: <strong>{state}</strong></p>
        <a href="/on"><button style="padding:10px 20px;">Turn ON</button></a>
        <a href="/off"><button style="padding:10px 20px;">Turn OFF</button></a>
    </body>
    </html>
    """
    return html

# Start Web Server on Specified Port
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', port))
s.listen(5)

while True:
    conn, addr = s.accept()
    print(f"🔗 Connection from {addr}")  # Debugging line
    request = conn.recv(1024).decode()
    print("📩 Request Received:", request)  # Debugging line

    if "/on" in request:
        relay.value(1)  # Turn ON relay
    elif "/off" in request:
        relay.value(0)  # Turn OFF relay

    response = web_page()
    conn.send("HTTP/1.1 200 OK\nContent-Type: text/html\n\n")
    conn.send(response)
    conn.close()
