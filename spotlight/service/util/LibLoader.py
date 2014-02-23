# 
#  Copyright © Dariusz Biskup
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

from spotlight.model.Settings import Settings
import os
import platform
import sys

import xbmc
import xbmcaddon


class Platform:
	
	LINUX = 'System.Platform.Linux'
	WINDOWS = 'System.Platform.Windows'
	OSX = 'System.Platform.OSX'
	
	@staticmethod
	def all_platforms():
		return [getattr(Platform, attr) for attr in vars(Platform) 
			if not callable(getattr(Platform, attr)) and not attr.startswith("__")]
	
class Architecture:
	
	X86 = "x86"
	X86_64 = "x86_64"
	ARMV6 = "armv6"	

class Libraries:
	
	DLL_DIRS = {
				(Platform.LINUX, Architecture.X86) : ["resources/dlls/linux/x86"],
				(Platform.LINUX, Architecture.X86_64) : ["resources/dlls/linux/x86_64"],
				(Platform.LINUX, Architecture.ARMV6) : ["resources/dlls/linux/armv6hf",
													"resources/dlls/linux/armv6"],
				(Platform.WINDOWS, Architecture.X86) : ["resources/dlls/windows/x86"],
				(Platform.OSX, Architecture.X86) : ["resources/dlls/osx"]				
				}
	
	EXTERNAL = ['resources/libs/CherryPy.egg',
	              'resources/libs/PyspotifyCtypes.egg',
	              'resources/libs/PyspotifyCtypesProxy.egg']
	
class LibLoader:
	
	def __init__(self):
		addon_id = Settings.ADD_ON_ID
		addon_cfg = xbmcaddon.Addon(addon_id)
		self.addon_path = addon_cfg.getAddonInfo('path')
	
	def load_all(self):
		self.add_native_libraries()
		self.add_external_libraries()
	
	def add_native_libraries(self):
		architecture = self.get_architecture()
		platform = self.get_platform()
		dirs_to_include = Libraries.DLL_DIRS.get((platform, architecture)) 

		if len(dirs_to_include) == 0:
			raise OSError('This platform is not supported (%s %s)' % (architecture, platform))

		self.add_library_paths(dirs_to_include)
	
	def add_external_libraries(self):
		self.add_library_paths(Libraries.EXTERNAL)
	
	def get_architecture(self):
		architecture = platform.machine()

		if architecture.startswith('armv6'):
			return Architecture.ARMV6
		
		elif architecture.startswith('i686'):
			return Architecture.X86
		
		return architecture
	
	def get_platform(self):
		platforms = [platform for platform in Platform.all_platforms() if xbmc.getCondVisibility(platform)]
		
		if len(platforms) > 0:
			return platforms.pop()
		
		return None
	
	def add_library_paths(self, paths):
		for path in paths:
			self.add_library_path(path)
	
	def add_library_path(self, path):
		full_path = os.path.join(self.addon_path, path)
		sys.path.append(full_path)
	
	
		
		
