import re

class Quote:
    pass

class CodeFence:
    pass

class OrderedList:
    pass

class UnorderedList:
    pass


class ATX:
    def __init__(self, mdfile):
        self.mdfile = mdfile
        # {lineno: heading_string}
        self.headings = {}

    regex = {
            pound_heading: '^\s{0,3}(#){1,6}(\s*)?(.*)',
            prev_line_heading: '^\s{0,3}([\-])',
            setext: '^[ ]{0,3}', # https://spec.commonmark.org/0.30/#setext-heading
            codefence: '^[ ]{0,3}`{3}' # https://spec.commonmark.org/0.30/#code-fence
            thematic_break: '^[ ]{0,3}(?P<ch>[\-\_\*])((?P=ch)|[ ]){2,}\Z' # https://spec.commonmark.org/0.30/#thematic-break
            }

    dumb_re_headding = re.compile('\s{0,3}(#){1,6}(\s*)?(.*)')
    prev_line_is_heading = re.compile('\s{0,3}')
    codefence = re.compile(self.regex['codefence'])

    def get_atx(self):
        with open(self.mdfile, 'r') as mdf:
            in_codefence = False
            last3 = ['','','']
            for lineno, line in enumerate(mdf.readlines()):
                last3.pop(0)
                last3.append(line)
                if in_codefence:
                    continue
                
                cf = self.codefence.match(line)
                atx = self.dumb_re_headding.match(line)
                
                if cf:
                    in_codefence = not in_codefence
                    continue

                if atx:

if __name__ == '__main__':
    from pathlib import Path
    mdfile = Path('/home/zeebrow/repos/github.com/zeebrow/mddb/tests/example_md_file.md')
    atx = ATX(mdfile)
    with open(mdfile, 'r') as mdf:
        



