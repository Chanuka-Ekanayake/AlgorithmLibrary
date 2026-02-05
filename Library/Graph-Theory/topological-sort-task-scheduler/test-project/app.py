"""
Real-World Application: Build System Task Scheduler
Uses Topological Sort to determine the correct order to build project files
"""

import sys
import os

# Add parent directory to path to import the core module
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from core.topological_sort import TopologicalSort, topological_sort_with_names


def build_system_scheduler():
    """
    Example: Software Build System
    Determine the order to compile files based on dependencies
    """
    print("=" * 60)
    print("BUILD SYSTEM - File Compilation Order")
    print("=" * 60)
    
    files = [
        "utils.py",      # 0 - No dependencies
        "config.py",     # 1 - No dependencies
        "database.py",   # 2 - Depends on config
        "models.py",     # 3 - Depends on database
        "api.py",        # 4 - Depends on models and utils
        "main.py"        # 5 - Depends on api and config
    ]
    
    # Dependencies (source -> depends on source)
    dependencies = [
        ("config.py", "database.py"),    # database needs config
        ("database.py", "models.py"),    # models need database
        ("models.py", "api.py"),         # api needs models
        ("utils.py", "api.py"),          # api needs utils
        ("api.py", "main.py"),           # main needs api
        ("config.py", "main.py"),        # main needs config
    ]
    
    print("\nFiles to compile:")
    for i, file in enumerate(files):
        print(f"  {i}. {file}")
    
    print("\nDependencies:")
    for prereq, dependent in dependencies:
        print(f"  {dependent} requires {prereq}")
    
    # Get compilation order
    order = topological_sort_with_names(files, dependencies)
    
    if order is None:
        print("\n❌ ERROR: Circular dependency detected!")
        print("Cannot determine build order.")
    else:
        print("\n✓ Build Order (DFS-based):")
        for i, file in enumerate(order, 1):
            print(f"  {i}. Compile {file}")


def course_prerequisite_planner():
    """
    Example: University Course Planning
    Determine the order to take courses based on prerequisites
    """
    print("\n\n" + "=" * 60)
    print("COURSE PLANNER - Semester Schedule")
    print("=" * 60)
    
    courses = [
        "CS101 - Intro to Programming",       # 0
        "CS102 - Data Structures",            # 1
        "CS201 - Algorithms",                 # 2
        "CS202 - Database Systems",           # 3
        "CS301 - Operating Systems",          # 4
        "CS302 - Computer Networks",          # 5
        "MATH101 - Calculus I",               # 6
        "MATH201 - Discrete Math",            # 7
    ]
    
    # Prerequisites (prerequisite, course)
    prerequisites = [
        ("CS101 - Intro to Programming", "CS102 - Data Structures"),
        ("CS102 - Data Structures", "CS201 - Algorithms"),
        ("CS102 - Data Structures", "CS202 - Database Systems"),
        ("CS201 - Algorithms", "CS301 - Operating Systems"),
        ("CS201 - Algorithms", "CS302 - Computer Networks"),
        ("MATH101 - Calculus I", "MATH201 - Discrete Math"),
        ("MATH201 - Discrete Math", "CS201 - Algorithms"),
    ]
    
    print("\nAvailable Courses:")
    for i, course in enumerate(courses):
        print(f"  {i}. {course}")
    
    print("\nPrerequisites:")
    for prereq, course in prerequisites:
        print(f"  {course}")
        print(f"    ↳ requires: {prereq}")
    
    # Get course order using Kahn's algorithm
    course_to_idx = {course: idx for idx, course in enumerate(courses)}
    topo = TopologicalSort(len(courses))
    
    for prereq, course in prerequisites:
        topo.add_edge(course_to_idx[prereq], course_to_idx[course])
    
    # Check for cycle
    if topo.has_cycle():
        print("\n❌ ERROR: Circular prerequisite detected!")
        return
    
    order_indices = topo.topological_sort_kahn()
    
    print("\n✓ Recommended Course Sequence:")
    semester = 1
    courses_per_semester = 2
    
    for i in range(0, len(order_indices), courses_per_semester):
        print(f"\n  Semester {semester}:")
        for idx in order_indices[i:i + courses_per_semester]:
            print(f"    • {courses[idx]}")
        semester += 1


