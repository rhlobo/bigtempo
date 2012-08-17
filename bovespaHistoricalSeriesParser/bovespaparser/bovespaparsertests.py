import unittest
from functools import partial
import bovespaparser as parser


DATAHEADER = "00COTAHIST.2012BOVESPA 20120808                                                                                                                                                                                                                      "
DATAFOOTER = "99COTAHIST.2012BOVESPA 2012080800000197525                                                                                                                                                                                                           "


class TestBovespaParserFunctions(unittest.TestCase):

    def parsingshouldignoreheaderandfooter(self, func):
        data = [DATAHEADER, DATAFOOTER]
        result = func(data)
        self.assertEqual(len(result), 0)

    def test_parsestocksdata_shouldignoreheaderandfooter(self):
        self.parsingshouldignoreheaderandfooter(parser.parsestocksdata)

    def test_parsedata_shouldignoreheaderandfooter(self):
        self.parsingshouldignoreheaderandfooter(parser.parsedata)

    def parsingshouldreturncorrectnumberofrecords(self, func):
        result = func("TESTDATAFILE.TXT")
        self.assertEqual(len(result), 18)

    def test_parsestocksfile_shouldreturncorrectnumberofrecords(self):
        self.parsingshouldreturncorrectnumberofrecords(parser.parsestocksfile)

    def test_parsefile_shouldreturncorrectnumberofrecords(self):
        self.parsingshouldreturncorrectnumberofrecords(parser.parsefile)

if __name__ == '__main__':
    unittest.main()
