from spotilight.service.util.LibLoader import LibLoader
loader = LibLoader()
loader.load_all() 

from spotilight.service.Server import Server    

Server().run()        