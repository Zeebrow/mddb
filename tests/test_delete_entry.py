import unittest
from random import randint
import shutil
import os
from os.path import basename
from pathlib import Path
from mddb import Entry

class TestDeleteEntry(unittest.TestCase):    
    
    """
    Assumes test_create_entry.py passes
    """

    # def gen_tempdir_name(self, identifier: str) -> str:
    #     return f"{identifier}_{randint(1000,9999)}"

    def gen_temp_mddb(self, identifier: str):
        tempdir_name = f"{identifier}_{randint(1000,9999)}_repo"
        # for when run from repo's home
        basedir = Path(__file__).parent.resolve()
        newdir = basedir / tempdir_name
        shutil.copytree(Path(basedir/"fixture_repo"), newdir)
        return newdir

    def setUp(self):
        """ """
        self.this_repo = self.gen_temp_mddb(identifier="test_delete")
        self.w1 = Entry("test1", repo_path=self.this_repo)
        self.w2 = Entry("test2", repo_path=self.this_repo)
        self.w3 = Entry("test3", repo_path=self.this_repo)
        self.w4 = Entry("test4", repo_path=self.this_repo)

        # self.mddb = self.this_repo / "mddb.md"
        # print(get_wishes(mddb_file=self.mddb))
        # self.w = Entry(wishname=self.wishname, 
        #        repo_path=self.this_repo)
        # self.wish_prj_base_dir = self.this_repo / "prj-skel" / self.wishname
        # self.wish_readme = self.wish_prj_base_dir / "README.md"

    def tearDown(self):
        shutil.rmtree(self.this_repo)

#    def test_del_entry_removes_prj_dir(self):
#        self.assertTrue(self.w3.prj_path.exists())
#        self.w3.delete()
#        self.assertFalse(self.w3.prj_path.exists())


    def test_del_entry_doesnt_affect_other_entryes_in_wl(self):

        entryname = "some_entry"

        w0 = Entry(entryname=f"pre_{entryname}", repo_path=self.this_repo)
        w0.create()

        w1 = Entry(entryname=f"delme_{entryname}", repo_path=self.this_repo)
        w1.create()

        w2 = Entry(entryname=f"post_{entryname}", repo_path=self.this_repo)
        w2.create()

        deleted_block = w1.block
        w1.delete()
        with open(self.this_repo/"mddb.md",'r') as wl:
            wl_as_string = wl.read()

        self.assertIn(w0.block, wl_as_string)
        self.assertNotIn(deleted_block, wl_as_string)
        self.assertIn(w2.block, wl_as_string)

    def test_del_entry_(self):
        pass


if __name__ == '__main__':
    unittest.main()
