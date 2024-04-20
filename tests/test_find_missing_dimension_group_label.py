import unittest

import yaml

from lightdash_pre_commit.find_missing_dimension_group_labels import (
    find_missing_group_labels,
)


class TestDBTYAMLGroupLabelChecks(unittest.TestCase):
    def test_no_dimensions_defined(self):
        yaml_data = """
models:
  - name: test_no_dimensions_defined
    columns:
      - name: date_at
      - name: revenue
        """
        data = yaml.safe_load(yaml_data)
        errors = find_missing_group_labels(data)
        self.assertEqual(errors, [])

    def test_all_dimensions_have_group_label(self):
        yaml_data = """
models:
  - name: test_all_dimensions_have_group_label
    columns:
      - name: date_at
        meta:
          dimension:
            type: date
            time_intervals: [ 'DAY', 'WEEK', 'MONTH', 'QUARTER' ]
            group_label: "Time"
          additional_dimensions:
            period_7_days:
              type: string
              sql: "abc"
              group_label: "Period Indicators"
            period_28_days:
              type: string
              sql: "abc"
              group_label: "Period Indicators"
          metrics:
            days_in_period:
              type: number
              sql: "(datediff('day', min(date_at), max(date_at)) + 1)"
              group_label: "Revenue"
      - name: revenue
        meta:
          dimension:
            hidden: true
          metrics:
            total_revenue:
              type: sum
              group_label: "Revenue"
        """
        data = yaml.safe_load(yaml_data)
        errors = find_missing_group_labels(data)
        self.assertEqual(errors, [])

    def test_skip_group_label_attribute(self):
        yaml_data = """
models:
  - name: test_all_dimensions_have_group_label
    columns:
      - name: date_at
        meta:
          dimension:
            type: date
            time_intervals: [ 'DAY', 'WEEK', 'MONTH', 'QUARTER' ]
            group_label: "Time"
          additional_dimensions:
            period_7_days:
              type: string
              sql: "abc"
              group_label: "Period Indicators"
            period_28_days:
              type: string
              sql: "abc"
              group_label: "Period Indicators"
          metrics:
            days_in_period:
              type: number
              sql: "(datediff('day', min(date_at), max(date_at)) + 1)"
              skip_group_label: true
      - name: revenue
        meta:
          dimension:
            hidden: true
          metrics:
            total_revenue:
              type: sum
              group_label: "Revenue"
        """
        data = yaml.safe_load(yaml_data)
        errors = find_missing_group_labels(data)
        self.assertEqual(errors, [])

    def test_one_dimension_missing_group_label(self):
        yaml_data = """
models:
  - name: test_one_dimension_missing_group_label

    columns:
      - name: date_at  # Missing group label in this top level dimension
        meta:
          dimension:
            type: date
            time_intervals: [ 'DAY', 'WEEK', 'MONTH', 'QUARTER' ]
          additional_dimensions:
            period_7_days:
              type: string
              sql: "abc"
              group_label: "Period Indicators"
            period_28_days:
              type: string
              sql: "abc"
              group_label: "Period Indicators"
          metrics:
            days_in_period:
              type: number
              sql: "(datediff('day', min(date_at), max(date_at)) + 1)"
              group_label: "Revenue"
      - name: revenue
        meta:
          dimension:
            hidden: true
          metrics:
            total_revenue:
              type: sum
        """
        data = yaml.safe_load(yaml_data)
        errors = find_missing_group_labels(data)
        self.assertIn("Missing 'group_label' in dimension of column 'date_at'.", errors)

    def test_multiple_dimensions_missing_group_labels_across_models(self):
        yaml_data = """
models:
  - name: test_multiple_dimensions_missing_group_labels_across_models

    columns:
      - name: date_at  # Missing group label in this top level dimension
        meta:
          dimension:
            type: date
            time_intervals: [ 'DAY', 'WEEK', 'MONTH', 'QUARTER' ]
          additional_dimensions:
            period_7_days:
              type: string
              sql: "abc"
              group_label: "Period Indicators"
            period_28_days:
              type: string
              sql: "abc"
              group_label: "Period Indicators"
          metrics:
            days_in_period:
              type: number
              sql: "(datediff('day', min(date_at), max(date_at)) + 1)"
              group_label: "Revenue"
      - name: revenue
        meta:
          dimension:
            type: number
          metrics:
            total_revenue:
              type: sum
        """
        data = yaml.safe_load(yaml_data)
        errors = find_missing_group_labels(data)
        expected_errors = [
            "Missing 'group_label' in dimension of column 'date_at'.",
            "Missing 'group_label' in dimension of column 'revenue'.",
        ]
        self.assertEqual(errors, expected_errors)

    def test_missing_group_label_in_additional_dimensions(self):
        yaml_data = """
models:
  - name: test_missing_group_label_in_additional_dimensions

    columns:
      - name: date_at  # Missing group label in this top level dimension
        meta:
          dimension:
            type: date
            time_intervals: [ 'DAY', 'WEEK', 'MONTH', 'QUARTER' ]
          additional_dimensions:
            period_7_days:
              type: string
              sql: "abc"
              group_label: "Period Indicators"
            period_28_days:
              type: string
              sql: "abc"
              group_label: "Period Indicators"
          metrics:
            days_in_period:
              type: number
              sql: "(datediff('day', min(date_at), max(date_at)) + 1)"
              group_label: "Revenue"
      - name: revenue
        meta:
          dimension:
            hidden: true
          metrics:
            total_revenue:
              type: sum
        """
        data = yaml.safe_load(yaml_data)
        errors = find_missing_group_labels(data)
        self.assertIn("Missing 'group_label' in dimension of column 'date_at'.", errors)


if __name__ == "__main__":
    unittest.main()
