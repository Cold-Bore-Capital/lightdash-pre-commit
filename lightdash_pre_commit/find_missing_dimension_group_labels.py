import argparse
from typing import Optional
from typing import Sequence

import yaml


def find_missing_group_labels(data: dict) -> list:
    errors = []

    for model in data.get("models", []):
        # Check metrics and dimensions inside each column
        for column in model.get("columns", []):
            if "meta" in column:
                # Check primary dimension
                if "dimension" in column["meta"]:
                    dimension_details = column["meta"]["dimension"]
                    if (
                        not dimension_details.get("hidden", False)
                        and "group_label" not in dimension_details
                    ):
                        errors.append(
                            f"Missing 'group_label' in dimension of column '{column.get('name')}'."
                        )

                # Check additional dimensions
                if "additional_dimensions" in column["meta"]:
                    for dimension_name, dim_details in column["meta"][
                        "additional_dimensions"
                    ].items():
                        if (
                            not dim_details.get("hidden", False)
                            and "group_label" not in dim_details
                        ):
                            errors.append(
                                f"Missing 'group_label' in additional dimension '{dimension_name}' in column "
                                f"'{column.get('name')}'."
                            )

    return errors


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Check YAML files for missing 'group_label' in dimensions",
    )
    args = parser.parse_args(argv)

    error_flag = False
    for file_path in args.filenames:
        try:
            with open(file_path, "r") as file:
                data = yaml.safe_load(file)
                errors = find_missing_group_labels(data)
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
