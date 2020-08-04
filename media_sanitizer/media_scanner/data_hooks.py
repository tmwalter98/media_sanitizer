import sys


class Hooks:
    def __init__(self):
        self.hooks = dict()
        return

    def add_hook(self, hook, fish):
        if self.hooks.get(hook):
            sys.stderr.write('attempted to overwrite hook \'{}\'. \
              To modify hook, use \'modify_hook(hook, fish)\''.format(hook))
        else:
            self.hooks[hook] = fish

    def modify_hook(self, hook, fish):
        self.hooks[hook] = fish

    def get(self, hook):
        return self.hooks.get(hook)

    def __iter__(self):
        return self.hooks
