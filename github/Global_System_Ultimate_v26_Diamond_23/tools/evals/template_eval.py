"""
Eval Template for Eval-Driven Development (EDD).
Use this template to define success metrics BEFORE writing code.
"""

def eval_feature_x(output: str, expected: str) -> bool:
    """
    Metric: Exact Match
    Pass Criteria: Output must exactly match expected string.
    """
    return output.strip() == expected.strip()

def eval_feature_y_robustness(output_json: dict) -> bool:
    """
    Metric: Schema Validation
    Pass Criteria: Output must be valid JSON with required fields.
    """
    required_fields = ["id", "status", "timestamp"]
    return all(field in output_json for field in required_fields)
