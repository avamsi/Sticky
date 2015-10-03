import sublime
import sublime_plugin


class InterceptCloseCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings('sticky.sublime-settings')
        sticked = settings.get('sticked')
        if self.view.file_name() in sticked:
            return
        self.view.window().run_command('close')


class StickCurrentTabCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings('sticky.sublime-settings')
        sticked = settings.get('sticked')
        sticked[self.view.file_name()] = None
        settings.set('sticked', sticked)
        sublime.save_settings('sticky.sublime-settings')
        self.view.set_status('_', 'STICKED')


class UnstickCurrentTabCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings('sticky.sublime-settings')
        sticked = settings.get('sticked')
        sticked.pop(self.view.file_name(), None)
        settings.set('sticked', sticked)
        sublime.save_settings('sticky.sublime-settings')
        self.view.erase_status('_')
