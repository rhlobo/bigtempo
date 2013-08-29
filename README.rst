bigtempo
========

.. image:: https://pypip.in/d/bigtempo/badge.png
        :target: https://pypi.python.org/pypi/bigtempo

.. image:: https://pypip.in/v/bigtempo/badge.png
        :target: https://pypi.python.org/pypi/bigtempo


.. 
    ..image:: http://cloud.github.com/downloads/rhlobo/bigtempo/bigtempo_128.png // TODO


:Implementation: Python 2.7+
:Download: http://pypi.python.org/pypi/bigtempo/
:Source: http://github.com/rhlobo/bigtempo/
:Keywords: bigdata, time series, temporal processment, temporal analysis, data processment, data analysis, scalable, distributed, exploration, production ready, python


About
=====

**BigTempo** is a powerful temporal data processment / analysis library for Python, providing a scalable programming model conceived for data analysis, exploration and evaluation at massive levels.

.. Python package providing a powerful and scalable programming model specially crafted for temporal data processment / analysis. It was conceived for data analysis, exploration and production use, and it is ready to handle massive levels of data.

.. A powerful and scalable programming model specially crafted for temporal data processment / analysis. It's production ready and can handle large ammounts of data.


Motivation
----------

There were no simple solutions aiming temporal processments available out there.  **MapReduce**, for instance, can't process interdependent data models such as time series. So, altough easy exploration of many bigdata application domains was made viable lately, there is still a humonguous demand for more...

**BigTempo** is here to complement the set of tools you have available to solve bigdata problems.


Features
--------

- **Simplicity**

..     
    // TODO
    All you have to do is to declare your 'datasources'
    Encapsulates complexity of complex processment chains
    Evaluates dependencies automatically

- **Flexiblity**

.. 
    // TODO
    Designed to be easily extended
    Does not compete... Can be used in with simpy, theano, ... Complements them
    Can be adapted to process other data domains / models


- **Scalablability**

.. 
    // TODO
    Provides programming model built for distributed evaluation
    Integration with celery_ is in the way
    Thread / process pools also in the way


- **Performance**

.. 
    // TODO
    Promotes lazy evaluation
    Smart caching is in the way


.. _celery: http://github.com/celery/celery


Getting started
===============

Coming out soon!

.. 
    http://pandas.pydata.org/pandas-docs/dev/dsintro.html


More on about how to use it
---------------------------

If you need more examples, or just feel like checking out how bigtempo can be used in a project, refer to stockExperiments_.

.. _stockExperiments: https://github.com/rhlobo/stockExperiments


Installation
============

To install bigTempo, simply:

.. code-block:: bash

    $ pip install bigtempo

Or, if you absolutely must:

.. code-block:: bash

    $ easy_install bigtempo

But, you really shouldn't do that.


Dependencies
------------

    Both the installation methods above should take care of dependencies on its own, automatically.

The pandas_ library is the only direct dependency the package has. You should visit its page to find out what it depends on. For best results, we recommend installing optional packages as well. 

If you want to run the package tests, or enjoy its testing facilities, you'll need:

- mockito_ >= 0.5.1

In order to run the tests using the command contained in the ``bin`` directory, also install:

- nose >= 1.3.0
- coverage >= 3.6
- pep8 >= 1.4.5

.. _mockito: https://pypi.python.org/pypi/mockito
.. _pandas: http://github.com/pydata/pandas


Installing from source
------------------------

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
`development mode <http://www.pip-installer.org/en/latest/usage.html>`__)::

.. code-block:: bash

    $ pip install -e .


Bug tracker
===========

If you have any suggestions, bug reports or annoyances please report them to our issue_tracker_.

.. _issue_tracker: http://github.com/rhlobo/bigtempo/issues


Contribute
==========

1. On the tracker_, check for open issues or open a new one to start a discussion around a feature, idea or bug.
2. Fork the repository_ on GitHub to start making your changes.
3. Write a test which shows that the bug was fixed or that the feature works as expected.
4. Send a pull request and wait until it gets merged and published. Make sure to add yourself to AUTHORS_.

.. _tracker: http://github.com/rhlobo/bigtempo/issues
.. _repository: http://github.com/rhlobo/bigtempo
.. _AUTHORS: https://github.com/rhlobo/bigtempo/blob/master/AUTHORS.rst
