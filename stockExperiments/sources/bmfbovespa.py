import urllib
import re


class SymbolImporter(object):

    def __init__(self):
        self.regex = re.compile(r'<span\s+id="ctl00_contentPlaceHolderConteudo_grdResumoCarteiraTeorica_ctl00_ctl\d+_lblCodigo".*?>([\w\d]+)</span>', re.IGNORECASE | re.DOTALL | re.MULTILINE)
        self.s_urlTemplate = 'http://www.bmfbovespa.com.br/indices/ResumoCarteiraTeorica.aspx?=%s&idioma=pt-br'

    def import_symbols(self, s_index):
        data = urllib.urlencode({"Indice": s_index})
        s_content = urllib.urlopen(self.s_urlTemplate % data)
        return re.findall(self.regex, s_content)
