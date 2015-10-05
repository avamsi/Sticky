from contextlib import contextmanager
import sublime
import sublime_plugin

@contextmanager
def load_settings(save=True):
    settings = sublime.load_settings('sticky.sublime-settings')
    sticked = settings.get('sticked')
    yield sticked # sticked is mutable and it is very important
    if save:
        settings.set('sticked', sticked)
        sublime.save_settings('sticky.sublime-settings')

def plugin_loaded(): # cleaning up
    with load_settings() as tabs:
        for tab in tabs.keys():
            if tab.startswith('sticky-id'):
                del tabs[tab]


class InterceptCloseCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        with load_settings(save=False) as tabs:
            tab = self.view.file_name()
            if tab is None:
                tab = 'sticky-id: %s' % self.view.id()
            if tab not in tabs:
                self.view.window().run_command('close')


class StickCurrentTabCommand(sublime_plugin.TextCommand):
    def __init__(self, view):
        with load_settings(save=False) as tabs:
            if view.file_name() in tabs:
                view.set_status('_', 'STICKED')
        self.view = view

    def run(self, edit):
        with load_settings() as tabs:
            tab = self.view.file_name()
            if tab is None:
                tab = 'sticky-id: %s' % self.view.id()
            tabs[tab] = None
        self.view.set_status('_', 'STICKED')


class UnstickCurrentTabCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        with load_settings() as tabs:
            tab = self.view_file_name()
            if tab is None:
                tab = 'sticky-id: %s' % self.view.id()
            tabs.pop(tab, None)
        self.view.erase_status('_')
