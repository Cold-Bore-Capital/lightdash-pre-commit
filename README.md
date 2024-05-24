# lightdash-pre-commit
A system for Git pre-commit checks for Lightdash schema. Currently, this system is fairly limited. If you have suggestions for additional checks, please open an issue.

## Installation
After installing pre-commit, add the following block to your `.pre-commit-config.yaml` file in the repos section.

```yaml
  - repo: https://github.com/Cold-Bore-Capital/lightdash-pre-commit.git
    rev: <check for latest release>
    hooks:
      - id: check-duplicate-dims-and-metrics
      - id: find_missing_metric_group_labels
      - id: find_missing_dimension_group_labels
      - id: find_incorrect_indentation_of_dims_and_metrics
      - id: find_missing_model_group_labels
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
This hook checks for missing metric group labels in the Lightdash schema.

> [!NOTE]
> If you want to skip a group label in a metric, add `skip_group_label: true` to the metric.

For example:

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
            another_metric:
              label: "Average Revenue"
              type: average
              group_label: "Revenue Metrics"
              skip_group_label: true  # This metric will not be checked
```

In this example, the metric `total_revenue_sum` is missing a `group_label`.

### find_missing_dimension_group_labels
This hook checks for missing dimension group labels in the Lightdash schema. Add `skip_group_label:true` to the dimension to skip this check.

> [!NOTE]
> This inspection will ignore any dimension with the attribute `hidden: true` or where `skip_group_label: true` is set.


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

### find_incorrect_indentation_of_dims_and_metrics
This hook looks for instances where a metric, dimension, or additional_dimension key is nested under another of the same. The Lightdash system doesn't seem to catch this, and it can have the effect of hiding a metric or dimension from the schema.

In this example, `metrics` has been nested under `additional_dimensions`:

```yaml
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
```

### find_missing_model_group_labels
This hook checks for missing group labels in model meta tags within the Lightdash schema. Optionally, it can check against a supplied list of allowed group labels.

In this example, there is no group_label attribute under the model level `meta` tag. This will throw an error.
```yaml
models:
  - name: example_model
    description: >
      This model provides example metrics.

    meta:
      label: "Example Metrics"

```

#### Check for allowed group label value
If you specify the argument `--allowed-labels`, the system will check to make sure the value of the attribute `group_label` is in the allowed list.

```yaml
models:
  - name: example_model
    description: >
      This model provides example metrics.

    meta:
      label: "Example Metrics"
      group_label: "InvalidLabel"

```

In this example, the model `example_model` has a group_label `InvalidLabel`. As this is not in the list of allowed labels, it will not pass the test.

If you want to enforce a list of allowed group labels, you can pass them using the `--allowed-labels` argument:

Example configuration in `.pre-commit-config.yaml`

```yaml
  - repo: https://github.com/Cold-Bore-Capital/lightdash-pre-commit.git
    rev: 0.0.9
    hooks:
      - id: find_missing_model_group_labels
        args: [ '--allowed-labels', 'Finance,Revenue Metrics,Customer Metrics' ]
```
