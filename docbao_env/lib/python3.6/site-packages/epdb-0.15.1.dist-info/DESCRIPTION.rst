========
Overview
========

Adds functionality to the python debugger, including support for remote
debugging

Installation
============

::

    pip install epdb

Usage
=====

For debugging code locally, epdb generally works the same as `pdb
<https://docs.python.org/3/library/pdb.html>`_. You can debug a program from
the python interpreter::

    >>> import epdb
    >>> import mymodule
    >>> epdb.Epdb().run('mymodule.test()')
    *** NameError: name 'execfile' is not defined
    > /home/wasche/git/epdb/<string>(1)<module>()
    -> """
    (Epdb) continue
    Traceback (most recent call last):
      File "<console>", line 1, in <module>
      File "/usr/lib64/python3.5/bdb.py", line 431, in run
        exec(cmd, globals, locals)
      File "<string>", line 1, in <module>
      File "/home/wasche/git/epdb/mymodule.py", line 2, in test
        import spam
    ImportError: No module named 'spam'

You can also drop breakpoints at specific places in a program's code by
inserting::

    import epdb; epdb.set_trace()

or by using the alias ``st``::

    import epdb; epbd.st()

To debug code that is either running on a remote system, or in a process that
isn't attached to your tty you can use epdb in server mode::

    import epdb; epdb.serve()

By default ``epdb.serve()`` will start a simple telnet server on port 8080, but
you can use the ``port`` keyword argument to use a different port::

    import epdb; epdb.serve(port=8888)

You can connect to the epdb server by using ``epdb.connect()``::

    >>> import epdb
    >>> epdb.connect()

By default ``epdb.connect()`` will attempt to connect to port 8080 on
localhost. If you are debugging a process on another host or port, you can call
connect with the ``host`` or ``port`` keyword arguments::

    >>> import epdb
    >>> epdb.connect(host='some.host.com', port=8888)


