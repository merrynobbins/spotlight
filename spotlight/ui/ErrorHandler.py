import types
import xbmcgui

class ErrorHandler(object):
    
    def __init__ (self, func):
        self.func = func
    
    def __call__ (self, *args, **kw):
        try:
            return self.func (*args, **kw)
        except Exception, e:
            dialog = xbmcgui.Dialog()
            dialog.ok("SpotiLite Error", str(e))
            

    def __get__(self, obj, ownerClass=None):
        return types.MethodType(self, obj)