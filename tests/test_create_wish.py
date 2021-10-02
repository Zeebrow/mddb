import unittest
from random import randint
import shutil
from os.path import basename
from os import PathLike
from pathlib import Path
from mddb import Entry

class TestCreateEntry(unittest.TestCase):    

    def gen_temp_mddb(self, identifier: str):
        """
        Generates a temporary mddb (prj-skel directory and mddb.md)
        by copying a template
        """
        tempdir_name = f"{identifier}_{randint(1000,9999)}_repo"
        # for when run from repo's home
        basedir = Path(__file__).parent.resolve()
        newdir = basedir / tempdir_name
        shutil.copytree(Path(basedir/"fixture_repo"), newdir)
        return newdir

    def setUp(self):
        """ """
        self.this_repo = self.gen_temp_mddb(identifier="test_create")
        self.this_mddb = self.this_repo / "mddb.md"
        self.w1 = Entry("test1", repo_path=self.this_repo)
        self.w2 = Entry("test2", repo_path=self.this_repo)
        self.w3 = Entry("test3", repo_path=self.this_repo)
        self.w4 = Entry("test4", repo_path=self.this_repo)

    def tearDown(self):
        shutil.rmtree(self.this_repo)
        
    def test_entry_doesnt_exist_until_create(self):
        """Not an attribute test, since depends on success of create()"""
        new_w5 = Entry("new_entry_5", repo_path=self.this_repo)
        self.assertFalse(new_w5.exists)
        new_w5.create()
        self.assertTrue(new_w5.exists)
    
    def test_create_raises_on_fail(self):
        """TODO
        Decide what constitutes 'failure to create entry' - fail to write file?
        fail to git commit?
        ???
        """
        pass

    def test_create_entry_name_is_configurable(self):
        """this might be a frivolous test"""
        rand_entryname = f"new_entry_{randint(1000,9999)}"
        new_w5 = Entry(rand_entryname, repo_path=self.this_repo)
        self.assertEqual(new_w5.name, rand_entryname)

    def test_entry_attributes(self):
        return
        """TODO: not exclusive to 'Entry().create()', needs to move"""
        new_w5 = Entry("new_entry_5", repo_path=self.this_repo)
        self.assertEqual(new_w5.repo_path, self.this_repo)
        self.assertEqual(new_w5.prj_path, self.entry_prj_base_dir)
        self.assertEqual(new_w5.readme, self.entry_readme)
        self.assertIsInstance(new_w5.prj_path, PathLike)

    def test_create_entry_name_equals_prj_skel_dir_name(self):
        """
        Changes to how directories and files are named should fail tests
        """
        new_w5 = Entry("new_entry_5", repo_path=self.this_repo)
        new_w5.create()
        self.assertEqual(new_w5.name, basename(new_w5.prj_path))

    def test_create_entry_creates_prj_skel(self):
        """Test for README.md"""
        entryname = "new_entry_5"
        new_w5 = Entry(entryname, repo_path=self.this_repo)
        self.assertFalse(Path(self.this_repo / "prj-skel" / entryname / "README.md").exists())
        new_w5.create()
        self.assertTrue(Path(self.this_repo / "prj-skel" / entryname / "README.md").exists())

    def test_created_entry_block_equals_prj_readme(self):
        new_w5 = Entry("new_entry_5", repo_path=self.this_repo)
        new_w5.create()
        with open(new_w5.readme, 'r') as md:
            self.assertEqual(new_w5.block, md.read())
    
    def test_create_entry_appends_to_mddb_non_destructively(self):
        with open(self.this_mddb, 'r') as wl:
            before_create = wl.read()
        new_w5 = Entry("new_entry_5", repo_path=self.this_repo)
        new_w5.create()
        with open(self.this_mddb, 'r') as wl:
            after_create = wl.read()
        self.assertEqual(len(before_create), len(after_create) - len(new_w5.block))
    
    # def test_create_on_existing_entry_throws(self):
    #     self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
