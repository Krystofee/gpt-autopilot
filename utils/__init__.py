def extract_python_code(text):
    """ get python code from response. Find ```python and ``` and return the code in between """
    code = ""
    start = text.find("```python")
    if start != -1:
        start = start + 9
        end = text.find("```", start)
        if end != -1:
            code = text[start:end]
    return code