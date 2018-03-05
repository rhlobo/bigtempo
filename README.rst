
.. image:: https://img.shields.io/pypi/v/bigtempo.svg
        :target: https://pypi.python.org/pypi/bigtempo

.. image:: https://img.shields.io/pypi/dm/bigtempo.svg
        :target: https://pypi.python.org/pypi/bigtempo

.. image:: https://travis-ci.org/rhlobo/bigtempo.png?branch=master
        :target: https://travis-ci.org/rhlobo/bigtempo

.. image:: https://coveralls.io/repos/rhlobo/bigtempo/badge.png
        :target: https://coveralls.io/r/rhlobo/bigtempo

.. image:: http://rhlobo.github.io/bigtempo/bigtempo_small.png


:Implementation: Python 2.7
:Status: Alpha (contract may change)
:Download: http://pypi.python.org/pypi/bigtempo/
:Source: http://github.com/rhlobo/bigtempo/
:Keywords: bigdata, time series, temporal processment, temporal analysis, data processment, data analysis, scalable, distributed, data exploration, python


This is a Python package created to help you build complex hierarchies of processments, each refered as a datasource.
The package was originally conceived to handle temporal data and it is typically used as a colleague of pandas_ - dealing with time series and dataframes - but it is flexible and can easily be extended to support other data models.
It handles dependency resolution, provides a tagging system that enables querying operations over datasource sets, and much more.

There are other software packages that focus on lower level aspects of data processing, like pandas_, numpy_, sympy_, theano_.
This is not a framework to replace these. Instead, it aims to support many of these tools, helping you to stitch many processments together.
It provides a decoupled programming model that was built with scalability support in its heart and it takes care of a lot of the workflow management so that you can focus on the data itself.

Bigtempo aims to provide support an wide range of applications - including artificial intelligence systems - working in data pull fashion.
Its philosophy is to lazyload things as possible: analysis are retrieved from cache if available, processed otherwise.
A `datasource` serves data through processors that can be used by other `datasources` (or by you directly) and processors are made to be executed in a distributed fashion, if that is desired.

.. It is here to address the plumbing associated with complex chained data evaluation processes, and because each datasource can be used as input for new datasources, it is ideal for data exploration and analysis.
.. Using it, you are able - for instance - to easily spawn multiple variations of a processment over sets of other datasources.
.. It is a great tool for distributed processment when you have 'a few quadrillion' [interdependent] processments for interdependent data sets.

+--------------------------------------------------------------------------------------+
| Keep in mind that the package - although performatic - is in Alpha Stage and, as so, |
| most of its caching and distributed processing capabilities are still in the owen.   |
+--------------------------------------------------------------------------------------+


Getting started
---------------

You can `get started reading an ipython notebook`_, and for a better understandment of what can be done, you shall take a peek in the `pandas introduction`_.


Example project
^^^^^^^^^^^^^^^

If you need more examples, or just feel like checking out how bigtempo can be used in a project, please refer to stockExperiments_.


Installation
------------

To install, simply:

.. code-block:: bash

    $ pip install bigtempo

Or, if you absolutely must:

.. code-block:: bash

    $ easy_install bigtempo


Dependencies
^^^^^^^^^^^^

    Both the installation methods above should take care of dependencies on its own, automatically.


The pandas_ library is the only direct dependency the package has in order to be executed. You should visit its page to find out what it depends on. For best results, we recommend installing optional packages as well.

If you want to run the package tests, or enjoy its testing facilities, you'll need:

- mockito_ >= 0.5.1

In order to run the tests using the command contained in the ``bin`` directory, also install:

- nose >= 1.3.0
- coverage >= 3.6
- pep8 >= 1.4.5

    At `bin/docker_base` you can find a script named `setup-ubuntu_14.04_x64.sh` that is able to prepare an Ubuntu (Trusty Tahr) machine with pandas and all of its dependencies. It is originally mean to be used to build the project's docker image but it should work on real machines.


Installing from source
^^^^^^^^^^^^^^^^^^^^^^

To install bigtempo from source you need:

Clone the git repository:

.. code-block:: bash

    $ git clone https://github.com/rhlobo/bigtempo.git

Get into the project directory:

.. code-block:: bash

    $ cd bigtempo

Install dependencies (if you are not using virtualenv, it may need super user privileges):

.. code-block:: bash

    $ pip install -r requirements.txt

Install it:

.. code-block:: bash

    $ python setup.py install

Alternatively, you can use `pip` if you want all the dependencies pulled in automatically (the optional ``-e`` option is for installing it in
`development mode <http://www.pip-installer.org/en/latest/usage.html>`__):

.. code-block:: bash

    $ pip install -e .


Next versions?
--------------

.. Although this is an open source project, some of its next big features are going to be released publicly only when they are better defined.
.. This measure will be valid and applyed til the project achieves a Beta development stage. Feel free to get in contact if you want to know more about it.

Distributed processing

- Build in process pools
- Integration with celery_
- Integration with Apache ZooKeeper and ZeroMQ

Caching

- Smart temporal data caching

Compatibility

- Python 2.7+


Bug tracker
-----------

If you have any suggestions, bug reports or annoyances please report them to our issue_tracker_.


Contribute
----------

1. On the tracker_, check for open issues or open a new one to start a discussion around an idea or bug.
2. Fork the repository_ on GitHub to start making your changes.
3. Write a test which shows that the bug was fixed or that the feature works as expected.
4. Send a pull request and wait until it gets merged and published. Make sure to add yourself to AUTHORS_.


.. _pandas: http://pandas.pydata.org
.. _`pandas introduction`: http://pandas.pydata.org/pandas-docs/dev/dsintro.html
.. _numpy: http://www.numpy.org/
.. _sympy: http://sympy.org/
.. _theano: http://deeplearning.net/software/theano/
.. _mockito: https://pypi.python.org/pypi/mockito
.. _celery: http://github.com/celery/celery
.. _stockExperiments: https://github.com/rhlobo/stockExperiments
.. _issue_tracker: http://github.com/rhlobo/bigtempo/issues
.. _tracker: http://github.com/rhlobo/bigtempo/issues
.. _repository: http://github.com/rhlobo/bigtempo
.. _AUTHORS: https://github.com/rhlobo/bigtempo/blob/master/AUTHORS.rst
.. _`get started reading an ipython notebook`: http://nbviewer.ipython.org/urls/raw.github.com/rhlobo/bigtempo/master/ipy-notebooks/getting_started.ipynb



--------------------------------------------------------------

.. image:: https://d2weczhvl823v0.cloudfront.net/rhlobo/bigtempo/trend.png
   :target: https://bitdeli.com/free

.. image:: https://cruel-carlota.pagodabox.com/72a329aaa141ddda4059d84df6c4d9ea
    :target: https://githalytics.com/rhlobo/bigtempo
