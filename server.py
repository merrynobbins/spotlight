from SimpleXMLRPCServer import SimpleXMLRPCServer
from spotilight.service.util.LibLoader import LibLoader
import xbmc
from spotilight.service.util.Settings import Settings
from spotilight.service.util.ModelFactory import ModelFactory
from spotilight.model.ListItemFactory import ListItemFactory
  
loader = LibLoader()
loader.add_library_paths(['resources/libs/CherryPy.egg',
                          'resources/libs/TaskUtils.egg',
                          'resources/libs/PyspotifyCtypes.egg',
                          'resources/libs/PyspotifyCtypesProxy.egg'])
loader.set_library_paths('resources/dlls')
  
from spotilight.service.session.SpotifySetup import SpotifySetup
from spotilight.service.SpotiLightService import SpotiLightService
from spotifyproxy.audio import BufferManager
from spotifyproxy.httpproxy import ProxyRunner
from spotilight.service.playback.Player import Player
from spotilight.service.session.Authenticator import Authenticator
from spotilight.service.session.ProxyInfo import ProxyInfo
from spotilight.service.util.UrlGenerator import UrlGenerator
  
buf = BufferManager(5)
authenticator = Authenticator()
session = SpotifySetup(buf, authenticator).launch()
proxy_runner = ProxyRunner(session, buf, host='127.0.0.1', allow_ranges=False)
proxy_runner.start()
proxy_info = ProxyInfo(proxy_runner)
list_item_factory = ListItemFactory(session, proxy_info)
url_gen = UrlGenerator(session, proxy_info)
message_factory = ModelFactory(url_gen)
settings = Settings()
player = Player(session, list_item_factory)
authenticator.login(settings.username(), settings.password())
  
xbmc.log('port: %s' % proxy_runner.get_port())
  
server = SimpleXMLRPCServer(("localhost", 8000))
server.register_instance(SpotiLightService(session, player, authenticator, message_factory))
server.serve_forever() 