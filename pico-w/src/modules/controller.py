from modules.responsebuilder import ResponseBuilder
from modules.iohandler import IoHandler
from modules.requestparser import RequestParser
from modules.wlanconnection import WiFiConnection
from modules.networkcredentials import NetworkCredentials
import utime

class Controller:
    def __init__(self):
        pass
        
    def get_temp_reading():
        temp_value = IoHandler.get_temp_value()
        response_obj = {
            'temperature': temp_value
        }
        return response_obj
    
    def scan_wifi():
        networks = WiFiConnection.wlan.scan()
        formatted_networks = []
        for network in networks:
            ssid = network[0].decode('utf-8')  # Convert bytes to string
            bssid = ":".join("{:02x}".format(byte) for byte in network[1])
            security = network[2]
            channel = network[3]
            RSSI = network[4]
            hidden = network[5]
        
            formatted_network = {
                'ssid': ssid,
                'bssid': bssid,
                'security': security,
                'channel': channel,
                'RSSI': RSSI,
                'hidden': hidden
            }
            formatted_networks.append(formatted_network)
        
        response_obj = {'networks': formatted_networks}
        return response_obj
    
    def configure_wifi(ssid, password):
        print("switching to sta mode")
        switch_success = WiFiConnection.handle_wifi_switch(ssid, password)
        if switch_success:
            NetworkCredentials.set_credentials(ssid, password)
        response_obj = {
            'message': 'WiFi settings changed'    
        }
        return response_obj
        


