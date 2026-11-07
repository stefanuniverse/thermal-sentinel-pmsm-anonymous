import threading
import unittest
import urllib.request
import urllib.error
from http.server import ThreadingHTTPServer
from thermal_sentinel.demo import Handler

class DemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start()
        cls.base='http://127.0.0.1:'+str(cls.server.server_port)
    @classmethod
    def tearDownClass(cls):cls.server.shutdown();cls.server.server_close();cls.thread.join()
    def test_page_and_secret_paths(self):
        with urllib.request.urlopen(self.base) as response:
            self.assertEqual(response.status,200)
            self.assertIn(b'Thermal Sentinel',response.read())
        for path in ['/data/kaggle-pmsm.zip','/.env','/.git/config','/results/tnn-author.pt','/../LICENSE']:
            with self.assertRaises(urllib.error.HTTPError) as result:
                urllib.request.urlopen(self.base+path)
            self.assertEqual(result.exception.code,404)

if __name__=='__main__':unittest.main()
