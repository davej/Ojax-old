import unittest
import jellybaby.providers

class MiscTests(unittest.TestCase):
    def test_providers_expand_star(self):
        expanded = jellybaby.providers.expand_star("jellybaby.providers.*")
        self.assertEqual(expanded, [
            'jellybaby.providers.delicious',
            'jellybaby.providers.flickr',
            'jellybaby.providers.gitscm',
            'jellybaby.providers.gsearch',
            'jellybaby.providers.lastfm',
            'jellybaby.providers.magnolia',
            'jellybaby.providers.svn',
            'jellybaby.providers.youtube',
        ])