import urllib
import re


class SymbolImporter(object):

    def __init__(self):
        self.regex = re.compile(r'<span\s+id="ctl00_contentPlaceHolderConteudo_grdResumoCarteiraTeorica_ctl00_ctl\d+_lblCodigo".*?>([\w\d]+)</span>', re.IGNORECASE | re.DOTALL | re.MULTILINE)
        self.s_urlTemplate = 'http://www.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?Indice=%s&idioma=pt-br'

    def import_symbols(self, s_index):
        return re.findall(self.regex, self.s_urlTemplate % (s_index))