def package_dependency_resolver():
    """
    Example: Package Manager Dependency Resolution
    Determine installation order for software packages
    """
    print("\n\n" + "=" * 60)
    print("PACKAGE MANAGER - Installation Order")
    print("=" * 60)
    
    packages = [
        "python",        # 0
        "pip",           # 1
        "numpy",         # 2
        "pandas",        # 3
        "matplotlib",    # 4
        "scikit-learn",  # 5
        "tensorflow",    # 6
        "jupyter",       # 7
    ]
    
    # Dependencies (package, depends_on_package)
    dependencies = [
        ("python", "pip"),
        ("pip", "numpy"),
        ("pip", "matplotlib"),
        ("numpy", "pandas"),
        ("numpy", "scikit-learn"),
        ("numpy", "tensorflow"),
        ("matplotlib", "pandas"),
        ("pandas", "scikit-learn"),
        ("pip", "jupyter"),
        ("numpy", "jupyter"),
    ]
    
    print("\nPackages to install:")
    for pkg in packages:
        print(f"  • {pkg}")
    
    print("\nDependency Graph:")
    dep_dict = {}
    for prereq, pkg in dependencies:
        if pkg not in dep_dict:
            dep_dict[pkg] = []
        dep_dict[pkg].append(prereq)
    
    for pkg, deps in dep_dict.items():
        print(f"  {pkg}:")
        for dep in deps:
            print(f"    ↳ requires {dep}")
    
    # Get installation order
    order = topological_sort_with_names(packages, dependencies)
    
    if order:
        print("\n✓ Installation Sequence:")
        for i, pkg in enumerate(order, 1):
            print(f"  {i}. Install {pkg}")
        
        print(f"\nTotal packages: {len(order)}")
    else:
        print("\n❌ Circular dependency detected!")


def project_task_scheduler():
    """
    Example: Project Management Task Scheduling
    Determine task execution order based on dependencies
    """
    print("\n\n" + "=" * 60)
    print("PROJECT MANAGEMENT - Task Schedule")
    print("=" * 60)
    
    tasks = [
        "Gather Requirements",       # 0
        "Design Database",            # 1
        "Design UI Mockups",          # 2
        "Setup Development Env",      # 3
        "Implement Backend API",      # 4
        "Implement Frontend",         # 5
        "Write Tests",                # 6
        "Deploy to Production",       # 7
    ]
    
    # Task dependencies
    dependencies = [
        ("Gather Requirements", "Design Database"),
        ("Gather Requirements", "Design UI Mockups"),
        ("Design Database", "Setup Development Env"),
        ("Setup Development Env", "Implement Backend API"),
        ("Implement Backend API", "Implement Frontend"),
        ("Design UI Mockups", "Implement Frontend"),
        ("Implement Backend API", "Write Tests"),
        ("Implement Frontend", "Write Tests"),
        ("Write Tests", "Deploy to Production"),
    ]
    
    print("\nProject Tasks:")
    for i, task in enumerate(tasks):
        print(f"  {i + 1}. {task}")
    
    print("\nTask Dependencies:")
    for prereq, task in dependencies:
        print(f"  '{task}' depends on '{prereq}'")
    
    # Create graph and detect cycles
    task_to_idx = {task: idx for idx, task in enumerate(tasks)}
    topo = TopologicalSort(len(tasks))
    
    for prereq, task in dependencies:
        topo.add_edge(task_to_idx[prereq], task_to_idx[task])
    
    # Get task order
    order_indices = topo.topological_sort_dfs()
    
    print("\n✓ Task Execution Timeline:")
    week = 1
    for idx in order_indices:
        print(f"  Week {week}: {tasks[idx]}")
        week += 1
    
    print(f"\nProject Duration: {len(order_indices)} weeks")


def circular_dependency_example():
    """
    Example: Detecting Circular Dependencies
    Shows what happens when dependencies form a cycle
    """
    print("\n\n" + "=" * 60)
    print("CIRCULAR DEPENDENCY DETECTION")
    print("=" * 60)
    
    print("\nScenario: Module Import System with Circular Dependency")
    
    modules = ["ModuleA", "ModuleB", "ModuleC", "ModuleD"]
    
    # Circular dependency: A → B → C → D → A
    dependencies = [
        ("ModuleA", "ModuleB"),
        ("ModuleB", "ModuleC"),
        ("ModuleC", "ModuleD"),
        ("ModuleD", "ModuleA"),  # Creates cycle!
    ]
    
    print("\nModule Dependencies:")
    for prereq, module in dependencies:
        print(f"  {module} imports {prereq}")
    
    order = topological_sort_with_names(modules, dependencies)
    
    if order is None:
        print("\n❌ CIRCULAR DEPENDENCY DETECTED!")
        print("Cycle: ModuleA → ModuleB → ModuleC → ModuleD → ModuleA")
        print("\nThis creates an infinite loop and cannot be resolved.")
        print("Solution: Refactor code to break the cycle.")
    else:
        print("\n✓ Valid module import order:", order)


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║" + " " * 10 + "TOPOLOGICAL SORT APPLICATIONS" + " " * 18 + "║")
    print("║" + " " * 12 + "Task Scheduling & Dependency Resolution" + " " * 7 + "║")
    print("╚" + "═" * 58 + "╝")
    
    # Run all examples
    build_system_scheduler()
    course_prerequisite_planner()
    package_dependency_resolver()
    project_task_scheduler()
    circular_dependency_example()
    
    print("\n" + "=" * 60)
    print("All examples completed!")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
