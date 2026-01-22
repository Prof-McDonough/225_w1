"""
Core testing functions for grading Jupyter notebooks.
Used by both GitHub Actions autograder and local grading script.
"""

import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import re
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import subprocess


def execute_notebook(notebook_path: Path, timeout: int = 600) -> nbformat.NotebookNode:
    """
    Execute a Jupyter notebook and return the executed notebook object.
    
    Args:
        notebook_path: Path to the notebook file
        timeout: Maximum time in seconds for execution
        
    Returns:
        Executed notebook object
        
    Raises:
        Exception if notebook fails to execute
    """
    with open(notebook_path) as f:
        nb = nbformat.read(f, as_version=4)
    
    ep = ExecutePreprocessor(timeout=timeout, kernel_name='python3')
    
    try:
        ep.preprocess(nb, {'metadata': {'path': notebook_path.parent}})
        return nb
    except Exception as e:
        raise Exception(f"Error executing {notebook_path.name}: {str(e)}")


def get_cell_output(nb: nbformat.NotebookNode, cell_index: int) -> str:
    """
    Extract text output from a specific cell in an executed notebook.
    
    Args:
        nb: Executed notebook object
        cell_index: Index of the cell (0-based)
        
    Returns:
        String representation of cell output
    """
    if cell_index >= len(nb.cells):
        return ""
    
    cell = nb.cells[cell_index]
    
    if cell.cell_type != 'code':
        return ""
    
    output_text = []
    for output in cell.get('outputs', []):
        if output.output_type == 'stream':
            output_text.append(output.text)
        elif output.output_type == 'execute_result':
            output_text.append(output.data.get('text/plain', ''))
        elif output.output_type == 'display_data':
            output_text.append(output.data.get('text/plain', ''))
    
    return ''.join(output_text).strip()


def get_cell_source(nb: nbformat.NotebookNode, cell_index: int) -> str:
    """
    Get the source code of a specific cell.
    
    Args:
        nb: Notebook object
        cell_index: Index of the cell (0-based)
        
    Returns:
        Source code as string
    """
    if cell_index >= len(nb.cells):
        return ""
    
    return nb.cells[cell_index].source


def check_output_matches(actual: str, expected: str, flexible: bool = True) -> bool:
    """
    Check if actual output matches expected output.
    
    Args:
        actual: Actual output from notebook
        expected: Expected output
        flexible: If True, ignore whitespace differences and case
        
    Returns:
        True if outputs match
    """
    if flexible:
        # Normalize whitespace and case
        actual_normalized = re.sub(r'\s+', ' ', actual.lower().strip())
        expected_normalized = re.sub(r'\s+', ' ', expected.lower().strip())
        return actual_normalized == expected_normalized
    else:
        return actual.strip() == expected.strip()


def check_code_contains_ellipsis(source: str) -> bool:
    """
    Check if code cell still contains the ... placeholder.
    
    Args:
        source: Source code from cell
        
    Returns:
        True if ... is found (indicating incomplete work)
    """
    # Match ... that's not part of a string or comment
    # Simple check: look for ... on its own or in print(...)
    return '...' in source and not ('"""' in source or "'''" in source)


def check_essay_answered(nb: nbformat.NotebookNode, cell_index: int, min_length: int = 20) -> Tuple[bool, str]:
    """
    Check if an essay question has been answered (replaced < your answer >).
    
    Args:
        nb: Notebook object
        cell_index: Index of the markdown cell with essay answer
        min_length: Minimum length of answer in characters
        
    Returns:
        Tuple of (answered: bool, answer_text: str)
    """
    if cell_index >= len(nb.cells):
        return False, ""
    
    cell = nb.cells[cell_index]
    
    if cell.cell_type != 'markdown':
        return False, ""
    
    answer = cell.source.strip()
    
    # Check if still contains placeholder
    if '< your answer >' in answer.lower():
        return False, answer
    
    # Check minimum length
    if len(answer) < min_length:
        return False, answer
    
    return True, answer


def run_basic_linting(source: str) -> List[str]:
    """
    Run basic code quality checks and return list of suggestions.
    
    Args:
        source: Source code to check
        
    Returns:
        List of linting suggestions (empty if no issues)
    """
    suggestions = []
    
    lines = source.split('\n')
    
    for i, line in enumerate(lines, 1):
        # Skip empty lines and comments
        if not line.strip() or line.strip().startswith('#'):
            continue
        
        # Check line length (PEP 8 recommends max 79 characters)
        if len(line) > 100:  # Being lenient for beginners
            suggestions.append(f"Line {i} is very long ({len(line)} chars). Consider breaking it up.")
        
        # Check for missing spaces around operators
        if re.search(r'[a-zA-Z0-9]\+[a-zA-Z0-9]', line) or \
           re.search(r'[a-zA-Z0-9]=[a-zA-Z0-9]', line.replace('==', '')):
            if '==' not in line:  # Don't flag comparison operators
                suggestions.append(f"Line {i}: Consider adding spaces around operators for readability.")
        
        # Check for variable names with mixed case (not following snake_case)
        var_pattern = r'\b([a-z]+[A-Z][a-zA-Z]*)\s*='
        if re.search(var_pattern, line):
            suggestions.append(f"Line {i}: Consider using snake_case for variable names (e.g., my_variable).")
    
    return suggestions[:3]  # Limit to 3 suggestions to avoid overwhelming


