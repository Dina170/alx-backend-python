#!/usr/bin/env python3
"""Testing utils"""
import unittest
from unittest.mock import patch, Mock

from parameterized import parameterized

from utils import access_nested_map, get_json, memoize


class TestAccessNestedMap(unittest.TestCase):
    """access_nested_map tests"""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2)
    ])
    def test__access_nested_map(self, nested_map, path, expected):
        """test that the method returns what it is supposed to"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError)
    ])
    def test_access_nested_map_exception(self, nested_map, path, exception):
        """test that a KeyError is raised"""
        with self.assertRaises(exception):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """get_json tests"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False})
    ])
    def test_get_json(self, test_url, test_payload):
        """test that utils.get_json returns the expected result"""
        mock = Mock()
        mock.json.return_value = test_payload
        with patch("requests.get", return_value=mock):
            self.assertEqual(get_json(test_url), test_payload)
            mock.json.assert_called_once()


class TestMemoize(unittest.TestCase):
    """memorize tests"""

    def test_memoize(self):
        """Test that when calling a_property twice,
        the correct result is returned but a_method is only called once
        """

        class TestClass:
            """test class"""

            def a_method(self):
                """always returns 42"""
                return 42

            @memoize
            def a_property(self):
                """property method"""
                return self.a_method()

        with patch.object(TestClass, "a_method", return_value=42) as mock:
            test_class = TestClass()
            self.assertEqual(test_class.a_property, 42)
            self.assertEqual(test_class.a_property, 42)
            mock.assert_called_with()
