# Brace Root

Brace Root contribution to mechanical stability

## Documentation


### Installation with Miniconda (Windows, linux, OSX)

#### Miniconda installation

Follow official website instruction to install miniconda :

http://conda.pydata.org/miniconda.html

1. Create virtual environment and activate it
.............................................

```
    conda create --name brace python=2.7
    source activate brace
```

2. Build and install from source (alternative)
................................................

```
    cd braceroot/conda
    conda build -c openalea/label/unstable -c openalea .
    conda install -c openalea/label/unstable -c openalea --use-local braceroot
```

(Optional) Install several package managing tools :

```
    conda install notebook nose sphinx sphinx_rtd_theme pandoc coverage
```

Authors
-------

* Erin Sparks
* Lindsay Erndwein
* Baptiste Brument
* Christian Fournier	
* Christophe Pradal
* Adam Stager
