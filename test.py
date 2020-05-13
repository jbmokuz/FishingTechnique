import unittest
from functions import *
        

class TestParse(unittest.TestCase):

    
    def setUp(self):
        pass

    def testReport(self):
        for p in parseGame("2020051311gm-0209-19713-a50611a9", TENGO):
            print(p)
        for p in parseGame("https://tenhou.net/0/?log=2020051311gm-0209-19713-a50611a9&tw=1", TENPIN):
            print(p)


if __name__ == '__main__':
    unittest.main()
