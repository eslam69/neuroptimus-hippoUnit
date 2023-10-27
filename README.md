# Neuroptimus
Neuroptimus is a graphical tool for fitting the parameters of neuronal models

Installation
============

Install `git` and type:


    git clone https://github.com/mohacsimate/neuroptimus


Dependencies
-------------

The following python libraries are required:
  - python
  - numpy 
  - eFEL
  - matplotlib 

The following libraries are recommended:
  - neuron
  - scipy 
  - PyQt5
  - inspyred 
  - pyelectro
  - Pygmo
  - bluepyopt
  - ipyparallel
  - nest
  - nest_simulator
  
You can get all the libraries with `pip` with the following command (for numpy):

  
    pip install numpy


Run Neuroptimus
-------------------

You can run Neuroptimus (with a GUI) directly from its folder with (PyQt5 required):

    python neuroptimus.py -g
    
Or for the command line version (you must specify a configuration file as well):

    python neuroptimus.py -c path/to/example.json
    
    
Test Platforms
--------------

The package was tested on the following systems:

    1. Ubuntu 22.04.1 LTS
    2. Fedora release 32 (Thirty Two) (neurofedora)

    
Developers
----------

Project Leader:

    - Szabolcs Káli:
        kali@koki.hu

Lead Developer:

    - Máté Mohácsi
	mohacsi.mate@koki.mta.hu
	
    - Sára Sáray
	saray.sara@koki.mta.hu
	
    - Márk Török Patrik
	torok.mark.patrik@gmail.com

    - Peter Friedrich:
        p.friedrich.m@gmail.com


