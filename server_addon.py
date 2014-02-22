from spotlight.service.util.LibLoader import LibLoader
loader = LibLoader()
loader.load_all() 

from spotlight.service.Server import Server    

Server().start()        