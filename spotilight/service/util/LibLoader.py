import xbmc
import os, sys, platform
import xbmcaddon

class LibLoader:
	
	def __init__(self):
		__addon_id__ = 'plugin.audio.spotifyxbmcplugin'
		addon_cfg = xbmcaddon.Addon(__addon_id__)
		self.addon_path = addon_cfg.getAddonInfo('path')
	
	def get_architecture(self):
		try:
			machine = platform.machine()
			
			#Some filtering...
			if machine.startswith('armv6'):
				return 'armv6'
			
			elif machine.startswith('i686'):
				return 'x86'
		
		except:
			return None
	
	def add_library_paths(self, paths):
		for path in paths:
			self.add_library_path(path)
	
	def add_library_path(self, path):
		full_path = os.path.join(self.addon_path, path)
		sys.path.append(full_path)
	
	def set_library_paths(self, base_dir):
		arch_str = self.get_architecture()
		
		if xbmc.getCondVisibility('System.Platform.Linux'):
			if arch_str in(None, 'x86'):
				self.add_library_path(os.path.join(base_dir, 'linux/x86'))
			
			if arch_str in(None, 'x86_64'):
				self.add_library_path(os.path.join(base_dir, 'linux/x86_64'))
			
			if arch_str in(None, 'armv6'):
				self.add_library_path(os.path.join(base_dir, 'linux/armv6hf'))
				self.add_library_path(os.path.join(base_dir, 'linux/armv6'))
		
		elif xbmc.getCondVisibility('System.Platform.Windows'):
			if arch_str in(None, 'x86'):
				self.add_library_path(os.path.join(base_dir, 'windows/x86'))
			else:
				raise OSError('Sorry, only 32bit Windows is supported.')
		
		elif xbmc.getCondVisibility('System.Platform.OSX'):
			self.add_library_path(os.path.join(base_dir, 'osx'))
		
		else:
			raise OSError('Sorry, this platform is not supported.')
