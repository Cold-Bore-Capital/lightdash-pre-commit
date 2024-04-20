# lightdash-pre-commit
A system for Git pre-commit checks for Lightdash schema. Currently, this system is fairly limited. If you have suggestions for additional checks, please open an issue.

## Installation
After installing pre-commit, add the following block to your `.pre-commit-config.yaml` file in the repos section.

```yaml
  - repo: https://github.com/Cold-Bore-Capital/lightdash-pre-commit.git
    rev: 0.0.6
    hooks:
      - id: check-duplicate-dims-and-metrics
      - id: find_missing_metric_group_labels
      - id: find_missing_dimension_group_labels
```

## Hooks

### check-duplicate-dims-and-metrics
This hook checks for duplicate dimensions and metrics in the Lightdash schema. This can happen when copying and pasting between dimensions. For example:

```yaml
      - name: total_revenue
        description: "Total revenue from all services."
        meta:
          dimension:
            hidden: true
          metrics:
            total_revenue_sum:
              label: "Total Revenue"
              type: sum

      - name: medical_revenue
        description: "Total revenue from medical services."
        meta:
          dimension:
            hidden: true
          metrics:
            total_revenue_sum:
              label: "Medical Revenue"
              type: sum
```

In this example, a user likely copied and pasted to create the next metric. The name `total_revenue_sum` is duplicated. The hook will look within non-column metrics, additional_dimensions, and column metrics and dimensions.

### find_missing_metric_group_labels
This hook checks for missing metric group labels in the Lightdash schema. For example:

```yaml
      - name: total_revenue
        description: "Total revenue from all services."
        meta:
          dimension:
            hidden: true
          metrics:
            total_revenue_sum:
              label: "Total Revenue"
              type: sum
            average_revenue:
              label: "Average Revenue"
              type: average
              group_label: "Revenue Metrics"
```

In this example, the metric `total_revenue_sum` is missing a `group_label`.

### find_missing_dimension_group_labels
This hook checks for missing dimension group labels in the Lightdash schema.

> [!NOTE]
> Note, this inspection will ignore any dimension with the attribute `hidden: true`.


For example:

```yaml
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
```

In this example, the meta level dimension `date` and the column dimension `revenue` are missing the `group_label` attribute.
