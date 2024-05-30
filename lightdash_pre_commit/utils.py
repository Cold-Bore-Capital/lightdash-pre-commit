def has_dimensions(data: dict) -> bool:
    """
    Check if the dbt resource has any dimensions.

    Args:
        data (dict): The dbt resource data.

    Returns:
        bool: True if the resource has dimensions, False otherwise.

    Raises:
        ValueError: If the dbt resource type is unsupported.
    """
    if "models" in data:
        return has_dimensions_in_model(data=data)
    else:
        raise ValueError("Unsupported dbt resource type")


def has_dimensions_in_model(data: dict) -> bool:
    """
    Check if the dbt model has any dimensions.

    Args:
        data (dict): The dbt model data.

    Returns:
        bool: True if the model has dimensions, False otherwise.
    """
    for model in data.get("models", []):
        for column in model.get("columns", []):
            if "meta" in column:
                if (
                    "dimension" in column["meta"]
                    or "additional_dimensions" in column["meta"]
                ):
                    return True
    return False


def has_metrics(data: dict) -> bool:
    """
    Check if the dbt resource has any metrics.

    Args:
        data (dict): The dbt resource data.

    Returns:
        bool: True if the resource has metrics, False otherwise.

    Raises:
        ValueError: If the dbt resource type is unsupported.
    """
    if "models" in data:
        return has_metrics_in_model(data=data)
    else:
        raise ValueError("Unsupported dbt resource type")


def has_metrics_in_model(data: dict) -> bool:
    """
    Check if the dbt model has any metrics.

    Args:
        data (dict): The dbt model data.

    Returns:
        bool: True if the model has metrics, False otherwise.
    """
    for model in data.get("models", []):
        for column in model.get("columns", []):
            if "meta" in column:
                if "metrics" in column["meta"]:
                    return True
    return False
