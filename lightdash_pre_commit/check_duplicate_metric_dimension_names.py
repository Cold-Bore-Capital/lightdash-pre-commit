import argparse
from typing import Optional
from typing import Sequence

import yaml


def find_duplicates(data: dict) -> list:
    all_names = {}  # Dictionary to track both metrics and dimensions
    errors = []

    # Check for metrics and dimensions defined at the model 'meta' level
    for model in data.get("models", []):
        # Process model-level metrics
        if "meta" in model and "metrics" in model["meta"]:
            for metric, details in model["meta"]["metrics"].items():
                all_names[metric] = all_names.get(metric, 0) + 1

        # Check for metrics and dimensions defined at the column level
        for column in model.get("columns", []):
            # Process column-level dimensions
            if "meta" in column and "dimension" in column["meta"]:
                column_name = column['name']
                all_names[column_name] = all_names.get(column_name, 0) + 1

            # Process column-level additional dimensions
            if "meta" in column and "additional_dimensions" in column["meta"]:
                for ad_dim, ad_details in column["meta"]["additional_dimensions"].items():
                    all_names[ad_dim] = all_names.get(ad_dim, 0) + 1

            # Process column-level metrics
            if "meta" in column and "metrics" in column["meta"]:
                for metric_name, details in column["meta"]["metrics"].items():
                    all_names[metric_name] = all_names.get(metric_name, 0) + 1

    # Check for duplicates and gather error messages
    for name, count in all_names.items():
        if count > 1:
            errors.append(
                f"Duplicate name '{name}' used {count} times (as metrics or dimensions)."
            )

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
