import unittest
from functions import GameInstance

class TestSinglton(unittest.TestCase):

    def testMultiple(self):
        gi = GameInstance()
        gi2 = GameInstance()

        gi.waiting.append("A")
        gi2.waiting.append("B")

        self.assertTrue("B" in gi.waiting)
        self.assertTrue("B" in gi2.waiting)
        self.assertTrue("A" in gi.waiting)
        self.assertTrue("A" in gi2.waiting)
        self.assertFalse("C" in gi.waiting)
        self.assertFalse("C" in gi2.waiting)
        
        

class TestGameSetup(unittest.TestCase):

    def setUp(self):
        self.gi = GameInstance()

    def testAddWaiting(self):
        self.gi.clearWaiting()
        self.assertEqual(self.gi.waiting, [])
        self.gi.addWaiting("test")
        self.assertNotEqual(self.gi.waiting, [])
        
    def testClearWaiting(self):
        self.gi.clearWaiting()
        self.gi.addWaiting("test")
        self.gi.clearWaiting()
        self.assertEqual(self.gi.waiting, [])
    
    def testRemoveWaiting(self):
        self.gi.clearWaiting()
        self.assertEqual(self.gi.waiting, [])
        self.gi.addWaiting("test")
        self.gi.removeWaiting("test")
        self.assertEqual(self.gi.waiting, [])
        self.gi.addWaiting("1")
        self.gi.addWaiting("2")
        self.gi.addWaiting("3")
        self.gi.addWaiting("4")
        self.gi.removeWaiting("2")
        self.assertEqual(self.gi.waiting, ["1","3","4"])
        self.gi.removeWaiting("3")
        self.assertEqual(self.gi.waiting, ["1","4"])
        self.gi.addWaiting("5")
        self.assertEqual(self.gi.waiting, ["1","4","5"])
        self.gi.removeWaiting("9")
        self.assertEqual(self.gi.waiting, ["1","4","5"])

if __name__ == '__main__':
    unittest.main()
