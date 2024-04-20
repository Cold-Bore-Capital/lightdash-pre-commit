import argparse
from typing import Optional
from typing import Sequence

import yaml


def find_missing_group_labels(data: dict) -> list:
    errors = []

    for model in data.get("models", []):
        # Check metrics at the model-level 'meta' tag
        model_level_metrics = model.get("meta", {}).get("metrics", {})
        for metric, details in model_level_metrics.items():
            if "group_label" not in details:
                errors.append(
                    f"Missing 'group_label' in model-level metric '{metric}'."
                )

        # Check metrics within the columns' 'meta' tag
        for column in model.get("columns", []):
            if "meta" in column and "metrics" in column["meta"]:
                for metric, details in column["meta"]["metrics"].items():
                    if "group_label" not in details:
                        errors.append(
                            f"Missing 'group_label' in column metric '{metric}'."
                        )

    return errors


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filenames",
        nargs="*",
        help="Check YAML files for missing 'group_label' in metrics",
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
