import unittest

import yaml

from lightdash_pre_commit.find_missing_model_group_labels import (
    find_missing_model_group_labels,
)


class TestFindMissingModelGroupLabels(unittest.TestCase):

    def test_model_with_group_label(self):
        yaml_data = """
models:
  - name: test_model_with_group_label
    meta:
      group_label: "Finance"
    columns:
      - name: date_at
        meta:
          dimension:
            type: date
            time_intervals: [ 'DAY', 'WEEK', 'MONTH', 'QUARTER' ]
      - name: revenue
        meta:
          dimension:
            hidden: true
        """
        data = yaml.safe_load(yaml_data)
        errors = find_missing_model_group_labels(data)
        self.assertEqual(errors, [])

    def test_model_missing_group_label(self):
        yaml_data = """
models:
  - name: test_model_missing_group_label
    meta:
      label: "Finance Metrics"
    columns:
      - name: date_at
        meta:
          dimension:
            type: date
            time_intervals: [ 'DAY', 'WEEK', 'MONTH', 'QUARTER' ]
      - name: revenue
        meta:
          dimension:
            hidden: true
        """
        data = yaml.safe_load(yaml_data)
        errors = find_missing_model_group_labels(data)
        self.assertIn(
            "Missing 'group_label' in model 'test_model_missing_group_label' meta.",
            errors,
        )

    def test_model_invalid_group_label(self):
        yaml_data = """
models:
  - name: test_model_invalid_group_label
    meta:
      group_label: "InvalidLabel"
    columns:
      - name: date_at
        meta:
          dimension:
            type: date
            time_intervals: [ 'DAY', 'WEEK', 'MONTH', 'QUARTER' ]
      - name: revenue
        meta:
          dimension:
            hidden: true
        """
        data = yaml.safe_load(yaml_data)
        errors = find_missing_model_group_labels(
            data, allowed_labels=["Finance", "Practice", "Customers", "Marketing"]
        )
        self.assertIn(
            "Invalid 'group_label' 'InvalidLabel' in model 'test_model_invalid_group_label'. Allowed labels "
            "are: ['Finance', 'Practice', 'Customers', 'Marketing'].",
            errors,
        )

    def test_model_with_valid_metrics_group_label(self):
        yaml_data = """
models:
  - name: test_model_with_valid_metrics_group_label
    meta:
      group_label: "Finance"
      metrics:
        total_revenue:
          sql: "sum(revenue)"
          group_label: "MetricsGroup"
    columns:
      - name: date_at
        meta:
          dimension:
            type: date
            time_intervals: [ 'DAY', 'WEEK', 'MONTH', 'QUARTER' ]
        """
        data = yaml.safe_load(yaml_data)
        errors = find_missing_model_group_labels(
            data,
            allowed_labels=[
                "Finance",
                "Practice",
                "Customers",
                "Marketing",
                "MetricsGroup",
            ],
        )
        self.assertEqual(errors, [])

    def test_model_with_invalid_metrics_group_label_doesnt_raise_error(self):
        yaml_data = """
models:
  - name: test_model_with_invalid_metrics_group_label
    meta:
      group_label: "Finance"

      metrics:
        total_revenue:
          sql: "sum(revenue)"
          group_label: "InvalidMetricsGroup"
    columns:
      - name: date_at
        meta:
          dimension:
            type: date
            time_intervals: [ 'DAY', 'WEEK', 'MONTH', 'QUARTER' ]
        """
        data = yaml.safe_load(yaml_data)
        errors = find_missing_model_group_labels(
            data, allowed_labels=["Finance", "Practice", "Customers", "Marketing"]
        )
        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
