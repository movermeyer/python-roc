ROC - Remote Object Call
========================

[![Build Status](https://travis-ci.org/peterdemin/python-roc.png?branch=master)](https://travis-ci.org/peterdemin/python-roc)

ROC is RPC enhancment allowing to manipulate
remote objects like they are local

Why ROC?
========
ROC development was started to support acceptance testing
of distributed systems with [FitNesse](http://fitnesse.org)
and [waferslim](https://github.com/peterdemin/waferslim).
System infrastucture may be described as follows:

* Host machine running FitNesse server and SLIM server;
* Set of guests, that are provisioned by [vagrant](http://vagrantup.com) with current version of system under test;
* Host and Guests share same python sources (through VM shared folders);

When hosts' fixture is invoked by SLIM server, it can access guests' roc servers.
The trick is, that class definition acts as protocol description on host machine.
