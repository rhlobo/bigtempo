import json


CANDLESTICK, COLUMN = 'candlestick', 'column'
GROUPING_UNITS = [['week', [1]], ['month', [1, 2, 3, 4, 6]]]


class HighChartsOptions(object):

    def asDict(self):
        return self.asDict


class OptionBuilder(HighChartsOptions):

    def __init__(self, title='ipyghstocks'):
        self.asDict = {

            'chart': {

                'renderTo': '',

                'alignTicks': False
            },

            'rangeSelector': {

                'selected': 1
            },

            'title': {
                'text': title
            },

            'plotOptions': {

                'candlestick': {

                    'color': 'red',

                    'upColor': 'blue'
            }
        },

            'yAxis': [],

            'series': []
        }

    def json(self, renderTo):
        self.asDict['chart']['renderTo'] = renderTo
        return json.dumps(self, cls=HighChartsOptionsJSONEncoder)

    def add(self, obj):
        if not isinstance(obj, HighChartsOptions):
            raise ValueError
        self.asDict[('yAxis' if isinstance(obj, Axis) else 'series')].append(obj)
        return self


class Axis(HighChartsOptions):

    def __init__(self, name, height=300, lineWidth=2):
        self.asDict = {

            'title':  {

                'text': name
            },

            'height': height,

            'lineWidth': lineWidth,
        }


class Series(HighChartsOptions):

    def __init__(self, name, data, chartType=CANDLESTICK, yAxisIndex=0, dataGroupingUnits=GROUPING_UNITS):
        self.asDict = {

            'type': chartType,

            'name': name,

            'data': data,

            'yAxis': yAxisIndex,

            'dataGrouping': {

                'units': dataGroupingUnits
            }
        }


class HighChartsOptionsJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, HighChartsOptions):
            return obj.asDict
        return json.JSONEncoder.default(self, obj)
