"""
Autograder runner script for GitHub Actions.
This file should be placed in the .grading/ directory of student repositories.
"""

import sys
from pathlib import Path

# Add .grading directory to path so we can import test_functions
sys.path.insert(0, str(Path(__file__).parent))

import test_functions
import assignment_config


def run_autograder():
    """Run autograder on all configured notebooks."""
    
    repo_root = Path.cwd()
    all_results = []
    total_score = 0
    max_total_score = 0
    
    print(f"\n{'='*70}")
    print(f"Running Autograder: {assignment_config.ASSIGNMENT_NAME}")
    print(f"{'='*70}\n")
    
    # Test each configured notebook
    for notebook_path in assignment_config.get_all_configured_notebooks():
        notebook_full_path = repo_root / notebook_path
        
        if not notebook_full_path.exists():
            print(f"⚠️  Warning: {notebook_path} not found, skipping...")
            continue
        
        print(f"Testing: {notebook_path}")
        
        config = assignment_config.get_notebook_config(notebook_path)
        results = test_functions.test_notebook(notebook_full_path, config)
        
        # Display results
        print(test_functions.format_results_for_display(results))
        
        all_results.append(results)
        total_score += results['overall_score']
        max_total_score += results['max_score']
    
    # Summary
    print(f"\n{'='*70}")
    print(f"AUTOGRADER SUMMARY")
    print(f"{'='*70}")
    print(f"\nAutomated Checks Score: {total_score}/{max_total_score} ({total_score/max_total_score*100:.1f}%)")
    print(f"\nThis covers:")
    print(f"  - Completeness: All questions attempted")
    print(f"  - Correctness: Automated answer checking")
    print(f"\nManual grading still required for:")
    print(f"  - Essay questions (detailed understanding)")
    print(f"  - Code quality assessment")
    print(f"  - Iterative development (commit history)")
    print(f"\n{'='*70}\n")
    
    # Save results to file
    with open('autograder_results.txt', 'w') as f:
        f.write(f"Autograder Results: {assignment_config.ASSIGNMENT_NAME}\n")
        f.write(f"{'='*70}\n\n")
        f.write(f"Overall Automated Score: {total_score}/{max_total_score} ({total_score/max_total_score*100:.1f}%)\n\n")
        
        for results in all_results:
            f.write(test_functions.format_results_for_display(results))
            f.write("\n")
    
    print("✓ Results saved to autograder_results.txt")
    
    # Exit with success if any tests ran
    return 0 if all_results else 1


if __name__ == "__main__":
    sys.exit(run_autograder())
