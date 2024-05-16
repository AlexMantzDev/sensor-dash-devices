from machine import I2C, Pin, SoftSPI, PWM
import ssd1306
import mcp9808
from wificonnection import WiFiConnection
import uasyncio
import utime



class IoHandler:
    
    # Initialize I2C
    i2c = I2C(0, scl = Pin(21), sda=Pin(20), freq=400000)
    # Initialize SPI
    spi = SoftSPI(baudrate = 500000, polarity = 1, phase = 0, sck = Pin(18), mosi = Pin(19), miso = Pin(16))
    dc = Pin(22)
    rst = Pin(27)
    cs = Pin(17)
    display = ssd1306.SSD1306_SPI(128, 64, spi, dc, rst, cs)
    # Initialize MCP9808 sensor
    sensor = mcp9808.MCP9808(i2c)
    # Initialize button
    button1_pin = Pin(0, Pin.IN, Pin.PULL_UP)
    button2_pin = Pin(1, Pin.IN, Pin.PULL_UP)
    
    red_pin = Pin(13, Pin.OUT)
    green_pin = Pin(12, Pin.OUT)
    blue_pin = Pin(11, Pin.OUT)

    r_pwm = PWM(red_pin)
    g_pwm = PWM(green_pin)
    b_pwm = PWM(blue_pin)
    
    led_values = [0, 0, 0]
    
    temp = None
    ip = WiFiConnection.ip
    
    def __init__(self):
        self.__class__.display.fill(0)
        self.__class__.set_led([20,20,0])
        self.__class__.show_display()
        
    @classmethod
    def show_led(cls):
        cls.r_pwm.duty_u16(int(cls.led_values[0] * 65535 - 1 / 255))
        cls.g_pwm.duty_u16(int(cls.led_values[1] * 65535 - 1 / 255))
        cls.b_pwm.duty_u16(int(cls.led_values[2] * 65535 - 1 / 255))
        
    @classmethod
    def set_led(cls, values):
        try:
            cls.set_red_value(values[0])
            cls.set_green_value(values[1])
            cls.set_blue_value(values[2])
        except:
            pass
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
    def get_temp_value_f(cls):
        return cls.temp
    
    @classmethod
    def set_display_temp(cls):
        cls.set_temp_value_f(cls.sensor)
        cls.display.text("Temperature: ", 0, 0)
        cls.display.text("{:.2f} F".format(cls.get_temp_value_f()), 0, 9)
        
    @classmethod
    def set_ip(cls):
        cls.ip = WiFiConnection.ip
        
    @classmethod
    def set_display_ip(cls):
        cls.set_ip()
        cls.display.text("{}".format(cls.ip), 0, 18)
    
    @classmethod
    async def show_display(cls):
        cls.display.fill(0)
        cls.set_display_temp()
        cls.set_display_ip()
        cls.display.show()
        await uasyncio.sleep(.5)
        
    @classmethod
    def clear_display(cls):
        cls.display.fill(0)
        cls.display.show()



