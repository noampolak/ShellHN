import pytest
from .ShellHN import *

class TestHNClass:

    def test_ident(self):
        ident = createIdent(10)
        assert(len(ident) == 10)

    def test_get_aricle_item_by_rank(self):
        item = getArticleItemByRank(10)
        assert item != None, "There should be rank of 10"
        item = getArticleItemByRank(30)
        assert item != None, "There should be rank of 30"
        item = getArticleItemByRank(100)
        assert item != None, "There should be rank of 100"

        item = getArticleItemByRank(999)
        assert item == None, "There shouldn't be rank of 999"