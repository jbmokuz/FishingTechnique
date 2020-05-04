import unittest
from functions import GameInstance, TENSAN, TENGO, TENPIN

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
                
class TestTable(unittest.TestCase):

    def setUp(self):
        self.gi = GameInstance()

    def testAddTable(self):
        self.gi.reset()
        self.assertEqual(self.gi.tables, {})
        self.assertEqual(self.gi.addTable("player1", "tableA"),0)
        self.assertEqual(self.gi.addTable("player1", "tableB"),1)
        print(self.gi.lastError)
        self.assertEqual(self.gi.addTable("player2", "tableA",TENPIN),1)
        print(self.gi.lastError)
        self.assertEqual(self.gi.addTable("player2", "tableA",TENSAN),0)
        self.assertEqual(self.gi.addTable("player3", "tableA"),0)
        self.assertEqual(self.gi.addTable("player4", "tableA"),0)
        self.assertEqual(self.gi.addTable("player5", "tableA"),1)
        print(self.gi.lastError)        
                
    def testRemoveTable(self):
        self.gi.reset()
        self.assertEqual(self.gi.tables, {})
        self.assertEqual(self.gi.remove("player1"),1)
        print(self.gi.lastError)
        self.assertEqual(self.gi.addTable("player1","tableA"),0)
        self.assertEqual(len(self.gi.tables["tableA"].players),1)
        self.assertEqual(self.gi.addTable("player2","tableA"),0)
        self.assertEqual(self.gi.addTable("player3","tableA"),0)
        self.assertEqual(self.gi.addTable("player4","tableA"),0)
        self.assertEqual(len(self.gi.tables["tableA"].players),4)
        self.assertEqual(self.gi.remove("player2"),0)
        self.assertEqual(self.gi.tables["tableA"].players, {'player1': None, 'player3': None, 'player4': None})
        

class TestGame(unittest.TestCase):

    def setUp(self):
        self.gi = GameInstance()

    def testReport(self):
        self.gi.reset()
        self.assertEqual(self.gi.report("player1","60000+0"),1)
        print(self.gi.lastError)
        self.assertEqual(self.gi.addTable("player1","tableA"),0)
        self.assertEqual(self.gi.addTable("player2","tableA"),0)
        self.assertEqual(self.gi.addTable("player3","tableA"),0)
        self.assertEqual(self.gi.addTable("player4","tableA"),0)
        self.assertEqual(self.gi.report("player1",""),1)
        print(self.gi.lastError)
        self.assertEqual(self.gi.report("player1","weiorjw"),1)
        print(self.gi.lastError)
        self.assertEqual(self.gi.report("player1","+0"),1)
        print(self.gi.lastError)
        self.assertEqual(self.gi.report("player1","60000"),1)
        print(self.gi.lastError)
        self.assertEqual(self.gi.report("player1","60000+0"),1)
        print(self.gi.lastError)
        self.assertEqual(self.gi.report("player1","60000 +0"),0)
        self.assertEqual(self.gi.report("player2","25000 +0"),0)
        self.assertEqual(self.gi.report("player3","+15000 +0"),0)
        self.assertEqual(self.gi.report("player4","0 +0"),0)

    def testScore(self):
        self.gi.reset()
        self.assertEqual(self.gi.addTable("player1","tableA"),0)
        self.assertEqual(self.gi.addTable("player2","tableA"),0)
        self.assertEqual(self.gi.addTable("player3","tableA"),0)
        self.assertEqual(self.gi.scoreTable("A"),1)
        print(self.gi.lastError)
        self.assertEqual(self.gi.scoreTable("tableA"),1)
        print(self.gi.lastError)
        self.assertEqual(self.gi.addTable("player4","tableA"),0)
        self.assertEqual(self.gi.report("player1","60000 +0"),0)
        self.assertEqual(self.gi.report("player2","25000 +0"),0)
        self.assertEqual(self.gi.report("player3","+15000 +0"),0)
        self.assertEqual(self.gi.scoreTable("tableA"),1)
        print(self.gi.lastError)

        self.assertEqual(self.gi.report("player4","0 +1"),0)
        self.assertEqual(self.gi.scoreTable("tableA"),1)
        print(self.gi.lastError)

        self.assertEqual(self.gi.report("player4","1 +0"),0)
        self.assertEqual(self.gi.scoreTable("tableA"),1)
        print(self.gi.lastError)

        self.assertEqual(self.gi.report("player4","0 +0"),0)
        self.assertEqual(type(self.gi.scoreTable("tableA")),type(""))
        print(self.gi.scoreTable("tableA"))

        self.assertEqual(self.gi.report("player2","25000 +2"),0)
        self.assertEqual(self.gi.report("player3","+15000 -2"),0)
        self.assertEqual(type(self.gi.scoreTable("tableA")),type(""))
        print(self.gi.scoreTable("tableA"))

        self.assertEqual(self.gi.setTableRate("tableB",TENPIN),1)
        print(self.gi.lastError)

        self.assertEqual(self.gi.setTableRate("tableA",""),1)
        print(self.gi.lastError)

        self.assertEqual(self.gi.setTableRate("tableA",TENPIN),0)
        print(self.gi.scoreTable("tableA", True))


if __name__ == '__main__':
    unittest.main()
