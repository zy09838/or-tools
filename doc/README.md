# Routing Samples

OR-Tools comes with lots of routing samples

## Table of Contents

* [VRP](#vehicle-routing-problem)
* [CVRP](#capacitated-vehicle-routing-problem)
* [CVRPTW](#capacitated-vehicle-routing-problem-with-time-window)
* [Misc](#misc)

## Vehicle Routing Problem
Data Problem:
![problem](vrp.svg)
Solution:
![solution](vrp_solution.svg)
src: [vrp.py](vrp.py)

### GlobalSpan on Distance Dimension
Solution:
![solution](vrpgs_solution.svg)
src: [vrpgs.py](vrpgs.py)

## Capacitated Vehicle Routing Problem
Data Problem:
![problem](cvrp.svg)
Solution:
![solution](cvrp_solution.svg)
src: [cvrp.py](cvrp.py)

## Capacitated Vehicle Routing Problem with Time Windows
Data Problem:
![problem](cvrptw.svg)
Solution:
![solution](cvrptw_solution.svg)
src: [cvrptw.py](cvrptw.py)

## Misc
Images have been generated using [`vrp_svg.py`](vrp_vg.py) through bash script:
```sh
./generate_svg.sh
```
src: [generate_svg.sh](generate_svg.sh)
