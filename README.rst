pastacli
=========================

Command line interface for interacting with the Provenance Aware Synthesis
Tracking Architecture (PASTA), the system that runs the Environmental Data
Initiative (EDI) data repository.

| This CLI implements functionality based on the API documented here:
| http://pastaplus-core.readthedocs.io/en/latest/index.html


Staging vs production
=========================
Use the --staging option to run commands using the staging server rather
than the production. This is probably most useful for testing uploads and
evaluations

    >>> pastacli --staging list package-identifiers knb-lter-cce
        9
        10
        11
        13
        ...


Searching
=========================
Search documents

.. code-block:: console

    $ pastacli search 'q=CTD&fl=doi,site'
    > <resultset numFound='265' start='0' rows='10'>
    >   <document>
    >       <doi>doi:10.6073/pasta/0a80531208b9750385315dca8d1614f4</doi>
    >       <site>cce</site>
    >   </document>
    >   <document>
    >       <doi>doi:10.6073/pasta/fae601f79f10ce0578f722f5f663a90a</doi>
    >       <site>cce</site>
    >   </document>
    >   ...
    >   ...
    > </resultset>

Use the `rows` and `start` params for a Solr query to specify how many records
you want. By default, the `search` command returns the first 10 rows.

You can override the `rows` and `start` params by specifying the `--all` option,
useful if you're running the script as part of some workflow and always want
all results to be returned.

.. code-block:: console

    $ pastacli search 'q=CTD&fl=doi,site' --all
    > <resultset numFound='265' start='0' rows='265'>
    >   <document>
    >       <doi>doi:10.6073/pasta/0a80531208b9750385315dca8d1614f4</doi>
    >       <site>cce</site>
    >   </document>
    >   ...
    >   ...
    > </resultset>

You can also just get the number of results for a query

.. code-block:: console

    $ pastacli search 'q=CTD&fl=doi,site' --count
    > 265
