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
        print(newdir)
        return newdir
    
    def setUp(self):
        """ """
        self.this_repo = self.gen_temp_mddb(identifier="test_create")
        self.this_mddb = self.this_repo / "mddb.md"
        self.w1 = Entry("test-commit-entry-1", repo_path=self.this_repo)
        self.w1.create()

    def tearDown(self):
        shutil.rmtree(self.this_repo)
        
    def test_commit_adds_target_repo(self):
        pass

if __name__ == '__main__':
    unittest.main()
