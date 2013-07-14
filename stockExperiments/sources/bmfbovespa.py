# -*- coding: utf-8 -*-


import urllib
import re


class SymbolImporter(object):

    def __init__(self):
        self.regex = re.compile(r'<span\s+id="ctl00_contentPlaceHolderConteudo_grdResumoCarteiraTeorica_ctl00_ctl\d+_lblCodigo".*?>([\w\d]+)</span>', re.IGNORECASE | re.DOTALL | re.MULTILINE)
        self.s_urlTemplate = 'http://www.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?%s&idioma=pt-br'

    def import_symbols(self, s_index):
        """
        s_index is a string representing a stock index. Examples include:
        - IBovespa, IBrX50, IBrX, IBrA, MLCX, SMLL, IVBX, IDIV, IEE, INDX, ICON, IMOB, IFNC, IMAT, UTIL, ...
        The complete list of available stock indexes can be found at 'http://www.bmfbovespa.com.br/indices/BuscarIndices.aspx?idioma=pt-br'
        """
        data = urllib.urlencode({"Indice": s_index})
        s_content = urllib.urlopen(self.s_urlTemplate % data).read()
        return re.findall(self.regex, s_content)
