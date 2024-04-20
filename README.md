# lightdash-pre-commit
A system for Git pre-commit checks for Lightdash schema. Currently, this system is fairly limited. If you have suggestions for additional checks, please open an issue. 

## Installation
After installing pre-commit, add the following block to your `.pre-commit-config.yaml` file in the repos section. 

```yaml
  - repo: https://github.com/Cold-Bore-Capital/lightdash-pre-commit.git
    rev: 0.0.6
    hooks:
      - id: check-duplicate-dims-and-metrics
        files: ^transform\/models\/.*\.(yml|yaml)$
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

In this example, a user likely copied and pasted to create the next metric. The name `total_revenue_sum` is duplicated. 

The current version does not look across metrics and dimensions. If there is a duplicate name in a metric, and the same name is in a dimension block, it will not raise an error. This is planed for future development. 