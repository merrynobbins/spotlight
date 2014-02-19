class AlbumFilter:
    
    def __init__(self, albums):
        self.albums = albums
        
    def filter(self):
        dictionary = {}
        for album in self.albums:
            current_value = dictionary.get(album.name())
            if current_value is None: 
                dictionary[album.name()] = album
                
        return sorted(dictionary.values(), key = lambda album : album.year(), reverse = True)
                 
                
            