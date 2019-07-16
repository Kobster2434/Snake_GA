# Snake_GA
Genetic algorithm to play a simple snake game.
Currently incomplete. I implemented a basic Genetic algorithm that doesn't work well. 

Next steps:
1: Try Reinforcement learning
2: Try a more complex genetic algorithm (NEAT?)
3: Keep current GA system but change how things are chosen (via crossover/mutation). Something such as Tournament rank selection may be sufficient. 
4: ... 

I got the snake game from the link below and modified the code appropraitely to fit my purpose. 
https://code.activestate.com/recipes/578996-snake-the-game/

Improvements to make:
- Show as text what generation and what number of the population to make more user friendly.
- Record best game each genreation and store best nerual network parameters from this. Note that pygame isn't the best for this and I may be limited by this.

Main issue with initial implementation is that it gets stuck at the beginning. Relevant hypothesis aren't going through to the next generation.
