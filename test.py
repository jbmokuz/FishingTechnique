import unittest
from functions import *




class TestWaiting(unittest.TestCase):
    
    def setUp(self):
        self.gi = GameInstance()

    def testAddWaiting(self):
        self.gi.reset()
        self.assertEqual([str(i) for i in self.gi.waiting], [])
        self.assertEqual(self.gi.addWaiting("test"),0)
        self.assertEqual([str(i) for i in self.gi.waiting], ["test"])
        self.assertEqual(self.gi.addWaiting("test"),1)        
        self.assertEqual([str(i) for i in self.gi.waiting], ["test"])
        self.assertEqual(self.gi.addWaiting("test2"),0)
        self.assertEqual([str(i) for i in self.gi.waiting], ["test","test2"])        
        
    def testRemoveWaiting(self):
        self.gi.reset()
        self.assertEqual(self.gi.waiting, [])
        self.assertEqual(self.gi.addWaiting("test"),0)
        self.assertEqual(self.gi.removeWaiting("test"),0)
        self.assertEqual(self.gi.waiting, [])
        self.gi.addWaiting("1")
        self.gi.addWaiting("2")
        self.assertEqual(self.gi.addWaiting("3"),0)
        self.assertEqual(self.gi.addWaiting("3"),1)
        self.gi.addWaiting("4")
        self.assertEqual(self.gi.removeWaiting("2"),0)
        self.assertEqual([str(i) for i in self.gi.waiting], ["1","3","4"])
        self.assertEqual(self.gi.removeWaiting("3"),0)
        self.assertEqual([str(i) for i in self.gi.waiting], ["1","4"])
        self.assertEqual(self.gi.addWaiting("5"),0)
        self.assertEqual([str(i) for i in self.gi.waiting], ["1","4","5"])
        self.assertEqual(self.gi.removeWaiting("9"),1)
        self.assertEqual([str(i) for i in self.gi.waiting], ["1","4","5"])

class TestGame(unittest.TestCase):

    def setUp(self):
        self.gi = GameInstance()

    def testShuffle(self):
        self.gi.reset()
        self.assertFalse(self.gi.addWaiting("1"))
        self.gi.addWaiting("2")
        self.assertEqual(self.gi.shuffle(),{})
        self.assertEqual(self.gi.waiting,["1","2"])
        self.gi.addWaiting("3")
        self.gi.addWaiting("4")
        self.gi.addWaiting("5")
        self.gi.addWaiting("6")
        self.gi.addWaiting("7")
        self.gi.addWaiting("8")
        self.gi.addWaiting("9")
        ret1 = self.gi.shuffle()
        self.assertEqual(len(self.gi.waiting), 1)
        self.assertEqual(len(ret1[1]), 4)
        ret2 = self.gi.shuffle()
        self.assertEqual(ret2,{})

class TestParse(unittest.TestCase):
    
    def setUp(self):
        pass

    def testReport(self):
        for p in parseGame("https://tenhou.net/0/?log=2020051311gm-0209-19713-a50611a9&tw=1", TENPIN):
            print(p)


if __name__ == '__main__':
    unittest.main()
