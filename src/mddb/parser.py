#avert eyes
from mdtypes import *
from mdregex import *
#revert eyes
import re
# https://spec.commonmark.org/0.30/#appendix-a-parsing-strategy

class Pass1:
    pass
class Pass2:
    pass

class Parser:
    """
    MDDB makes mardown files queriable
    Python-markdown, Marko, and Mistune do not do this.
    :
    A Markdown database is a collection of markdown files stored in git
    """
    def __init__(self, mdfile):
        self.mdfile = mdfile
        # {lineno: heading_string}
        self.entries = []

    def parse(self):
        re_atx = re.compile(ATX_HEADING)
        setext = re.compile(SETEXT)
        codefence = re.compile(CODEFENCE)

        current_context = 'base'
        in_codefence = False
        last3 = ['','','']
        ctx_curr_entry = None
        ctx_blk, ctx_lvl = None, -0 # type(-0) -> int
        ctx_cf_txt, ctx_cf_lvl, ctx_cf_lang = [], -0, ''
        with open(self.mdfile, 'r') as mdf:
            
            for lineno, line in enumerate(mdf.readlines()):
                last3.pop(0)
                last3.append(line)
                
                cf = codefence.match(line)
                atx = re_atx.match(line)
                stxt = setext.match(line)

                if cf and in_codefence:
                    new_cf = CodeFence(
                            text=ctx_cf_txt,
                            level=ctx_cf_lvl,
                            lang=ctx_cf_lang
                            )
                    ctx_curr_entry.add_codefence(new_cf)
                    print(f"got {len(ctx_cf_txt)} lines of code text")
                    in_codefence = False
                elif cf and (not in_codefence):
                    ctx_cf_txt = []
                    ctx_cf_lvl = len(cf.groupdict()['level'])
                    ctx_cf_lang = cf.groupdict()['lang']
                    print(f"l{ctx_cf_lvl} codefence for language: {cf.groupdict()['lang']}")
                    current_context = 'codefence'
                    in_codefence = True
                    continue
                
                if in_codefence:
                    ctx_cf_txt.append(line)
                    continue

                if atx and not in_codefence:
                    text = atx.groupdict()['heading']
                    level = len(atx.groupdict()['level'])

                    e = HashtagHeading(text=text, level=level, lineno=lineno)
                    ctx_curr_entry = e
                    self.entries.append(e)
                    cxt_blk,ctx_lvl = text, level

                    HashtagHeading(level=level, text=text, source_file=self.mdfile, lineno=lineno)
#                    print(f"atx ({lineno}): {line.strip()}")

if __name__ == '__main__':
    from pathlib import Path
    mdfile = Path('/home/zeebrow/repos/github.com/zeebrow/mddb/tests/example_md_file.md')
    mddb = Parser(mdfile)
    mddb.parse()
    print(mddb.entries)
    test_entry_name = 'AST and Setext'
    for i in mddb.entries:
        if i.text == test_entry_name:
            for j in i.code_fences:
                for e in j:
                    print(f"line: {e}")
                print(j)
                print(j.lang)
                print(j.text)
                print(j.level)
    


