=============
Python-Cicero
=============

Python-Cicero provides a Pythonic "wrapper" to `Azavea's Cicero API <http://www.azavea.com/cicero/>`_
for address-based legislative and non-legislative district matching, lookup of
elected official contact information, and election events.

Note: Be sure to take a look at `the project page on Github <http://github.com/azavea/python-cicero/>`_.

Installation / Setup
********************

Use pip to install the library:

    pip install python-cicero
    
If you anticipate making improvements/extensions and would like to document
them, use the extras_require convention to also install the Pycco documentation
generator as a dependency (see Documentation section below):
    
    pip install python-cicero['docs']
    
To make requests to the Cicero API, you will need a Cicero account. A free
trial of the API is available by registering `here <http://www.azavea.com/products/cicero/free-trial/>`_. The process for
purchasing additional API credits is described on the Cicero website.

Documentation
*************

Documentation, generated with `Pycco <http://fitzgen.github.io/pycco/>`_, is
available in the "docs" folder as HTML files. The filenames correspond to the
appropriate module being documented.

For examples of the wrapper in use, see the ``cicero_examples.py`` file.

Help!
*****

All of us at Azavea would be happy to help you get the most out of your
Cicero API account. For questions about this wrapper, contact
Community Evangelist, Andrew Thompson at athompson@azavea.com.

License
*******

python-cicero is licensed under the Apache 2.0 license. See ``LICENSE.txt`` for
more details.

Contribute
**********

See a bug? Want to improve the docs or provide more examples? Thank you!
Please open a pull-request with your improvements and we'll work to respond
to it in a timely manner.