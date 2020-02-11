.. contents::

=======
cereals
=======

CEreal REpresentation, ALgorithm and Simulation

=============
Documentation
=============

[...]


=================================================
Installation with Miniconda (Windows, linux, OSX)
=================================================

Miniconda installation
----------------------

Follow official website instruction to install miniconda :

http://conda.pydata.org/miniconda.html

1. Install conda-build if not already installed
...............................................

.. code:: shell

    conda install conda-build

2. Create virtual environment and activate it
.............................................

.. code:: shell

    conda create --name cereals python
    source activate cereals

3. Build and install openalea.phenomenal package
................................................

.. code:: shell

    cd cereals/conda
    conda build -c openalea/label/unstable -c openalea .
    conda install -c openalea/label/unstable -c openalea --use-local openalea.cereals

(Optional) Install several package managing tools :

.. code:: shell

    conda install notebook nose sphinx sphinx_rtd_theme pandoc coverage

Authors
-------

* Fournier	    Christian
* Christophe    Pradal
* Artzet	    Simon