# Spring Bridge

## Project Description

The project will build a 3D simulation of a footbridge modeled as a system of springs and planks to observe how a bridge would react to moving loads in the form of pedestrians.

The simulation will have a segmented bridge, which will have a red-blue gradient overlay dependent on the force on the adjacent springs of a plank, stick figures of varying sizes (depending on their mass).

The user interface will allow for the adjustment of various factors:
1. Amount of people → number of pedestrians crossing
2. Mass of each person → adjusts the mg vector down
3. Speed of each person → how quickly the load transfers between planks
4. Number of Planks → changes mass distribution
5. Spring constant of all springs → rigidity of the planks
6. Number of Springs in parallel → changes the elasticity
7. Type (Torsion, Tension, or Compression) → changes calculation of max force
8. Material of Spring (Aluminum, Steel, Bronze) → changes shear; durability of bridge



The users inputs will impact the main visual, but also other tracked data: 
1. The displacement of the center of the bridge
2. Tension/Resistive force on the different springs of the bridge
3. Energy graph that plots kinetic + potential energy
4. Red-blue gradient overlay on each plank which changes based on force

---

## Repository Structure

```bash
.
├── README.md
├── main.py			# main file; loops through objects
├── plank.py 		# plank object
└── spring.py 		# spring object
```