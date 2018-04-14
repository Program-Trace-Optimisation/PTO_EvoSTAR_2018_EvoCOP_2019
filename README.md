# PTO
Program Trace Optimisation is a system for `universal heuristic optimization made easy'. This is achieved by strictly separating the problem from the search algorithm.
New problem definitions and new generic search algorithms can be added to PTO easily and independently, and any algorithm can be used on any problem. PTO automatically extracts knowledge from the problem specification and designs search operators for the problem. The operators designed by PTO for standard representations coincide with existing ones, but PTO automatically designs operators for arbitrary representations.

This repository contains code implementing PTO in Python under `src`.

A [draft paper](docs/paper_2018.pdf) describing the system is provided.

Several tutorial-style Jupyter notebooks are available:
* [Onemax](src/problem/onemax.ipynb)
* [Sphere](src/problem/sphere.ipynb)
* [TSP](src/problem/TSP.ipynb).

[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/Program-Trace-Optimisation/PTO/master) to use interactive notebooks
