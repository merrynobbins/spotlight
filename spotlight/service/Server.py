from spotlight.service.util.Settings import Settings
from spotlight.service.session.SpotifyCallbacks import SpotifyCallbacks  
from spotlight.service.session.SessionFactory import SessionFactory
from spotlight.service.session.MainLoopThread import MainLoopThread
from spotlight.service.LocalService import LocalService
from spotlight.service.session.Authenticator import Authenticator
from spotlight.service.session.ProxyInfo import ProxyInfo
from spotlight.service.util.UrlGenerator import UrlGenerator
from spotlight.service.util.ModelFactory import ModelFactory
from spotifyproxy.audio import BufferManager
from spotify import MainLoop
from spotifyproxy.httpproxy import ProxyRunner
from SimpleXMLRPCServer import SimpleXMLRPCServer

class Server:

    def __init__(self):
        self.settings = Settings()
        self.buffer_manager = BufferManager()
        self.authenticator = Authenticator()
        self.main_loop = MainLoop()

    def run(self):
        session = self.set_up_session()
        self.set_up_authenticator(session)
        self.start_main_loop(self.main_loop, session)        
        proxy_info = self.start_proxy_runner(self.buffer_manager, session)
        self.log_in()
        self.start_rpc_server(self.authenticator, session, proxy_info)

    def start_main_loop(self, main_loop, session):
        runner = MainLoopThread(main_loop, session)
        runner.start()

    def start_proxy_runner(self, buf, session):
        proxy_runner = ProxyRunner(session, buf, host='127.0.0.1', allow_ranges=False)
        proxy_runner.start()
        proxy_info = ProxyInfo(proxy_runner)
        return proxy_info

    def start_rpc_server(self, authenticator, session, proxy_info):
        model_factory = self.create_model_factory(session, proxy_info)
        server = SimpleXMLRPCServer(("localhost", self.settings.internal_server_port))
        server.register_instance(LocalService(session, authenticator, model_factory))
        server.serve_forever()

    def set_up_session(self):
        callbacks = SpotifyCallbacks(self.main_loop, self.buffer_manager, self.authenticator)
        session = SessionFactory(callbacks, self.settings).create_session()
        return session

    def set_up_authenticator(self, session):
        return self.authenticator.set_session(session)

    def log_in(self):
        return self.authenticator.login(self.settings.username, self.settings.password)

    def create_model_factory(self, session, proxy_info):
        url_gen = UrlGenerator(session, proxy_info)
        model_factory = ModelFactory(url_gen)
        return model_factory
    
        
