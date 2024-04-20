import unittest

import yaml

from lightdash_pre_commit.find_missing_metric_group_labels import (
    find_missing_group_labels,
)


class TestDBTYAMLGroupLabelChecks(unittest.TestCase):
    def test_no_metrics_defined(self):
        yaml_data = """
models:
  - name: test_no_metrics_defined
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

      - name: revenue
        meta:
          dimension:
            hidden: true
        """
        data = yaml.safe_load(yaml_data)
        errors = find_missing_group_labels(data)
        self.assertEqual(errors, [])

    def test_all_metrics_have_group_label(self):
        yaml_data = """
models:
  - name: test_all_metrics_have_group_label
    meta:
      metrics:
        revenue_total:
          sql: "sum(revenue)"
          group_label: "Revenue"
        profit_total:
          sql: "sum(profit)"
          group_label: "Revenue"

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

    def test_one_metric_missing_group_label(self):
        yaml_data = """
models:
  - name: test_one_metric_missing_group_label
    meta:
      metrics:
        revenue_total:
          sql: "sum(revenue)"
          group_label: "Revenue"
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
        self.assertIn("Missing 'group_label' in column metric 'total_revenue'.", errors)

    def test_metric_in_top_level_meta_missing_group_label(self):
        yaml_data = """
models:
  - name: test_metric_in_top_level_meta_missing_group_label
    meta:
      metrics:
        revenue_total:
          sql: "sum(revenue)"
          group_label: "Revenue"
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
        self.assertIn(
            "Missing 'group_label' in model-level metric 'profit_total'.", errors
        )

    def test_multiple_metrics_missing_group_labels_across_models(self):
        yaml_data = """
models:
  - name: test_multiple_metrics_missing_group_labels_across_models
    meta:
      metrics:
        revenue_total:
          sql: "sum(revenue)"
          group_label: "Revenue"
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
        """
        data = yaml.safe_load(yaml_data)
        errors = find_missing_group_labels(data)
        expected_errors = [
            "Missing 'group_label' in model-level metric 'profit_total'.",
            "Missing 'group_label' in column metric 'days_in_period'.",
            "Missing 'group_label' in column metric 'total_revenue'.",
        ]
        self.assertEqual(errors, expected_errors)


if __name__ == "__main__":
    unittest.main()
