import argparse
from typing import List
from typing import Optional
from typing import Sequence

import yaml


def find_missing_model_group_labels(
    data: dict, allowed_labels: Optional[List[str]] = None
) -> list:
    errors = []

    for model in data.get("models", []):
        # Check model-level 'group_label' in meta
        model_group_label = model.get("meta", {}).get("group_label")
        if not model_group_label:
            errors.append(f"Missing 'group_label' in model '{model['name']}' meta.")
        elif allowed_labels and model_group_label not in allowed_labels:
            errors.append(
                f"Invalid 'group_label' '{model_group_label}' in model '{model['name']}'. Allowed labels are: "
                f"{allowed_labels}."
            )

    return errors


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", nargs="*", help="Filenames to check")
    parser.add_argument(
        "--allowed-labels",
        type=str,
        help="Comma-separated list of allowed group labels",
    )
    args = parser.parse_args(argv)

    allowed_labels = args.allowed_labels.split(",") if args.allowed_labels else None

    error_flag = False
    for file_path in args.filenames:
        try:
            with open(file_path, "r") as file:
                data = yaml.safe_load(file)
                errors = find_missing_model_group_labels(data, allowed_labels)
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
