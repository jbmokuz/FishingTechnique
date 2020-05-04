import unittest
from functions import GameInstance

class TestSinglton(unittest.TestCase):

    def testMultiple(self):
        gi = GameInstance()
        gi2 = GameInstance()
        
        gi.reset()
        gi2.reset()

        gi.waiting.append("A")
        gi2.waiting.append("B")

        self.assertTrue("B" in gi.waiting)
        self.assertTrue("B" in gi2.waiting)
        self.assertTrue("A" in gi.waiting)
        self.assertTrue("A" in gi2.waiting)
        self.assertFalse("C" in gi.waiting)
        self.assertFalse("C" in gi2.waiting)
                
class TestWaiting(unittest.TestCase):

    def setUp(self):
        self.gi = GameInstance()

    def testAddWaiting(self):
        self.gi.reset()
        self.assertEqual([str(i) for i in self.gi.waiting], [])
        self.gi.addWaiting("test")
        self.assertEqual([str(i) for i in self.gi.waiting], ["test"])
        self.gi.addWaiting("test")
        self.assertEqual([str(i) for i in self.gi.waiting], ["test"])
        self.gi.addWaiting("test2")
        self.assertEqual([str(i) for i in self.gi.waiting], ["test","test2"])        
        
    def testRemoveWaiting(self):
        self.gi.reset()
        self.assertEqual(self.gi.waiting, [])
        self.gi.addWaiting("test")
        self.gi.removeWaiting("test")
        self.assertEqual(self.gi.waiting, [])
        self.gi.addWaiting("1")
        self.gi.addWaiting("2")
        self.gi.addWaiting("3")
        self.gi.addWaiting("4")
        self.gi.removeWaiting("2")
        self.assertEqual([str(i) for i in self.gi.waiting], ["1","3","4"])
        self.gi.removeWaiting("3")
        self.assertEqual([str(i) for i in self.gi.waiting], ["1","4"])
        self.gi.addWaiting("5")
        self.assertEqual([str(i) for i in self.gi.waiting], ["1","4","5"])
        self.gi.removeWaiting("9")
        self.assertEqual([str(i) for i in self.gi.waiting], ["1","4","5"])

class TestGame(unittest.TestCase):

    def setUp(self):
        self.gi = GameInstance()

    def testShuffle(self):
        self.gi.reset()
        self.gi.addWaiting("1")
        self.gi.addWaiting("2")
        self.gi.addWaiting("3")
        self.gi.addWaiting("4")
        self.gi.addWaiting("5")
        self.gi.addWaiting("6")
        self.gi.addWaiting("7")
        self.gi.addWaiting("8")
        self.gi.addWaiting("9")
        ret1 = self.gi.shuffle()
        self.assertEqual(len(self.gi.waiting), 1)
        self.assertTrue(0 in self.gi.tables)
        self.assertTrue(1 in self.gi.tables)
        self.assertEqual(len(self.gi.tables[1].players), 4)
        ret2 = self.gi.shuffle()
        self.assertEqual(ret2,[])
        ret3 = self.gi.listPlaying()
        self.assertEqual([self.gi.tables[ret1[0]],self.gi.tables[ret1[1]]],ret3)

    def testReport(self):
        self.gi.reset()
        self.gi.addWaiting("1")
        self.gi.addWaiting("2")
        self.gi.addWaiting("3")
        self.gi.addWaiting("4")
        ret = self.gi.shuffle()
        self.assertEqual(self.gi.report("1","60000 +0"),1)
        self.assertEqual(self.gi.report("2","25000 +0"),1)
        self.assertEqual(self.gi.report("3","15000 +0"),1)
        self.assertEqual(self.gi.report("4","0 +0"),0)
        
    def testTable(self):
        self.gi.reset()
        self.gi.addTable("hello","0")
        self.gi.addTable("hello","0")
        self.gi.addTable("hello","0")
        self.assertEqual(self.gi.tables["0"].players,{'hello': None})
        self.gi.addTable("hello","0")
        self.gi.addTable("hello","1")
        self.gi.addTable("hello","2")
        self.assertEqual(self.gi.tables["0"].players,{'hello': None})
        self.assertEqual(len(self.gi.tables),1)
        self.gi.addTable("A","ATable")
        self.assertEqual(len(self.gi.tables),2)
        self.gi.addTable("B","ATable")
        self.gi.addTable("C","ATable")
        self.gi.addTable("D","ATable")
        self.assertEqual(self.gi.tables["ATable"].players,{'A': None, 'B': None, 'C': None, 'D': None})
        self.gi.addTable("E","ATable")
        self.assertEqual(self.gi.tables["ATable"].players,{'A': None, 'B': None, 'C': None, 'D': None})
        self.gi.remove("A")
        self.assertEqual(self.gi.tables["ATable"].players,{'B': None, 'C': None, 'D': None})
        self.gi.addTable("E","ATable")
        self.assertEqual(self.gi.tables["ATable"].players,{'E': None, 'B': None, 'C': None, 'D': None})


class TestScore(unittest.TestCase):
    
    def setUp(self):
        self.gi = GameInstance()
        
    def testReport(self):
        self.gi.reset()
        self.gi.addTable("1","A")
        self.gi.addTable("2","A")
        self.gi.addTable("3","A")
        self.gi.addTable("4","A")
        self.gi.report("2","25000 +0")
        print(self.gi.scoreTable("A"))
        print(self.gi.scoreTable("B"))        
        self.gi.report("3","60000 +0")        
        self.gi.report("1","15000 +0")
        self.gi.report("4","0 +1")
        print(self.gi.scoreTable("A"))
        self.gi.report("4","1 +0")
        print(self.gi.scoreTable("A"))
        self.gi.report("4","0 +0")
        print(self.gi.scoreTable("A"))        
        self.gi.report("3","60000 +0")        
        self.gi.report("1","15000 -1")
        self.gi.report("2","25000 +2")
        self.gi.report("4","0 +0")
        print(self.gi.scoreTable("A"))        
        self.gi.report("1","15000 -2")
        print(self.gi.scoreTable("A"))                
        #@TODO a good way to test this
        
if __name__ == '__main__':
    unittest.main()
