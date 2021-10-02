import unittest
import logging
from random import randint
import shutil
from pathlib import Path
from mddb import get_entries
from mddb import Entry
import subprocess

logger = logging.getLogger()
f = logging.Formatter('%(asctime)s : %(name)s : %(funcName)s : %(levelname)s: %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(f)
logger.addHandler(sh)
logger.setLevel(logging.DEBUG)

class TestListEntries(unittest.TestCase):
    
    """
    Assumes test_[create|del|update]_entry.py succeed
    """

    def new_test_entryname(self) -> str:
        return f"./test_entry_{randint(1000,9999)}"

    def make_fresh_mddb(self, entryname: str):
        newdir = Path(entryname + "_repo")
        shutil.copytree(Path("./fixture_repo"), newdir)
        return newdir

    def setUp(self):
        self.entryname = self.new_test_entryname()
        self.this_repo = self.make_fresh_mddb(
                entryname=self.entryname)
        self.mddb = self.this_repo / "mddb.md"

    def tearDown(self):
        shutil.rmtree(self.this_repo)

    def test_list_entries(self):
        self.assertIsInstance(
                get_entries(mddb_file=self.mddb), list)
        self.assertEqual(
                get_entries(mddb_file=self.mddb)[0], "test1")

    def test_get_entries_after_create_entry(self):
        w = Entry(entryname=self.entryname, repo_path=self.this_repo)
        self.assertNotIn("new_entry_1", get_entries(mddb_file=self.mddb))
        w.create()
        self.assertIn(
                self.entryname, 
                get_entries(mddb_file=self.mddb))

    def test_get_entries_after_delete_entry(self):
        self.assertTrue(False)

    def test_get_entries_after_edit_entry(self):
        self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
