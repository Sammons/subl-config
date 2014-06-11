import sublime, sublime_plugin, logging, os

def ensureModed(settings):
	if (not settings.has('keys')):
		settings.set('keys',0)

def toggleMode(settings,mode):
	if settings.get('keys')==mode:
		settings.set('keys',0)
	else: 
		settings.set('keys',mode)

class SetModeCommand(sublime_plugin.TextCommand):
	def run(self, edit, mode):
		settings = self.view.settings()
		toggleMode(settings,mode)
		print(settings.get('keys'))


class BindCommandsCommand(sublime_plugin.TextCommand):
	def run(self, edit, commands):
		settings = self.view.settings()
		ensureModed(settings)
		for command in commands:
			if (settings.get('keys')==command['mode']):
				if 'args' in command:
					self.view.run_command(command['command'],command['args'])
				else:
					self.view.run_command(command['command'])
				if 'subsequently' in command:
					settings.set('keys',command['subsequently'])

#terminal in current directory
class terminalCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file_name=self.view.file_name()
        path=file_name.split("/")
        current_driver=path[0]
        path.pop()
        current_directory="/".join(path)
        command=  "gnome-terminal --working-directory="+current_directory+" &"
        os.system(command)

#fix for find_under_expand
class ExpandCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        regions = []
        for s in self.view.sel():
            word = self.view.word(sublime.Region(s.begin(), s.end()))
            if word.end() == s.end():
                # this next part deals with an end of line issue
                word = self.view.word(sublime.Region(s.end(), s.end() + 1))
            regions.append(word)
        for r in regions:
            self.view.sel().add(r)


		

