#!/usr/bin/python
# Filename: bovespaparsertests.py


import unittest
import bovespaparser as parser


DATAHEADER = "00COTAHIST.2012BOVESPA 20120808                                                                                                                                                                                                                      "
DATAFOOTER = "99COTAHIST.2012BOVESPA 2012080800000197525                                                                                                                                                                                                           "
DATARECORD = "012012010202ABCB4       010ABC BRASIL  PN  EJ  N2   R$  000000000122100000000012440000000001175000000000119400000000011850000000001185000000000119300465000000000000131800000000000157420100000000000000009999123100000010000000000000BRABCBACNPR4117"


class TestBovespaParserFunctions(unittest.TestCase):

    def parsingshouldignoreheaderandfooter(self, func):
        data = [DATAHEADER, DATAFOOTER]
        result = func(data)
        self.assertEqual(len(result), 0)

    def test_parsestocksdata_shouldignoreheaderandfooter(self):
        self.parsingshouldignoreheaderandfooter(parser.parsestocksdata)

    def test_parsedata_shouldignoreheaderandfooter(self):
        self.parsingshouldignoreheaderandfooter(parser.parsedata)

    def parsingshouldreturncorrectnumberofrecords(self, func, nr):
        result = func("TESTDATAFILE.TXT")
        self.assertEqual(len(result), nr)

    def test_parsestocksfile_shouldreturncorrectnumberofrecords(self):
        self.parsingshouldreturncorrectnumberofrecords(parser.parsestocksfile, 18)

    def test_parsefile_shouldreturncorrectnumberofrecords(self):
        self.parsingshouldreturncorrectnumberofrecords(parser.parsefile, 18)

    def assertcorrectreturnvalues(self, func, values):
        data = [DATAHEADER, DATARECORD, DATAFOOTER]
        result = func(data)
        self.assertEqual(len(result), 1)
        self.assertEqual(len(result[0]), 7)
        self.assertEqual(result[0], values)

    def test_parsestocksdata_resultvalues(self):
        self.assertcorrectreturnvalues(parser.parsestocksdata, ['ABCB4', '20120102', 12.21, 11.75, 12.44, 11.85, 157420100])

    def test_parsedata_resultvalues(self):
        self.assertcorrectreturnvalues(parser.parsedata, ['20120102', 'ABCB4       ', '0000000001221', '0000000001244', '0000000001175', '0000000001185', '000000000157420100'])

if __name__ == '__main__':
    unittest.main()
