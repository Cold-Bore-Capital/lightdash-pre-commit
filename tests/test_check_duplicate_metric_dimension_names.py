import unittest
from lightdash_pre_commit.check_duplicate_metric_dimension_names import find_duplicates
import yaml

class TestDBTYAMLChecks(unittest.TestCase):
    def test_no_metrics_or_dimensions(self):
        yaml_data = """
        models:
          - columns: []
        """
        data = yaml.safe_load(yaml_data)
        errors = find_duplicates(data)
        self.assertEqual(errors, [])

    def test_unique_metric_and_dimension_names(self):
        yaml_data = """
models:
  - name: Test All Clean - No Duplicates
    meta:
      metrics:
        revenue_total:
          sql: "sum(revenue)"
        profit_total:
          sql: "sum(profit)"

    columns:
      - name: date_at
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
          metrics:
            days_in_period:
              type: number
              sql: "(datediff('day', min(date_at), max(date_at)) + 1)"
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
        errors = find_duplicates(data)
        self.assertEqual(errors, [])

    def test_duplicate_name_across_metric_and_dimension(self):
        yaml_data = """
models:
  - name: Test Duplicate Across Dim and Measures
    meta:
      metrics:
        revenue_total:
          sql: "sum(revenue)"
        profit_total:
          sql: "sum(profit)"

    columns:
      - name: date_at
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
          metrics:
            days_in_period:
              type: number
              sql: "(datediff('day', min(date_at), max(date_at)) + 1)"
      - name: revenue
        meta:
          dimension:
            hidden: true
          metrics:
            revenue_total:
              type: sum
              group_label: "Revenue"
        """
        data = yaml.safe_load(yaml_data)
        errors = find_duplicates(data)
        self.assertIn("Duplicate name 'revenue_total' used 2 times (as metrics or dimensions).", errors)

    def test_duplicate_within_metrics(self):
        yaml_data = """
models:
  - name: Test Duplicate Within Metrics
    columns:
      - name: date_at
        meta:
          dimension:
            type: date
            time_intervals: [ 'DAY', 'WEEK', 'MONTH', 'QUARTER' ]
          metrics:
            test_me:
              type: number
              sql: "(datediff('day', min(date_at), max(date_at)) + 1)"
      - name: revenue
        meta:
          dimension:
            hidden: true
          metrics:
            test_me:
              type: sum
              group_label: "Revenue"
        """
        data = yaml.safe_load(yaml_data)
        errors = find_duplicates(data)
        self.assertIn("Duplicate name 'test_me' used 2 times (as metrics or dimensions).", errors)

    def test_duplicate_within_dimensions(self):
        yaml_data = """
models:
  - name: Test Duplicate Across Dimensions
    columns:
      - name: date_at
        meta:
          dimension:
            type: date
            time_intervals: [ 'DAY', 'WEEK', 'MONTH', 'QUARTER' ]
          additional_dimensions:
            test_me:
              type: string
              sql: "abc"
              group_label: "Period Indicators"
      - name: revenue
        meta:
          dimension:
            hidden: true
          additional_dimensions:
            test_me:
              type: string
              sql: "abc"
              group_label: "Period Indicators"
        """
        data = yaml.safe_load(yaml_data)
        errors = find_duplicates(data)
        self.assertIn("Duplicate name 'test_me' used 2 times (as metrics or dimensions).", errors)


if __name__ == "__main__":
    unittest.main()
