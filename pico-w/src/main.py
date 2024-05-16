import utime
import network
import socket
import urequests
from requestparser import RequestParser
from responsebuilder import ResponseBuilder
from wificonnection import WiFiConnection
from iohandler import IoHandler
import uasyncio
import random

if not WiFiConnection.start_station_mode(True):
    raise RuntimeError('network connection failed')



io = IoHandler()

async def handle_req(reader, writer):
    try:
        raw_request = await reader.read(2048)
        req = RequestParser(raw_request)
        response_builder = ResponseBuilder()
        
        if req.url_match("/temp") and req.method == 'GET':
            temp_value = io.get_temp_value_f()
            response_obj = {
                'temperature': temp_value
            }
            response_builder.set_body_from_dict(response_obj)
    except:
         response_builder.server_static_file(req.url, "/api_index.html")
        
    response_builder.build_response()
    writer.write(response_builder.response)
    await writer.drain()
    await writer.wait_closed()
    
async def randomize_led_color():
    counter = 1
    while True:
        if counter == 1:
            io.set_led([10, 0, 0])
            await uasyncio.sleep(0.5)
        elif counter == 2:
            io.set_led([0, 10, 0])
            await uasyncio.sleep(0.5)
        elif counter == 3:
            io.set_led([0, 0, 10])
            await uasyncio.sleep(0.5)
        
        counter = 1 if counter >= 3 else counter + 1
        
        
async def update_display():
    while True:
        await io.show_display()
        await uasyncio.sleep(0)


async def main():
    print('Setting up web server...')
    server = uasyncio.start_server(handle_req, "0.0.0.0", 80)
    uasyncio.create_task(server)
    uasyncio.create_task(randomize_led_color())
    uasyncio.create_task(update_display())
    
    while True:
        await uasyncio.sleep(0)
    
try:
    uasyncio.run(main())
finally:
    uasyncio.new_event_loop()
