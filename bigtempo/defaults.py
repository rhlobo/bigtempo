# -*- coding: utf-8 -*-


import bigtempo.processors.dataframe_task as task


def sample_datasource_factory(cls):
    return cls()


datasource_factory = sample_datasource_factory
task_factory = task.factory
