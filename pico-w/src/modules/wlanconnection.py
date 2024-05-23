import time
import network
from modules.networkcredentials import NetworkCredentials


class WiFiConnection:
    # class level vars accessible to all code
    status = network.STAT_IDLE
    wlan_ip = ""
    wlan_subnet_mask = ""
    wlan_gateway = ""
    wlan_dns_server = ""
    ap_ip = ""
    ap_subnet_mask = ""
    ap_gateway = ""
    ap_dns_server = ""
    ap_ssid = ""
    mode=""
    wlan = network.WLAN(network.STA_IF)
    ap = network.WLAN(network.AP_IF)
    
    def __init__(self):
        pass
    
    @classmethod
    def clear_saved_credentials(cls):
        print("Clearing saved WiFi credentials.")      
        if cls.ap.active():
            cls.ap.active(False)
            time.sleep(1)
        if cls.wlan.isconnected():
            cls.wlan.disconnect()
            time.sleep(1)
        if cls.wlan.active():
            cls.wlan.active(False)
            time.sleep(1)
        wlan_config = cls.wlan.ifconfig()
        ap_config = cls.ap.ifconfig()
        cls.wlan_ip = wlan_config[0]
        cls.wlan_subnet_mask = wlan_config[1]
        cls.wlan_gateway = wlan_config[2]
        cls.wlan_dns_server = wlan_config[3]
        cls.ap_ip = ap_config[0]
        cls.ap_subnet_mask = ap_config[1]
        cls.ap_gateway = ap_config[2]
        cls.ap_dns_server = ap_config[3]
        cls.ap_ssid = cls.ap.config('essid')
        cls.mode = ""
        
    
    @classmethod
    def start_ap_mode(cls, ssid, password, ip, print_progress=False):
        print("Starting wireless access point...")
        cls.ap.config(essid=ssid, password=password)
        cls.ap.active(True)
        cls.ap.ifconfig((ip, '255.255.255.0', ip, '8.8.8.8'))
        
        config = cls.ap.ifconfig()
        cls.ap_ip = config[0]
        cls.ap_subnet_mask = config[1]
        cls.ap_gateway = config[2]
        cls.ap_dns_server = config[3]
        cls.ap_ssid = cls.ap.config('essid')
        cls.mode = "AP"
        if print_progress:
            print('ip = ' + str(cls.ap_ip))
        return True

    @classmethod
    def stop_ap_mode(cls):
        print("Stopping AP mode...")
        cls.ap.active(False)
        print("AP mode stopped")

    @classmethod
    def start_station_mode(cls, ssid, password, print_progress=False):
        cls.wlan.active(True)
        cls.wlan.disconnect()
        time.sleep(1)
        cls.wlan.connect(ssid, password)
    
        print("Connecting to WiFi")
    
        max_wait = 30
        while max_wait > 0:
            status = cls.wlan.status()
            """
            0   STAT_IDLE -- no connection and no activity,
            1   STAT_CONNECTING -- connecting in progress,
            -3  STAT_WRONG_PASSWORD -- failed due to incorrect password,
            -2  STAT_NO_AP_FOUND -- failed because no access point replied,
            -1  STAT_CONNECT_FAIL -- failed due to other problems,
            3   STAT_GOT_IP -- connection successful.
            """
            if status < 0 or status >= 3:
                # Connection attempt finished
                break
            max_wait -= 1
            time.sleep(0.5)
            if print_progress:
                print(f"Waiting for connection... status={status}")

        # Check connection
        status = cls.wlan.status()
        if status != 3:
            # No connection
            if print_progress:
                print("Connection Failed")
            return False
        else:
            # Connection successful
            config = cls.wlan.ifconfig()
            cls.wlan_ip = config[0]
            cls.wlan_subnet_mask = config[1]
            cls.wlan_gateway = config[2]
            cls.wlan_dns_server = config[3]
            cls.mode = "STA"
            if print_progress:
                print('IP:', config[0])
                print('Subnet Mask:', config[1])
                print('Gateway:', config[2])
                print('DNS Server:', config[3])
            return True
        
    @classmethod
    def stop_station_mode(cls):
        if cls.wlan.isconnected():
            print("Disconnecting from WiFi...")
            cls.wlan.disconnect()
        print("Stopping station mode...")
        cls.wlan.active(False)
        cls.wlan_ip = ""
        cls.wlan_subnet_mask = ""
        cls.wlan_gateway = ""
        cls.wlan_dns_server = ""
        cls.mode = ""
        
    @classmethod
    def handle_wifi_switch(cls, ssid, password):
        cls.stop_station_mode()
        cls.stop_ap_mode()
        cls.clear_saved_credentials()
        if cls.start_station_mode(ssid, password):
            print("Connected to provided network.")
            return True
        else:
            print("No saved credentials. Starting AP mode.")
            cls.start_ap_mode('Pi Pico W Demo', '123123123', '10.10.10.1')
            return False
            
    @classmethod
    def startup(cls):
        if NetworkCredentials.credentials_exist():
            stored_ssid, stored_password = NetworkCredentials.get_credentials()
            if cls.start_station_mode(stored_ssid, stored_password):
                print("Switched to stored network.")
            else:
                print("Failed to connect with stored credentials. Starting AP mode.")
                cls.start_ap_mode('Pi Pico W Demo', '123123123', '10.10.10.1')
        else:
            print("No saved credentials. Starting AP mode.")
            cls.start_ap_mode('Pi Pico W Demo', '123123123', '10.10.10.1')
