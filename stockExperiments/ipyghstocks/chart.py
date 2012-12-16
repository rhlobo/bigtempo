# *-* encoding: UTF-8 *-*

from IPython.display import HTML as export
import random
import string
from ipyghstocks import options as options


def plot(configuration):
    cid = _generate_id()
    html = (
            _generate_html(cid) +
            _generate_javascript(cid, configuration.json(cid) if isinstance(configuration, options.OptionBuilder) else configuration) +
            _importLibs(cid)
           )
    return export(html)


def _generate_id():
    return 'x%030x' % random.randrange(256 ** 15)


def _generate_html(container_id):
    return '<div id="%s" style="min-height: 500px; min-width: 500px; border: 1px solid gray;"></div>​' % (container_id)


def _generate_javascript(container_id, code):
    return string.Template('''
                            <script>
                                function draw${cid}() {
                                    window.chart = new Highcharts.StockChart(${code});
                                }
                            </script>
                           ''').substitute(cid=container_id, code=code)


def _importLibs(container_id):
    return '''
            <script>
                $.getScript("http://code.highcharts.com/stock/highstock.src.js", function(script, textStatus, jqXHR) {
                    $.getScript("http://code.highcharts.com/stock/modules/exporting.js", function(script, textStatus, jqXHR) {
                        draw%s();
                    });
                });
            </script>
           ''' % (container_id)
