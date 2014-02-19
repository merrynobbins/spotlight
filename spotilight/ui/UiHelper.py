import xbmc
import sys
import xbmcplugin
from spotilight.ui.Router import Router
import xbmcgui

class UiHelper:
    
    def __init__(self):
        self.addon_handle = int(sys.argv[1])
        xbmcplugin.setContent(self.addon_handle, 'songs')
    
    def keyboardText(self, heading = 'Enter phrase'):
        kb = xbmc.Keyboard('default', 'heading', True)
        kb.setDefault('')
        kb.setHeading(heading)
        kb.setHiddenInput(False)
        kb.doModal()
        if (kb.isConfirmed()):
            return kb.getText()     
        return None
    
    def create_folder_item(self, title, url, image = 'DefaultFolder.png'):
        li = xbmcgui.ListItem(title, iconImage = image)
        xbmcplugin.addDirectoryItem(handle = self.addon_handle, url = url, listitem = li, isFolder = True)       
         
    def create_list_of_playlists(self, playlists):
        for playlist in playlists:
            url = Router.url_for('get_playlist', {'name': playlist['name']})
            self.create_folder_item(playlist['name'], url)
        xbmcplugin.endOfDirectory(self.addon_handle)
         
    def create_list_of_tracks(self, tracks):
        self.create_track_list_items(tracks)
        xbmcplugin.endOfDirectory(self.addon_handle)
        
    def create_list_of_albums(self, albums):
        for album in albums:
            url = Router.url_for('album_tracks', {'album': album['uri']})
            self.create_folder_item('%s [%s]' % (album['name'], album['year']), url, album['image'])
        
        xbmcplugin.endOfDirectory(self.addon_handle)

    def create_track_list_items(self, tracks):
        track_uris = map(lambda track : track['uri'], tracks)
        for index, track in enumerate(tracks):
            self.create_track_list_item(track, track_uris, index + 1)

    def add_context_menu(self, track, play_url, li):
        browse_album_url = Router.url_for('album_tracks', {'album':track['album_uri']})
        browse_artist_url = Router.url_for('artist_albums', {'track':track['uri']})
        
        li.addContextMenuItems([('Queue item', 'XBMC.RunPlugin(%s)' % play_url), 
                                ('Browse album...', 'XBMC.Container.Update(%s)' % browse_album_url), 
                                ('Browse artist...', 'XBMC.Container.Update(%s)' % browse_artist_url)], 
                               replaceItems=False)
        
    def create_track_list_item(self, track, track_uris, index = 0):
        li = xbmcgui.ListItem('%s - %s' % (track['album'], track['track']), 
                              iconImage = track['iconImage'],
                              thumbnailImage = track['thumbnailImage'], 
                              path = track['path'])        
        li.setInfo('music', {'album':track['album'], 
                             'artist':track['artist'], 
                             'title' : track['track'],            
                             'duration':track['time'], 
                             'tracknumber' : index})
        
        self.add_context_menu(track, track['path'], li)
        xbmcplugin.addDirectoryItem(handle=self.addon_handle, url = track['path'], listitem=li, isFolder=False)
