
github_user = 'Zeebrow'
github_url = f'https://github.com/{github_user}'
github_repo_list = ['wish', ]

class Entry:
    def __init__(self, parent):
        self.level = -1
        if parent.isinstance(Entry):
            self.parent = parent
        else:
            self.parent = None
        self.children = []


    def __iter__(self):

