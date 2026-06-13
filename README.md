# Spring Bridge

## Project Description

The project is a 3D simulation of a footbridge modeled as a system of springs and planks to observe how a bridge would react to moving loads in the form of pedestrians.

The simulation has a segmented bridge, a red-blue heatmap that displays the current load on different planks depending on the force applied to the adjacent springs, and, most importantly, penguins.

This simulation continuously calculates the springs' net forces using Hooke's Law and velocity-dependent damping representing internal friction.

The user interface allows for the adjustment of various factors:
1. Number of people → number of pedestrians crossing
2. Mass of each person → adjusts the mg vector down
3. Speed of each person → how quickly the load transfers between planks (impulse and transfer of momentum)
4. Number of Planks → changes mass distribution
5. Spring constant of all springs → rigidity of the planks
6. Number of Springs in parallel → multiplying the stiffness by having multiple springs (increases k constant)
7. Damping (b) → controls the friction that will cause the bridge to stabilize rather than oscillate forever
8. Type (Torsion, Tension, or Compression) → changes the calculation of the maximum force a spring can withstand
9. Material of Spring (Aluminum, Steel, Bronze) → changes shear; durability of the bridge

The user's input impacts the main visual, but also other tracked data: 
1. Plank Force Heatmap: A map that shifts color (Blue to Red) based on the current mechanical load acting on the planks.
2. System Energy Graph: A graph that tracks Kinetic, Potential, and Total Energy (Joules) over time.
3. Max Spring Stress Graph: Tracks the peak stress fraction (0 = relaxed, 1.0 = breaking threshold) across all springs over time to indicate the point of collapse.
4. Plank Net Vertical Force Graph: Displays the real-time net force (Newtons) distributed across each plank, highlighting load transfers and equilibrium states.
5. Center Plank Displacement Graph: Plots the vertical displacement of the bridge's center over time.
