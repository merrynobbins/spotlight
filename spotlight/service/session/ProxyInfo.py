from urllib import urlencode

class ProxyInfo:
    
    def __init__(self, proxy_runner):
        self.proxy_runner = proxy_runner
        self.host = proxy_runner.get_host()
        self.port = proxy_runner.get_port()
        self.url_headers = self.get_url_headers()
        
    def get_url_headers(self):
        user_agent = "Spotlight 1.0"
        user_token = self.proxy_runner.get_user_token(user_agent)

        return urlencode({'User-Agent': user_agent, 'X-Spotify-Token': user_token})