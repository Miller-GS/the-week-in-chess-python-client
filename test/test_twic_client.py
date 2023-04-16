from unittest import mock, TestCase
from src.twic_client import TWICClient

class TestTWICClient(TestCase):
    def setUp(self) -> None:
        self.client = TWICClient()
        
    def test_get_available_pgn_game_urls(self):
        response = '''<html>
        <body>
            <table>
            <tr>
            <td>1478</td>
            <td>06/03/2023</td>
            </tr>
            <tr>
            <td>1477</td>
            <td>27/02/2023</td>
            </tr>
            </table>
        </body>
        </html>
        '''
        with mock.patch('src.twic_client.requests.get', return_value=mock.Mock(text=response)):
            result = self.client.get_available_pgn_game_urls()

        
        self.assertEqual(result, {
            '2023-03-06': 'https://theweekinchess.com/zips/twic1478g.zip',
            '2023-02-27': 'https://theweekinchess.com/zips/twic1477g.zip'
        })
        
