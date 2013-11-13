import sublime, sublime_plugin, re

SCOPES = ['variable.parameter', 'string', 'support.constant', 'invalid.illegal', 'invalid.deprecated']

class MultiHighlightCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		regions = self.view.sel()		
		
		if len(regions) > 0:
			if (regions[0].size() > 0) :
				value = self.view.substr(regions[0])
			else :
				value = self.view.substr(self.view.word(regions[0])).strip()
				
			HighlightKeys = self.view.settings().get('hkvalues', [])
			try:
				i = HighlightKeys.index(value)
			except ValueError:
				i = -1
			if i == -1:
				HighlightKeys.append(value)
				search = r"([^_0-9a-zA-Z])"+re.escape(value)+r"([^_0-9a-zA-Z])"
				print(search)
				#regions = self.view.find_all(search, sublime.LITERAL)
				begin = 0
				from_point = begin
				regions = []
				while True:
						tmp_region = self.view.find(search, from_point)
						if tmp_region:
								region = self.view.find(re.escape(value), tmp_region.begin())
								regions.append(region)
								from_point = region.end()
						else:
								break
				self.view.add_regions(value, regions,  SCOPES[HighlightKeys.index(value) % len(SCOPES)] , '', sublime.DRAW_EMPTY)
			else :
				HighlightKeys.remove(value)
				self.view.erase_regions(value)
			self.view.settings().set('hkvalues', HighlightKeys)
		else :
			return


class NoMultiHighlightCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		HighlightKeys = self.view.settings().get('hkvalues', [])
		if len(HighlightKeys) == 0:
			return
		for items in HighlightKeys:
			regions = self.view.find_all(items, sublime.LITERAL)
			self.view.erase_regions(items)
		self.view.settings().set('hkvalues', [])
