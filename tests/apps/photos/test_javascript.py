from ...utils import Selenium2OnSauce


class TestPhotoJavascript(Selenium2OnSauce):
    def test_remote(self):
        self.driver.get('google.com')

    def test_local(self):
        self.driver.get('%s%s' % (self.live_server_url, '/artists'))
