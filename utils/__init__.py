def extract_python_code(text):
    """get python code from response. Find (```python | ```) and ``` and return the code in between"""
    # Find the first occurence of ```python
    start = text.find("```python")
    start_offset = 8
    if start == -1:
        start = text.find("```")
        start_offset = 3
    if start == -1:
        return text
    # Find the first occurence of ``` after the first occurence of ```python
    end = text.find("```", start + 1)
    if end == -1:
        return text[start + start_offset :]
    return text[start + start_offset : end]
