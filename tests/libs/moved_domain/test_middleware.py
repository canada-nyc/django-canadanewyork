from django.test import TestCase, Client


class TestMoveDomainMiddleware(TestCase):

    def assertNoRedirect(self, client):
        response = client.get('/artists/')
        self.assertEqual(response.status_code, 200)

    def assertClientRedirectsDomain(self, client, destination_domain):
        response = client.get('/artists/', follow=True)
        self.assertItemsEqual(
            response.redirect_chain,
            [(u'http://{}/'.format(destination_domain), 301)]
        )

    def test_no_redirect_on_same_domain(self):
        with self.settings(MOVE_DOMAIN_TARGET='some_domain'):
            self.assertNoRedirect(
                Client(HTTP_HOST='some_domain')
            )

    def test_redirect_on_different_domain(self):
        with self.settings(MOVE_DOMAIN_TARGET='some_domain'):
            self.assertClientRedirectsDomain(
                Client(HTTP_HOST='other_domain'),
                destination_domain='some_domain'
            )
