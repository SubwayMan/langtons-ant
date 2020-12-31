# Langton's Ant

Langton's Ant is a simple set of rules that are imposed on an "ant" moving through a grid, leading to complex emergent behaviour.

# Program Features

  - Simulate behaviour of Langton's Ant
  - Change rules to observe varying emergent behaviour
  - Simulate at varying speeds

# Program use
- To get the code onto your machine, you can download git and directly clone this repository. This simulation requires PyFLTK preinstalled.
- If you have never used Git before, you can instead copy-paste the source code onto your own machine, save it as a new python script, and run it from there. Only the src/LangtonsAnt.py code is necessary.
- If using git, run simulation by going to the src directory and running the main script [Langton.py].
- Simulation can be started/paused with buttons. Upon pause, simulation can also be reset.
- Loaded simulation can be changed from the menu. Accepts a string of length 2-12 comprising of characters ["L", "R"] (case sensitive)
- Simulation speed can be controlled using slider on the bottom. slider is [logarithmic], ranging from 1-0.001s. (Innacurate, likely due to bottleneck from FLTK draw speeds)
# License
This program was constructed using a Python wrapper for the FLTK toolkit.
Software is issued under an MIT License.

# Examples
### RL (Default)
![Image1](./examples/example1.png)

### LRRL
![Image2](./examples/example2.png)

### LRLLRR
![Image3](./examples/example3.png)
# Todos
 - Add multiple "ant" states functionality
 - Add Hexagonal grid mode
 - Fix logarithmic speed slider to go down to 1 millis
# Further Reading
[Langton's Ant] - Wikipedia

   [Langton's Ant]: <https://en.wikipedia.org/wiki/Langton%27s_ant>
   [Logarithmic]: <https://en.wikipedia.org/wiki/Logarithmic_scale>
   [Langton.py]: <https://github.com/SubwayMan/langtons-ant/blob/master/src/Langton.py>

