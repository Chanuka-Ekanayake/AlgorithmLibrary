# Hopcroft-Karp Test Project

## Instructions

This test project demonstrates how to use the Hopcroft-Karp algorithm to solve a bipartite matching problem.

### Prerequisites
Make sure you have Python 3 installed.

### Running the Test
To execute the test project, simply run the Python `app.py` script:

```bash
cd test-project
python app.py
```

### Explanation of the Scenario
The test models a scenario where a group of `Applicants` are matched with open `Jobs`.
Each applicant applies for jobs based on their skills. Since each applicant can only take one job, and each job can be filled by at most one applicant, this forms a classic maximum bipartite matching problem.

The Hopcroft-Karp algorithm finds an optimal assignment that maximizes the number of filled jobs while respecting the applicant choices.
