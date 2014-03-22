# 
#  Copyright (c) Dariusz Biskup
#  
#  This file is part of Spotlight
# 
#  Spotlight is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as 
#  published by the Free Software Foundation; either version 3 of 
#  the License, or (at your option) any later version.
#  
#  Spotlight is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>
#  

from spotlight.ui.Router import Router
from spotlight.model.Model import Model
from spotlight.ui.Paths import Paths
from spotlight.model.GlobalSettings import GlobalSettings
import sys
import xbmcplugin
import xmlrpclib
import socket
import xbmcgui

class Navigation:
    
    SPOTILITE_SERVER = 'http://127.0.0.1:%d'

    def __init__(self, ui_helper):
        self.addon_handle = int(sys.argv[1])        
        self.ui_helper = ui_helper
        self.settings = GlobalSettings()
        self.create_server_proxy()  
        
        router_config = {None : self.main_menu, 
                         Paths.INBOX: self.inbox,
                         Paths.INBOX_ALBUMS: self.inbox_albums,
                         Paths.INBOX_ARTISTS: self.inbox_artists,
                         Paths.INBOX_PLAYLISTS: self.inbox_playlists,
                         Paths.INBOX_TRACKS: self.inbox_tracks,
                         Paths.STARRED : self.starred, 
                         Paths.SEARCH : self.search, 
                         Paths.PLAYLISTS : self.play_lists_menu,
                         Paths.GET_PLAYLIST : self.get_playlist,
                         Paths.ALBUM_TRACKS : self.album_tracks,
                         Paths.ARTIST_ALBUMS : self.artist_albums,
                         Paths.ARTIST_ALBUMS_FOR_TRACK : self.artist_albums_for_track,
                         Paths.START_SESSION: self.start_session,
                         Paths.STOP_SESSION: self.stop_session,
                         Paths.HAS_ACTIVE_SESSION: self.has_active_session,                         
                         }
        Router(router_config, self)

    def start_session(self):
        self.server.start_session()
        
    def stop_session(self, args = {}):
        result = self.server.stop_session()
        dialog = xbmcgui.Dialog()
        dialog.ok("Spotlight", result)
        
    def has_active_session(self):
        return self.server.has_active_session()
        
    def main_menu(self, args):
        self.start_session()
        
        self.ui_helper.create_folder_item('Inbox', Router.url_for(Paths.INBOX))
        self.ui_helper.create_folder_item('Search...', Router.url_for(Paths.SEARCH))
        self.ui_helper.create_folder_item('Starred', Router.url_for(Paths.STARRED))
        self.ui_helper.create_folder_item('Playlists', Router.url_for(Paths.PLAYLISTS))
        self.ui_helper.create_folder_item('Stop server', Router.url_for(Paths.STOP_SESSION))
      
        self.ui_helper.end_directory()
     
    def get_local_server_url(self):
        return Navigation.SPOTILITE_SERVER % self.settings.internal_server_port 

    def create_server_proxy(self):
        self.server = xmlrpclib.ServerProxy(self.get_local_server_url())
        socket.setdefaulttimeout(30)
        
    def play_lists_menu(self, args):
        playlists = Model.from_object_list(self.server.playlists())
        self.ui_helper.create_list_of_playlists(playlists)
        self.ui_helper.end_directory()
        
    def get_playlist(self, args):
        tracks = Model.from_object_list(self.server.playlist_tracks(args.uri))
        self.ui_helper.create_list_of_tracks(tracks)
        self.ui_helper.end_directory()
            
    def inbox(self, args):
        inbox = Model.from_object(self.server.inbox())
        
        self.ui_helper.create_list_of_playlists(Model.from_object_list(inbox.playlists))
        self.ui_helper.create_list_of_albums(Model.from_object_list(inbox.albums))
        self.ui_helper.create_list_of_artists(Model.from_object_list(inbox.artists))
        self.ui_helper.create_list_of_tracks(Model.from_object_list(inbox.tracks))
        self.ui_helper.end_directory()
        
    def inbox_albums(self, args):
        pass
    
    def inbox_playlists(self, args):
        pass
    
    def inbox_artists(self, args):
        pass
    
    def inbox_tracks(self, args):
        pass
            
    def starred(self, args):                
        tracks = Model.from_object_list(self.server.starred())
        self.ui_helper.create_list_of_tracks(tracks)
        self.ui_helper.end_directory()
 
    def search(self, args):        
        query = self.ui_helper.keyboardText()
        if query is not None:
            tracks = Model.from_object_list(self.server.search(query))
            self.ui_helper.create_list_of_tracks(tracks)
        self.ui_helper.end_directory()
        
    def album_tracks(self, args):
        tracks = Model.from_object_list(self.server.album_tracks(args.album))
        self.ui_helper.create_list_of_tracks(tracks)
        self.ui_helper.end_directory()
        
    def artist_albums_for_track(self, args):
        albums = Model.from_object_list(self.server.artist_albums_from_track(args.track))
        self.ui_helper.create_list_of_albums(albums)
        self.ui_helper.end_directory()
        
    def artist_albums(self, args):
        albums = Model.from_object_list(self.server.artist_albums(args.artist))
        self.ui_helper.create_list_of_albums(albums)
        self.ui_helper.end_directory()

            
      
    
        
        
        