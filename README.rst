ROC - Remote Object Call
========================

|Build Status| |PyPi version|

ROC is thin wrapper around SimpleXMLRPCServer allowing to manipulate
remote objects like they are local.

Usage
=====

Given you have remote\_class.py, that contains class RemoteClass on
machine **A** with ip 192.168.1.2. You want to serve it through ROC on
port 1234. After that you want to access it from machine **B**

On machine **A** in OS shell execute:

::

    $ python -m "roc" -m remote_class.py -p 1234

On machine **B** in python interactive shell execute:

::

    >>> from roc.client import server_proxy, remote_module
    >>> proxy = server_proxy(host='192.168.1.2', port=1234)
    >>> RModule = remote_module(proxy)

So now, RModule is like locally imported module, and you can access all
classes, that machine **A** serves through it.

The code executed on machine **B**:

::

    remote_instance = RModule.RemoteClass(1, 2, 3)

Will instantiate class RemoteClass from module remote\_class.py on
machine **A**. Then it will bind it to remote\_instance variable on
machine **B**.

From now every method called on remote\_instance will be executed on
machine **A**.

When you finished, call ``proxy.shutdown()`` to, well, shut down remote
ROC server.

Bit Of History
==============

ROC development was started to support acceptance testing of distributed
systems with `FitNesse <http://fitnesse.org>`__,
`waferslim <https://github.com/peterdemin/waferslim>`__ and
`vagrant <http://vagrantup.com>`__ System infrastucture may be described
as follows:

-  Host machine running FitNesse server and SLIM server;
-  Set of guests, that are provisioned by vagrant with ROC servers;

When hosts' fixture is invoked by SLIM server, it can access guests' roc
servers. That makes testing of distributed systems transparent and easy.

.. |Build Status| image:: https://travis-ci.org/peterdemin/python-roc.png?branch=master
   :target: https://travis-ci.org/peterdemin/python-roc
.. |PyPi version| image:: https://pypip.in/v/roc/badge.png
   :target: https://crate.io/packages/roc/