def analyze_commits(repo_path: Path, min_commits: int = 3) -> Dict[str, any]:
    """
    Analyze git commit history for iterative development.
    
    Args:
        repo_path: Path to the git repository
        min_commits: Minimum expected number of commits
        
    Returns:
        Dictionary with commit analysis results
    """
    try:
        # Get commit count
        result = subprocess.run(
            ['git', 'rev-list', '--count', 'HEAD'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        commit_count = int(result.stdout.strip())
        
        # Get commit messages
        result = subprocess.run(
            ['git', 'log', '--pretty=format:%s'],
            cwd=repo_path,
            capture_output=True,
            text=True,
            check=True
        )
        messages = result.stdout.strip().split('\n')
        
        # Analyze message quality
        descriptive_count = 0
        for msg in messages:
            # Consider message descriptive if it's longer than 10 chars and not generic
            generic_words = ['update', 'done', 'fix', 'wip', 'change', 'commit', 'save']
            is_generic = msg.lower().strip() in generic_words
            is_long_enough = len(msg.strip()) >= 10
            
            if is_long_enough and not is_generic:
                descriptive_count += 1
        
        return {
            'commit_count': commit_count,
            'meets_minimum': commit_count >= min_commits,
            'descriptive_count': descriptive_count,
            'descriptive_ratio': descriptive_count / commit_count if commit_count > 0 else 0,
            'messages': messages
        }
    
    except subprocess.CalledProcessError as e:
        return {
            'commit_count': 0,
            'meets_minimum': False,
            'descriptive_count': 0,
            'descriptive_ratio': 0,
            'messages': [],
            'error': str(e)
        }


def test_notebook(notebook_path: Path, test_config: Dict) -> Dict:
    """
    Test a single notebook according to configuration.
    
    Args:
        notebook_path: Path to notebook file
        test_config: Dictionary with test configuration
        
    Returns:
        Dictionary with test results
    """
    results = {
        'notebook': notebook_path.name,
        'executed': False,
        'questions': {},
        'overall_score': 0,
        'max_score': 0,
        'errors': []
    }
    
    try:
        # Execute notebook
        nb = execute_notebook(notebook_path)
        results['executed'] = True
        
        # Test each question
        for question_id, question_config in test_config.get('questions', {}).items():
            question_result = {
                'passed': False,
                'score': 0,
                'max_score': question_config.get('points', 1),
                'feedback': []
            }
            
            results['max_score'] += question_result['max_score']
            
            if question_config['type'] == 'code':
                cell_index = question_config['cell_index']
                source = get_cell_source(nb, cell_index)
                
                # Check if still contains ellipsis
                if check_code_contains_ellipsis(source):
                    question_result['feedback'].append("Code still contains '...' placeholder")
                else:
                    # Get output
                    output = get_cell_output(nb, cell_index)
                    
                    # Check expected outputs
                    expected_outputs = question_config.get('expected_outputs', [])
                    if isinstance(expected_outputs, str):
                        expected_outputs = [expected_outputs]
                    
                    matched = False
                    for expected in expected_outputs:
                        if check_output_matches(output, expected):
                            matched = True
                            break
                    
                    if matched:
                        question_result['passed'] = True
                        question_result['score'] = question_result['max_score']
                        question_result['feedback'].append("✓ Correct output")
                    else:
                        question_result['feedback'].append(f"Expected output like: {expected_outputs[0][:50]}...")
                        question_result['feedback'].append(f"Got: {output[:50]}...")
                    
                    # Run linting for feedback
                    linting_suggestions = run_basic_linting(source)
                    if linting_suggestions:
                        question_result['feedback'].append("Code quality suggestions:")
                        question_result['feedback'].extend(linting_suggestions)
            
            elif question_config['type'] == 'essay':
                cell_index = question_config['cell_index']
                answered, answer_text = check_essay_answered(nb, cell_index)
                
                if answered:
                    question_result['passed'] = True
                    question_result['score'] = question_result['max_score']
                    question_result['feedback'].append("✓ Answer provided (requires manual review)")
                else:
                    question_result['feedback'].append("No answer provided or too short")
            
            results['questions'][question_id] = question_result
            results['overall_score'] += question_result['score']
    
    except Exception as e:
        results['errors'].append(str(e))
    
    return results


def format_results_for_display(results: Dict) -> str:
    """
    Format test results for display in GitHub Actions or console.
    
    Args:
        results: Test results dictionary
        
    Returns:
        Formatted string for display
    """
    output = []
    output.append(f"\n{'='*60}")
    output.append(f"Results for: {results['notebook']}")
    output.append(f"{'='*60}")
    
    if not results['executed']:
        output.append("❌ Failed to execute notebook")
        for error in results['errors']:
            output.append(f"  Error: {error}")
        return '\n'.join(output)
    
    output.append(f"\nOverall Score: {results['overall_score']}/{results['max_score']} ({results['overall_score']/results['max_score']*100:.0f}%)")
    output.append(f"\nQuestion Results:")
    
    for q_id, q_result in results['questions'].items():
        status = "✓" if q_result['passed'] else "✗"
        output.append(f"\n{status} {q_id}: {q_result['score']}/{q_result['max_score']} points")
        for feedback in q_result['feedback']:
            output.append(f"  {feedback}")
    
    if results['errors']:
        output.append(f"\nErrors:")
        for error in results['errors']:
            output.append(f"  {error}")
    
    output.append(f"\n{'='*60}\n")
    
    return '\n'.join(output)
