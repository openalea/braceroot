# Brace Root

[![Anaconda-Server Badge](https://anaconda.org/openalea3/braceroot/badges/installer/conda.svg)](https://conda.anaconda.org/openalea3)
[![Anaconda-Server Badge](https://anaconda.org/openalea3/braceroot/badges/downloads.svg)](https://anaconda.org/openalea3/braceroot)
[![CI Badge](https://github.com/openalea/braceroot/actions/workflows/conda-package-build.yml/badge.svg)](https://github.com/openalea/braceroot/actions)

Brace Root contribution to mechanical stability

## Documentation


### Installation with Miniconda (Windows, linux, OSX)

#### Miniconda installation

Follow official website instruction to install miniconda :

http://conda.pydata.org/miniconda.html

1. Create virtual environment and activate it

```
    conda create --name brace -c openalea3 -c conda-forge braceroot
    conda activate brace
```

2. Build and install from source (alternative)

```
    cd braceroot/conda
    conda build -c openalea/label/unstable -c openalea .
    conda install -c openalea/label/unstable -c openalea --use-local braceroot
```

(Optional) Install several package managing tools :

```
    conda install notebook pytest sphinx sphinx_rtd_theme pandoc coverage
```

## Authors

* Erin Sparks
* Christophe Pradal
* Baptiste Brument
* Lindsay Erndwein
* Christian Fournier	
* Adam Stager
