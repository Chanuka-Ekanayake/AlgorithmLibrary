# User Guide: Fair Marketplace Rotator

This project demonstrates the necessity of unbiased randomization in E-commerce environments.

## The Logic
Unlike naive shuffling (like `list.sort(key=lambda x: random.random())`), Fisher-Yates ensures that every item has an exactly equal probability ($1/N$) of appearing in any specific slot. 

## Instructions
1. Navigate to the `test-project` directory.
2. Run the application:
   ```bash
   python app.py