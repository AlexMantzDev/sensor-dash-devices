from machine import I2C, Pin, SoftSPI, PWM
from modules.wlanconnection import WiFiConnection as wifi
import uasyncio
import time
from modules.ssd1306 import SSD1306_SPI
from modules.mcp9808 import MCP9808

class IoHandler:
    
    # Initialize I2C
    i2c = I2C(0, scl = Pin(21), sda=Pin(20), freq=400000)
    # Initialize SPI
    spi = SoftSPI(baudrate = 500000, polarity = 1, phase = 0, sck = Pin(18), mosi = Pin(19), miso = Pin(16))
    dc = Pin(22)
    rst = Pin(27)
    cs = Pin(17)
    display = SSD1306_SPI(128, 64, spi, dc, rst, cs)
    # Initialize MCP9808 sensor
    sensor = MCP9808(i2c)
    # Initialize button
    button1_pin = Pin(0, Pin.IN, Pin.PULL_UP)
    button2_pin = Pin(1, Pin.IN, Pin.PULL_UP)
    
    red_pin = Pin(13, Pin.OUT)
    green_pin = Pin(12, Pin.OUT)
    blue_pin = Pin(11, Pin.OUT)

    r_pwm = PWM(red_pin)
    g_pwm = PWM(green_pin)
    b_pwm = PWM(blue_pin)
    
    r_pwm.freq(1000)
    g_pwm.freq(1000)
    b_pwm.freq(1000)
    
    led_values = [0, 0, 0]
    
    
    
    temp = None
    wlan_ip = wifi.wlan_ip
    ap_ip = wifi.ap_ip
    wifi_mode = wifi.mode
    
    def __init__(self):
        self.__class__.display.fill(0)
        self.__class__.set_led([10,10,0])
        self.__class__.show_display()
        
    @classmethod
    def led_test(cls):
        cls.r_pwm.duty_u16(32768)  # 50% duty cycle
        cls.g_pwm.duty_u16(0)    # 0% duty cycle
        cls.b_pwm.duty_u16(0)     # 0% duty cycle
        time.sleep(1)

        cls.r_pwm.duty_u16(0)      
        cls.g_pwm.duty_u16(32768)
        cls.b_pwm.duty_u16(0)
        time.sleep(1)

        cls.r_pwm.duty_u16(0)
        cls.g_pwm.duty_u16(0)
        cls.b_pwm.duty_u16(32768)
        time.sleep(1)

        cls.r_pwm.duty_u16(0)
        cls.g_pwm.duty_u16(0)
        cls.b_pwm.duty_u16(0)
        
    @classmethod
    def show_led(cls):
        cls.r_pwm.duty_u16(int(cls.led_values[0] * 65535 - 1 / 255))
        cls.g_pwm.duty_u16(int(cls.led_values[1] * 65535 - 1 / 255))
        cls.b_pwm.duty_u16(int(cls.led_values[2] * 65535 - 1 / 255))
        
    @classmethod
    def set_led(cls, values):
        cls.set_red_value(values[0])
        cls.set_green_value(values[1])
        cls.set_blue_value(values[2])
        cls.show_led()
    
    @classmethod
    def set_red_value(cls, value):
        if value <= 0:
            cls.led_values[0] = 0
        elif value >= 255:
            cls.led_values[0] = 255
        else:
            cls.led_values[0] = value
            
    @classmethod
    def set_green_value(cls, value):
        if value <= 0:
            cls.led_values[1] = 0
        elif value >= 255:
            cls.led_values[1] = 255
        else:
            cls.led_values[1] = value
          
    @classmethod
    def set_blue_value(cls, value):
        if value <= 0:
            cls.led_values[2] = 0
        elif value >= 255:
            cls.led_values[2] = 255
        else:
            cls.led_values[2] = value
            
    @classmethod
    def get_red_value(cls):
        return cls.led_values[0]
    
    @classmethod
    def get_green_value(cls):
        return cls.led_values[1]
    
    @classmethod
    def get_blue_value(cls):
        return cls.led_values[2]
    
    @classmethod
    def set_temp_value_f(cls, sensor):
        cls.temp = sensor.read_temp_f()
    
    @classmethod
    def get_temp_value(cls):
        return cls.temp
    
    @classmethod
    def set_display_temp(cls):
        cls.display.text("Temperature: ", 0, 0)
        cls.display.text("{:.2f} F".format(cls.get_temp_value()), 0, 9)
        
    @classmethod
    def set_ip(cls):
        cls.wlan_ip = wifi.wlan_ip
        cls.ap_ip = wifi.ap_ip
        
    @classmethod
    def set_wlan_mode(cls):
        cls.wifi_mode = wifi.mode
        
    @classmethod
    def set_display_ip(cls):
        cls.set_ip()
        if cls.wifi_mode == "STA":
            cls.display.text("IP: {}".format(cls.wlan_ip), 0, 18)
        if cls.wifi_mode == "AP":
            cls.display.text("IP: {}".format(cls.ap_ip), 0, 18)
        
    @classmethod
    def set_display_wlan_mode(cls):
        cls.set_wlan_mode()
        cls.display.text("Mode: {}".format(cls.wifi_mode), 0, 27)
    
    @classmethod
    async def show_display(cls):
        cls.display.fill(0)
        cls.set_display_temp()
        cls.set_display_ip()
        cls.set_display_wlan_mode()
        cls.display.show()
        await uasyncio.sleep(0)
        
    @classmethod
    async def clear_display(cls):
        cls.display.fill(0)
        cls.display.show()
        await uasyncio.sleep(0)





