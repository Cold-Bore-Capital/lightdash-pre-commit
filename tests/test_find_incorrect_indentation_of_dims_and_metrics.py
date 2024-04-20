import unittest

import yaml

from lightdash_pre_commit.find_incorrect_indentation_of_dims_and_metrics import (
    find_indentation_issues,
)


class TestDBTIndentationIssues(unittest.TestCase):
    def test_no_indentation_issues(self):
        yaml_data = """
models:
  - name: ProperlyIndentedModel
    columns:
      - name: date_at
        meta:
          dimension:
            type: date
            label: "Date At"
            time_intervals: ['DAY', 'WEEK', 'MONTH', 'QUARTER']
            group_label: "Date Dimensions"
          additional_dimensions:
            period_7_days:
              type: string
              label: "Period - 7 Days"
              sql: "SQL_QUERY_HERE"
              group_label: "Period Indicators"
        """
        data = yaml.safe_load(yaml_data)
        errors = find_indentation_issues(data)
        self.assertEqual(errors, [])

    def test_metrics_under_additional_dimensions(self):
        yaml_data = """
models:
  - name: MetricsUnderAdditionalDimensions
    columns:
      - name: date_at
        meta:
          additional_dimensions:
            period_7_days:
              type: string
              label: "Period - 7 Days"
              sql: "SQL_QUERY_HERE"
              group_label: "Period Indicators"
            metrics:
              days_in_period:
                type: number
                label: "Days in Period"
                sql: "SQL_QUERY_HERE"
                group_label: "Period Indicators"
        """
        data = yaml.safe_load(yaml_data)
        errors = find_indentation_issues(data)
        self.assertEqual(len(errors), 1)
        self.assertIn(
            "Incorrect indent: 'metrics' should not be a child of 'additional_dimensions'",
            errors[0],
        )

    def test_additional_dimensions_under_dimension(self):
        yaml_data = """
models:
  - name: AdditionalDimensionsUnderDimension
    columns:
      - name: revenue
        meta:
          dimension:
            type: number
            label: "Revenue"
            additional_dimensions:
              revenue_by_type:
                type: string
                label: "Revenue By Type"
                sql: "SQL_QUERY_HERE"
                group_label: "Revenue Metrics"
        """
        data = yaml.safe_load(yaml_data)
        errors = find_indentation_issues(data)
        self.assertEqual(len(errors), 1)
        self.assertIn(
            "Incorrect indent: 'additional_dimensions' should not be a child of 'dimension'",
            errors[0],
        )

    def test_metrics_under_dimension(self):
        yaml_data = """
models:
  - name: MetricsUnderDimension
    columns:
      - name: revenue
        meta:
          dimension:
            type: number
            label: "Revenue"
            metrics:
              total_revenue:
                type: sum
                sql: "SQL_QUERY_HERE"
                group_label: "Total Revenue"
        """
        data = yaml.safe_load(yaml_data)
        errors = find_indentation_issues(data)
        self.assertEqual(len(errors), 1)
        self.assertIn(
            "Incorrect indent: 'metrics' should not be a child of 'dimension'",
            errors[0],
        )


if __name__ == "__main__":
    unittest.main()
