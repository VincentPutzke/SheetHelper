import re
import pandas as pd
import io
import numpy as np

def _find_after_last(text, type_pattern):
    """
    Searches for the last occurrence of a given type pattern in a text and 
    returns the substring that follows it.

    Args:
        text: The input text string.
        type_pattern: The regular expression pattern to search for.  This should 
                      be a raw string (e.g., r"TYPE") to handle special characters
                      correctly.  It's best practice to make it specific enough
                      to avoid unintended matches.

    Returns:
        The substring after the last occurrence of the type pattern, or an 
        empty string if the pattern is not found.  Returns None if there's an
        issue with the regex pattern.
    """
    try:
        matches = list(re.finditer(type_pattern, text))  # Find all matches

        if matches:
            last_match = matches[-1]  # Get the last match object
            return text[last_match.end():]  # Return the substring after the match
        else:
            return ""  # Return empty string if no match is found

    except re.error as e: # Handle potential regex errors
        print(f"Invalid regex pattern: {e}")
        return None
        
def _find_before_first(text, type_pattern):
    """
    Searches for the first occurrence of a given type pattern in a text and 
    returns the substring that precedes it.

    Args:
        text: The input text string.
        type_pattern: The regular expression pattern to search for.  This should 
                      be a raw string (e.g., r"TYPE") to handle special characters
                      correctly. It's best practice to make it specific enough
                      to avoid unintended matches.

    Returns:
        The substring before the first occurrence of the type pattern, or the 
        original text if the pattern is not found. Returns None if there's an
        issue with the regex pattern.
    """
    try:
        match = re.search(type_pattern, text)  # Search for the first match

        if match:
            return text[:match.start()]  # Return the substring before the match
        else:
            return text  # Return the original text if no match is found

    except re.error as e: # Handle potential regex errors
        print(f"Invalid regex pattern: {e}")
        return None

def _filter_with_pattern(text, type_pattern_start, type_pattern_end):
    stage_1_text = _find_after_last(text, type_pattern_start)
    if stage_1_text is None:
        return ""
    stage_2_text = _find_before_first(stage_1_text, type_pattern_end)
    if stage_2_text is None:
        return ""
    return stage_2_text

def filter_code_result(text):
    return _filter_with_pattern(text, r"<TYP>", r"</TYP>")

def filter_task_result(text):
    return _filter_with_pattern(text, r"<TASK>", r"</TASK>")

def randomize_row_order(text, column_count):
    
    matches = re.findall(r"\"(.*?)\"", text)
    columns = []
    for i in range(column_count):
        columns.append([])
    col = 0
    header_row = []
    for m in matches[:-column_count]:
        header_row.append(m)
    for m in matches[column_count:]:
        columns[col].append(m)
        col += 1
        col %= column_count
    
    for c in columns:
        np.random.shuffle(c)
    
    row_count = len(columns[0])
    result = ""
    for c in range(column_count-1):
        result += f"\"{header_row[c]}\","
    result += f"\"{header_row[column_count-1]}\"\n"
    for r in range(row_count):
        for c in range(column_count-1):
            result += f"\"{columns[c][r]}\","
        result += f"\"{columns[column_count-1][r]}\"\n"
        
    return result