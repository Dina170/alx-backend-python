#!/usr/bin/env python3
"""Testing client"""
import unittest
from unittest.mock import patch, PropertyMock

from parameterized import parameterized, parameterized_class

from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """GithubOrgClient tests"""

    @parameterized.expand([
        ("google", {"google": True}),
        ("abc", {"abc": True})
    ])
    @patch('client.get_json')
    def test_org(self, org, expected, mock):
        """tests that GithubOrgClient.org returns the correct value"""
        org_client = GithubOrgClient(org)
        mock.return_value = expected
        self.assertEqual(org_client.org, expected)
        mock.assert_called_once_with("https://api.github.com/orgs/" + org)

    def test_public_repos_url(self):
        """tests the _public_repos_url property."""
        with patch("client.GithubOrgClient.org",
                   new_callable=PropertyMock) as mock:
            mock.return_value = {
                'repos_url': "https://api.github.com/users/google/repos"
            }
            self.assertEqual(GithubOrgClient("google")._public_repos_url,
                             "https://api.github.com/users/google/repos")

    @patch('client.get_json')
    def test_public_repos(self, mock):
        """tests GithubOrgClient.public_repos"""
        json_payload = {
            'repos_url': "https://api.github.com/users/google/repos",
            'repos': [{"name": "repo1"}, {"name": "repo2"}]
        }
        mock.return_value = json_payload['repos']

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_response:
            mock_response.return_value = json_payload['repos_url']
            repos = GithubOrgClient('google').public_repos()

            check = [i["name"] for i in json_payload['repos']]
            self.assertEqual(repos, check)

            mock_response.assert_called_once()
            mock.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected):
        """tests GithubOrgClient.has_license"""
        self.assertEqual(GithubOrgClient.has_license(repo, license_key),
                         expected)


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """Integration tests of fixtures """

    @classmethod
    def setUpClass(cls):
        """mocks requests.get to return example payloads
        found in the fixtures"""
        side_eff = {
            'return_value.json.side_effect': [
                cls.org_payload, cls.repos_payload,
                cls.org_payload, cls.repos_payload
            ]
        }
        cls.get_patcher = patch('requests.get', **side_eff)
        cls.mock = cls.get_patcher.start()

    def test_public_repos(self):
        """tests the public_repos method to return
        the expected results based on the fixtures"""
        self.assertEqual(GithubOrgClient("google").public_repos(),
                         self.expected_repos)

    def test_public_repos_with_license(self):
        """tests the public_repos method with a license."""
        self.assertEqual(
            GithubOrgClient("google").public_repos(license="apache-2.0"),
            self.apache2_repos,
        )

    @classmethod
    def tearDownClass(cls):
        """stops the patcher"""
        cls.get_patcher.stop()
