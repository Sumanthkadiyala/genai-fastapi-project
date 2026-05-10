def calculate(expression: str):
    """
    Evaluates simple mathematical expressions.
    Example: '25 * 17'
    """

    try:
        result = eval(expression)
        return str(result)
    except Exception:
        return "Invalid mathematical expression."