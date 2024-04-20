import yaml
import sys


def find_duplicates(data):
    metric_names = {}
    dimension_names = {}
    errors = []

    for model in data.get('models', []):
        for column in model.get('columns', []):
            # Process regular dimensions
            if 'meta' in column and 'dimension' in column['meta']:
                dim_label = column['meta']['dimension'].get('label')
                if dim_label is not None:
                    dimension_names[dim_label] = dimension_names.get(dim_label, 0) + 1

            # Process additional dimensions
            if 'meta' in column and 'additional_dimensions' in column['meta']:
                for key in column['meta']['additional_dimensions']:
                    if key is not None:
                        dimension_names[key] = dimension_names.get(key, 0) + 1

            # Process metrics
            if 'meta' in column and 'metrics' in column['meta']:
                for metric in column['meta']['metrics']:
                    if metric is not None:
                        metric_names[metric] = metric_names.get(metric, 0) + 1

    # Check for duplicates and gather error messages
    for name, count in metric_names.items():
        if count > 1:
            errors.append(f"Duplicate metric name '{name}' found {count} times.")

    for name, count in dimension_names.items():
        if count > 1:
            errors.append(f"Duplicate dimension name '{name}' found {count} times.")

    return errors


def main(file_paths):
    for file_path in file_paths:
        try:
            with open(file_path, 'r') as file:
                data = yaml.safe_load(file)
                errors = find_duplicates(data)
                if errors:
                    print(f"Errors found in '{file_path}':")
                    for error in errors:
                        print(error)
                    sys.exit(1)

        except Exception as e:
            print(f"Failed to process '{file_path}': {e}")
            sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
