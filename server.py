from SimpleXMLRPCServer import SimpleXMLRPCServer
from spotilight.service.util.LibLoader import LibLoader
import xbmc
from spotilight.service.util.Settings import Settings
from spotilight.model.ListItemFactory import ListItemFactory
  
loader = LibLoader()
loader.load_all()
  
from spotilight.service.session.SpotifySetup import SpotifySetup
from spotilight.service.SpotiLightService import SpotiLightService
from spotifyproxy.audio import BufferManager
from spotifyproxy.httpproxy import ProxyRunner
from spotilight.service.session.Authenticator import Authenticator
from spotilight.service.session.ProxyInfo import ProxyInfo
from spotilight.service.util.UrlGenerator import UrlGenerator
from spotilight.service.util.ModelFactory import ModelFactory
  
buf = BufferManager(5)
authenticator = Authenticator()
session = SpotifySetup(buf, authenticator).launch()
proxy_runner = ProxyRunner(session, buf, host='127.0.0.1', allow_ranges=False)
proxy_runner.start()
proxy_info = ProxyInfo(proxy_runner)
url_gen = UrlGenerator(session, proxy_info)
model_factory = ModelFactory(url_gen)
settings = Settings()
authenticator.login(settings.username(), settings.password())
  
xbmc.log('port: %s' % proxy_runner.get_port())
  
server = SimpleXMLRPCServer(("localhost", 8000))
server.register_instance(SpotiLightService(session, authenticator, model_factory))
server.serve_forever() 