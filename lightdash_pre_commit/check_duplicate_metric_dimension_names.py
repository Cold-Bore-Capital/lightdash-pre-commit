import argparse
from typing import Optional
from typing import Sequence

import yaml


def find_duplicates(data: dict) -> list:
    metric_names = {}
    dimension_names = {}
    errors = []

    for model in data.get("models", []):
        for column in model.get("columns", []):
            # Process regular dimensions
            if "meta" in column and "dimension" in column["meta"]:
                dim_label = column["meta"]["dimension"].get("label")
                if dim_label is not None:
                    dimension_names[dim_label] = dimension_names.get(dim_label, 0) + 1

            # Process additional dimensions
            if "meta" in column and "additional_dimensions" in column["meta"]:
                for key in column["meta"]["additional_dimensions"]:
                    dimension_names[key] = dimension_names.get(key, 0) + 1

            # Process metrics
            if "meta" in column and "metrics" in column["meta"]:
                for metric in column["meta"]["metrics"]:
                    metric_names[metric] = metric_names.get(metric, 0) + 1

    # Check for duplicates and gather error messages
    for name, count in metric_names.items():
        if count > 1:
            errors.append(f"Duplicate metric name '{name}' found {count} times.")
    for name, count in dimension_names.items():
        if count > 1:
            errors.append(f"Duplicate dimension name '{name}' found {count} times.")

    return errors


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to check")
    args = parser.parse_args(argv)

    error_flag = False
    for file_path in args.filenames:
        try:
            with open(file_path, "r") as file:
                data = yaml.safe_load(file)
                errors = find_duplicates(data)
                if errors:
                    print(f"Errors found in '{file_path}':")
                    for error in errors:
                        print(error)
                    error_flag = True
        except Exception as e:
            print(f"Failed to process '{file_path}': {e}")
            error_flag = True

    if error_flag:
        return 1

    return 0


if __name__ == "__main__":
    exit(main(None))
