import uasyncio
from modules.requestparser import RequestParser
from modules.responsebuilder import ResponseBuilder
from modules.wlanconnection import WiFiConnection as wifi
from modules.iohandler import IoHandler
from modules.controller import Controller
from modules.router import Router
from modules.networkcredentials import NetworkCredentials
import machine
import time

io = IoHandler()
router = Router()

io.led_test()

wifi.startup()

async def rotate_led_color():
    counter = 1
    while True:
        if counter == 1:
            io.set_led([10, 0, 0])
            #print("red")
            await uasyncio.sleep(1)
        elif counter == 2:
            io.set_led([0, 10, 0])
            #print("green")
            await uasyncio.sleep(1)
        elif counter == 3:
            io.set_led([0, 0, 10])
            #print("blue")
            await uasyncio.sleep(1)
        
        counter = 1 if counter >= 3 else counter + 1
        
async def update_display():
    while True:
        if io.button1_pin.value() == 0:
            await io.show_display()
        await uasyncio.sleep(0)
            
async def hide_display():
     while True:
        if io.button1_pin.value() == 1:
            await io.clear_display()
        await uasyncio.sleep(0)
        
async def record_temp():
    while True:
        io.set_temp_value_f(io.sensor)
        await uasyncio.sleep(1)


async def main():
    print('Setting up web server...')
    server = uasyncio.start_server(router.handle_request, "0.0.0.0", 80)
    uasyncio.create_task(server)
    uasyncio.create_task(rotate_led_color())
    uasyncio.create_task(update_display())
    uasyncio.create_task(hide_display())
    uasyncio.create_task(record_temp())
    
    while True:
        await uasyncio.sleep(0)
    
try:
    uasyncio.run(main())
finally:
    uasyncio.new_event_loop()










