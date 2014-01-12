import sublime, sublime_plugin, logging, os

def ensureModed(settings):
	if (not settings.has('ben-mode')):
		settings.set('ben-mode',0)

def toggleMode(settings,mode):
	if settings.get('ben-mode')==mode:
		settings.set('ben-mode',0)
	else: 
		settings.set('ben-mode',mode)

class SetModeCommand(sublime_plugin.TextCommand):
	def run(self, edit, mode):
		settings = self.view.settings()
		toggleMode(settings,mode)
		print(settings.get('ben-mode'))


class BindCommandsCommand(sublime_plugin.TextCommand):
	def run(self, edit, commands):
		settings = self.view.settings()
		ensureModed(settings)
		for command in commands:
			if (settings.get('ben-mode')==command['mode']):
				if 'args' in command:
					self.view.run_command(command['command'],command['args'])
				else:
					self.view.run_command(command['command'])
				if 'subsequently' in command:
					settings.set('ben-mode',command['subsequently'])

#terminal in current directory
class terminalCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        file_name=self.view.project_path()
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


		

