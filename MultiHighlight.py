import sublime, sublime_plugin

SCOPES = ['variable.parameter', 'string', 'support.constant', 'invalid.illegal', 'invalid.deprecated']

class MultiHighlightCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		regions = self.view.sel()
	
		if len(regions) > 0 and regions[0].size() > 0:
			value = self.view.substr(regions[0])
			HighlightKeys = self.view.settings().get('hkvalues', [])
			try:
				i = HighlightKeys.index(value)
			except ValueError:
				i = -1
			if i == -1:
				HighlightKeys.append(value)
				regions = self.view.find_all(value, sublime.LITERAL)
				self.view.add_regions(value, regions,  SCOPES[HighlightKeys.index(value) % len(SCOPES)] , '', sublime.HIDE_ON_MINIMAP)
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
