import re
ATX_HEADING = '^\s{0,3}(?P<level>[#]{1,6})(?:\s*)?(?P<heading>.*)'
SETEXT = '^[ ]{0,3}(?P<setext>[=\-])(?P=setext)*\s*'
CODEFENCE = '^[ ]{0,3}(?P<level>[`~]{3,})(?P<lang>[\w]*)'
THEM_BRK = '^[ ]{0,3}(?P<ch>[\-\_\*])(?:(?P=ch)|\s*){2,}\Z'

#regex = {
#        # groups: level, text
#        'pound_heading': '^\s{0,3}(?P<level>[#]{1,6})(?:\s*)?(?P<heading>.*)',
#        
#        # NOTE: whatever string precedes without line break will render
#        # so basically, an entire paragraph can be a heading.
#        # https://spec.commonmark.org/0.30/#setext-heading
#        #
#        # groups: setext
#        'setext': '^[ ]{0,3}(?P<setext>[=\-])(?P=setext)*\s*', 
#
#        # https://spec.commonmark.org/0.30/#code-fence
#        #
#        # groups: lang
#        'codefence': '^[ ]{0,3}(?P<level>[`~]{3,})(?P<lang>[\w]*)',
#
#        # NOTE: will also match setext
#        # https://spec.commonmark.org/0.30/#thematic-break
#        #
#        # groups: ch(arcter used)
#        'thematic_break': '^[ ]{0,3}(?P<ch>[\-\_\*])(?:(?P=ch)|\s*){2,}\Z' 
#        }


