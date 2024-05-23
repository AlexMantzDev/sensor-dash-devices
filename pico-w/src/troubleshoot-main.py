import uasyncio
import network
import time

# Set up the access point
ap_ssid = "Another Pico WiFi Test"
ap_password = "123123123"

def start_ap_mode(ssid, password):
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    time.sleep(5)
    ap.config(essid=ssid, password=password)
    while not ap.active():
        pass
    print('AP mode started with SSID:', ssid)

async def handle_request(reader, writer):
    print("Request received")
    request_line = await reader.readline()
    print("Request:", request_line)

    response = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\nHello, World!"
    await writer.awrite(response)
    await writer.aclose()

async def main():
    start_ap_mode(ap_ssid, ap_password)
    print('Setting up web server...')
    server = uasyncio.start_server(handle_request, "0.0.0.0", 80)
    uasyncio.create_task(server)
    print("Web server running...")
    
    while True:
        await uasyncio.sleep(0)

try:
    uasyncio.run(main())
finally:
    uasyncio.new_event_loop()

