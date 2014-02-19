from spotilight.ui.Router import Router
from spotilight.ui.UiHelper import UiHelper
import xbmc
import xbmcgui
import xbmcplugin
import sys
import xmlrpclib
from spotilight.ui.ErrorHandler import ErrorHandler
import socket

class Navigation:
    
    def __init__(self):
        self.addon_handle = int(sys.argv[1])
        self.server = xmlrpclib.ServerProxy('http://localhost:8000')
        socket.setdefaulttimeout(30)  
        self.uiHelper = UiHelper()
        router_config = {None : self.main_menu, 
                         'starred' : self.starred, 
                         'search' : self.search, 
                         'play' : self.play,
                         'play_list' : self.play_list,
                         'playlists' : self.play_lists_menu,
                         'get_playlist' : self.get_playlist,
                         'album_tracks' : self.album_tracks,
                         'artist_albums' : self.artist_albums}
        
        Router(router_config, self)
     
    def main_menu(self, args):
        
        self.uiHelper.create_folder_item('Search...', Router.url_for('search'))
        self.uiHelper.create_folder_item('Starred', Router.url_for('starred'))
        self.uiHelper.create_folder_item('Playlists', Router.url_for('playlists'))
      
        xbmcplugin.endOfDirectory(self.addon_handle)
     
    def play_lists_menu(self, args):
        playlists = self.server.playlists()
        self.uiHelper.create_list_of_playlists(playlists)
        
    def get_playlist(self, args):
        tracks = self.server.playlist_tracks(args['name'])
        self.uiHelper.create_list_of_tracks(tracks)
            
    def starred(self, args):                
        tracks = self.server.starred()
        self.uiHelper.create_list_of_tracks(tracks)
    
    def play(self, track):
        self.server.play(track)
        
    def play_list(self, args):
        self.server.play_list(args['tracks'], args['starting_track'])

    def search(self, args):        
        query = self.uiHelper.keyboardText()
        if query is not None:
            tracks = self.server.search(query)
            self.uiHelper.create_list_of_tracks(tracks)
        
    def album_tracks(self, args):
        tracks = self.server.album_tracks(args['album'])
        self.uiHelper.create_list_of_tracks(tracks)
        
    def artist_albums(self, args):
        albums = self.server.artist_albums(args['track'])
        self.uiHelper.create_list_of_albums(albums)

        
        
      
    
        
        
        