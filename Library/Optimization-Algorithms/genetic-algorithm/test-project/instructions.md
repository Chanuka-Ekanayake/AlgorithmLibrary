# User Guide: Natural Selection Simulator (Genetic Algorithm)

This project provides a highly visual demonstration of **Genetic Algorithms**. 

## What You'll See
The engine is tasked with generating the exact target phrase `"ALGORITHM ENGINEERING"`. 
- However, it has absolutely no idea what the target is. It is only given a **Fitness Score** (e.g., "you got 3 letters right").
- It starts with a population of 200 completely random strings (e.g., `"XHQ PZTWOMBEIF YU"`).
- Through the biological processes of **Tournament Selection**, **Crossover** (mating strings together), and **Mutation** (randomly flipping letters), you will watch the population rapidly evolve out of the chaos.
- Within just a few hundred generations (usually under a second), it solves the target!

## How to Test

1. **Navigate** to the `test-project` folder.
2. **Run** the simulator:
   ```bash
   python app.py
   ```

## Why this is powerful
If you tried to guess the string `"ALGORITHM ENGINEERING"` (21 characters) using pure randomness, there are $27^{21}$ combinations. You would literally be guessing until the heat death of the universe. 

By applying evolutionary pressure, the Genetic Algorithm solves it in a fraction of a second.
