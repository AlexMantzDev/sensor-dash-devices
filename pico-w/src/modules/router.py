from modules.controller import Controller
from modules.responsebuilder import ResponseBuilder
from modules.requestparser import RequestParser
    

class Router:
    
    def __init__(self):
        self.response_builder = ResponseBuilder()
        self.req = None
        self.req_data = None
        self.routes = {
            'GET': {
                '/temp': self.get_temp_reading,
                '/wifi/scan': self.scan_wifi,
            },
            'POST': {
                '/wifi/config': self.set_wifi_config,
            }
        }
    
    async def handle_request(self, reader, writer):
        print("Incomming request...")
        try:
            raw_request = await reader.read(2048)
            self.req = RequestParser(raw_request)
            self.req_data = self.req.data()
            
            method = self.req.method
            url = self.req.url
            handler = self.routes.get(method, {}).get(url, self.wildcard)
            handler()
            
            self.response_builder.build_response()
            writer.write(self.response_builder.response)
            await writer.drain()
            await writer.wait_closed()
        except OSError as e:
            print('connection error ' + str(e.errno) + " " + str(e))
    
    def get_temp_reading(self):
        if self.req.url_match('/temp') and self.req.method == 'GET':
            response_obj = Controller.get_temp_reading()
            self.response_builder.set_body_from_dict(response_obj)
        
    def scan_wifi(self):
        if self.req.url_match('/wifi/scan') and self.req.method == 'GET':
            response_obj = Controller.scan_wifi()
            self.response_builder.set_body_from_dict(response_obj)
        
    def set_wifi_config(self):
        if self.req.url_match('/wifi/config') and self.req.method == 'POST':
            ssid = self.req.data()['ssid']
            password = self.req.data()['password']
            response_obj = Controller.configure_wifi(ssid, password)
            self.response_builder.set_status(200)
            self.response_builder.set_body_from_dict(response_obj)
            
    def wildcard(self):
        self.response_builder.serve_static_file(self.req.url, "/web/wifi-config.html")


