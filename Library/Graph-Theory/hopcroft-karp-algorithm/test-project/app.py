import os
import sys

# Add the parent directory to sys.path to import the core algorithm
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.hopcroft_karp import HopcroftKarp

def main():
    print("Hopcroft-Karp Algorithm - Test Project")
    print("-" * 40)
    
    # Example: Assigning Applicants (U nodes) to Jobs (V nodes)
    applicants = ['Alice', 'Bob', 'Charlie', 'Diana']
    jobs = ['Engineer', 'Designer', 'Manager', 'Analyst']
    
    hk = HopcroftKarp(applicants, jobs)
    
    # Add matches based on skills and job requirements
    # Alice can be an Engineer or a Designer
    hk.add_edge('Alice', 'Engineer')
    hk.add_edge('Alice', 'Designer')
    
    # Bob is only an Engineer
    hk.add_edge('Bob', 'Engineer')
    
    # Charlie can be a Designer or an Analyst
    hk.add_edge('Charlie', 'Designer')
    hk.add_edge('Charlie', 'Analyst')
    
    # Diana can only be an Analyst
    hk.add_edge('Diana', 'Analyst')
    
    # Example edge case: No one can be a Manager in this exact configuration
    
    print("\nApplicants:", applicants)
    print("Jobs:", jobs)
    print("Graph Edges (Skills -> Job Requirement):")
    for u, v_list in hk.graph.items():
        print(f"  {u} -> {', '.join(v_list)}")
    
    # Find the maximum matching
    max_matches, matches = hk.max_matching()
    
    print("\nResults:")
    print("-------")
    print(f"Maximum Number of Matchings: {max_matches}")
    print("Assignments:")
    for applicant, job in matches.items():
        print(f"  {applicant} is assigned to {job}")

if __name__ == "__main__":
    main()
