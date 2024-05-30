import unittest

import yaml

from lightdash_pre_commit.utils import has_dimensions
from lightdash_pre_commit.utils import has_metrics


class TestHasDimensions(unittest.TestCase):
    def test_has_dimensions_true(self):
        yaml_data = """
        models:
          - name: model_with_dimensions
            columns:
              - name: column_with_dimension
                meta:
                  dimension:
                    type: string
        """
        data = yaml.safe_load(yaml_data)
        self.assertTrue(has_dimensions(data))

    def test_has_dimensions_false(self):
        yaml_data = """
        models:
          - name: model_without_dimensions
            columns:
              - name: column_without_dimension
        """
        data = yaml.safe_load(yaml_data)
        self.assertFalse(has_dimensions(data))

    def test_unsupported_resource_type(self):
        yaml_data = """
        exposures:
          - name: unsupported
        """
        data = yaml.safe_load(yaml_data)
        with self.assertRaises(ValueError):
            has_dimensions(data)


class TestHasMetrics(unittest.TestCase):
    def test_has_metrics_true(self):
        yaml_data = """
        models:
          - name: model_with_metrics
            columns:
              - name: column_with_metric
                meta:
                  metrics:
                    test_sum:
                      type: sum
        """
        data = yaml.safe_load(yaml_data)
        self.assertTrue(has_metrics(data))

    def test_has_metrics_false(self):
        yaml_data = """
        models:
          - name: model_without_metrics
            columns:
              - name: column_without_metric
        """
        data = yaml.safe_load(yaml_data)
        self.assertFalse(has_metrics(data))

    def test_unsupported_resource_type(self):
        yaml_data = """
        exposures:
          - name: unsupported
        """
        data = yaml.safe_load(yaml_data)
        with self.assertRaises(ValueError):
            has_metrics(data)
