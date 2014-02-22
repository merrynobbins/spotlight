from spotlight.ui.Router import Router
from spotlight.model.Model import Model
from spotlight.ui.Paths import Paths
from spotlight.service.util.Settings import Settings
import sys
import xbmcplugin
import xmlrpclib
import socket

class Navigation:
    
    SPOTILITE_SERVER = 'http://localhost:%d'

    def __init__(self, ui_helper):
        self.addon_handle = int(sys.argv[1])        
        self.ui_helper = ui_helper
        self.settings = Settings()
        self.create_server_proxy()  
        
        router_config = {None : self.main_menu, 
                         Paths.STARRED : self.starred, 
                         Paths.SEARCH : self.search, 
                         Paths.PLAYLISTS : self.play_lists_menu,
                         Paths.GET_PLAYLIST : self.get_playlist,
                         Paths.ALBUM_TRACKS : self.album_tracks,
                         Paths.ARTIST_ALBUMS : self.artist_albums}
        Router(router_config, self)
        

     
    def main_menu(self, args):
        self.ui_helper.create_folder_item('Search...', Router.url_for(Paths.SEARCH))
        self.ui_helper.create_folder_item('Starred', Router.url_for(Paths.STARRED))
        self.ui_helper.create_folder_item('Playlists', Router.url_for(Paths.PLAYLISTS))
      
        xbmcplugin.endOfDirectory(self.addon_handle)
     
    def get_local_server_url(self):
        return Navigation.SPOTILITE_SERVER % self.settings.internal_server_port 

    def create_server_proxy(self):
        self.server = xmlrpclib.ServerProxy(self.get_local_server_url())
        socket.setdefaulttimeout(30)
        
    def play_lists_menu(self, args):
        playlists = Model.from_object_list(self.server.playlists())
        self.ui_helper.create_list_of_playlists(playlists)
        
    def get_playlist(self, args):
        tracks = Model.from_object_list(self.server.playlist_tracks(args.name))
        self.ui_helper.create_list_of_tracks(tracks)
            
    def starred(self, args):                
        tracks = Model.from_object_list(self.server.starred())
        self.ui_helper.create_list_of_tracks(tracks)
 
    def search(self, args):        
        query = self.ui_helper.keyboardText()
        if query is not None:
            tracks = Model.from_object_list(self.server.search(query))
            self.ui_helper.create_list_of_tracks(tracks)
        
    def album_tracks(self, args):
        tracks = Model.from_object_list(self.server.album_tracks(args.album))
        self.ui_helper.create_list_of_tracks(tracks)
        
    def artist_albums(self, args):
        albums = Model.from_object_list(self.server.artist_albums(args.track))
        self.ui_helper.create_list_of_albums(albums)

            
      
    
        
        
        