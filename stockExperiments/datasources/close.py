import pandas

from instances import data_engine


@data_engine.for_synched(data_engine.select('STOCK_TICKS'))
def _datasource_factory(source_reference):

    @data_engine.datasource('CLOSE:%s' % (source_reference),
                            dependencies=[source_reference],
                            tags=['CLOSE'])
    class Close(object):

        def evaluate(self, context, symbol, start=None, end=None):
            df_source = context.dependencies(source_reference)

            result = pandas.DataFrame(columns=['close'], index=df_source.index)
            result['value'] = df_source['close']

            return result
