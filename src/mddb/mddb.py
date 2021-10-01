import logging
from os import stat, path
import os
import shutil
from textwrap import dedent
from shutil import rmtree
import tempfile
from pathlib import Path
from git import Repo

__all__ = ['Entry']

logger = logging.getLogger(__name__)

## TODO: 'branding'
# first off, shyeddep. I dont have a brand.
# I just need sensical names for compnents
# using placeholders for now, vars ending like
# var_

# heirarchy
# repo -> md_file -> entry (header level)
# each entry has arbitrary nested stuff, upt markdown's limit


class Utils:
    def __ini__(self):
        pass

    def get_all_(self, md_file):
        _regex = re.compile("^##\s+(.*)$")
        _list_ = []
        with open(md_file, 'r') as md:
            for line in md:
                m = _regex.match(line)
                if m:
                    _list_.append(m.groups()[0].strip())
        return _list_

    def check_prj_readme(_md_ting_) -> bool:
        """
        leftovers from grandparent: 
        save a _md_thing_ to a file..
        could be useful
        """
        try:
            with open(w.readme, 'r') as rm:
                lines = rm.read()
                if lines == w.block:
                    return True
                else:
                    return False
        except FileNotFoundError:
            return False
##

default_entry_level_ = lambda level: "#"*level
D= default_entry_level_
new_default_entry_ = lambda entryname_: f"""
{D} {entry_name_}

{D}# Synopsis

{D}# Usage

```
{entry_name_}
```

{D}# Would Require

{D}# Difficulty


"""
###

# maybe Entries should be recursive
# Entry.entries returns next level of entries! :O

class Entry:
    """
    Entrieses are the 'main' uint of data
    """
    def __init__(self, entryname, repo_path='.'):
        # "bare-minimum"-like params
        self.exists = False
        self.name = entryname
        self.sections = None
        # config- and settings-like params
        self.entry_regex_ = re.compile("^##\s+(.*)$")

        # remove when separated
        self.prj_path = self.repo_path / "prj-skel" / self.name
        self.readme = self.prj_path / "README.md"

        # make ready for caller
        self._init_entry()

    def __repr__(self):
        return self.name

    def _init_entry(self):
        try:
            self.exists = self._check_exists()
            if not self.exists:
                self.block = C.new_entry_skel(self.name)
        except Exception as e:
            # what do if failure to launch
            raise e
            
    def _check_exists(self) -> bool:
        """Re-loads self.before, self.after, and self.block from wishlist."""
        self._load_entry()
        self.exists = False if self.block == '' else True
        return self.exists
    
    def _load_entry(self):
        """ 
        Meat and potatoes. The secret sauce. The reason for the season (get it? cuz wishlist? santapls?)
        Never call this directly... probably. Use self._check_exists() instead.
        TODO: wrap in try/catch, which calls self._cleanup() on exception

        ASSUMPTIONS:
        - self.md_file exists
        - self.entry_regex_ is valid (TODO: move this OUT of constants)
        - fuck, what else...

        QUESTIONS:
        1. considering the importance, should this return anything? should _check_exists() ask more of this thing?
        """

        self.before = ''
        self.block = ''
        self.after = ''

        with open(self.md_file, 'r') as wl:
            append_output=False
            b4 = True
            after = False

            for line in wl:
                m = self.entry_regex_.match(line)
                if m and append_output:
                    after = True
                    append_output = False
                if append_output:
                    self.block += line
                if m and m.groups()[0] == self.name:
                    self.exists = True
                    self.block = line
                    b4 = False
                    append_output = True
                if b4:
                    self.before += line
                if after:
                    self.after += line

    def create(self):
        # whats the difference between below and 'if not self.block'?
        if self.exists:
            logger.error(f"Cannot create new entry '{self.name}' - already exists!")
            raise ValueError(f"Cannot create new entry '{self.name}' - already exists!")

        self._write_wishlist()
        self._write_block_to_prj_skel()
        self._commit()
        logger.debug(f"Created new entry '{self.name}'.")
        return self._check_exists()

    def pprint(self, raw=False, mdtext=''):
        if raw:
            print(self.block)
            return
        if mdtext == '':
            prettyprint_mdtext.format_mdtext(mdtext=self.block)

    def update(self, mdtext):
        self.block = mdtext
        self._write_wishlist()
        self._write_block_to_prj_skel()
        self._commit()
        logger.debug(f"Updated entry '{self.name}'.")


    def delete(self) -> bool:
        self._check_exists()
        if not self.exists:
            logger.warning(f"Could not delete entry '{self}': Does not exist.")
            raise ValueError(f"Could not delete entry '{self}': Does not exist.")
        self.block = ''
        self._write_wishlist()
        self._remove_prj_skel()
        logger.debug(f"Deleted entry '{self.name}'.")
        return not self._check_exists()

    def _write_wishlist(self):
        tmp_wl = tempfile.mktemp()
        b = 0
        with open(tmp_wl, 'w') as wl:
            b += wl.write(self.before)
            b += wl.write(self.block)
            b += wl.write(self.after)
        try:
            os.remove(self.md_file)
            shutil.copyfile(tmp_wl, self.md_file)
            logger.debug(f"Wrote {b} bytes to '{self.md_file}'.")
        except Exception as e:
            logger.critical(f"Could not replace existing wishlist file '{self.md_file}': {e}")
        finally:
            os.remove(tmp_wl)

    def _commit(self, msg='', push=False):
        """
        Commit changes to git and push
        """
        return
        if msg == '':
            msg = "Committing change..."
            logger.warning(f"Using generic commit message...")
        self.repo.index.add(str(self.md_file))
        self.repo.index.add(str(self.readme))
        self.repo.index.commit(message=msg)
        if push:
            remote = self.repo.remote()
            remote.push()


# old code


def _remove_prj_skel(self):
    try:
        rmtree(self.prj_path)
        logger.debug(f"Removed project {self.prj_path} for entry '{self.name}'")
        return
    except FileNotFoundError as e:
        logger.warning(f"Wish '{self.name}' has no associated project to delete!")
        return

def _write_block_to_prj_skel(self):
    self.prj_path.mkdir(parents=True, exist_ok=True)
    with open(self.readme, 'w') as sk:
        b = sk.write(self.block)
    logger.debug(f"Wrote {b} bytes to '{self.readme}' for entry '{self.name}'.")

