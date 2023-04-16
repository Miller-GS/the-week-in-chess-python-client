from unittest import mock, TestCase
from twic.twic_client import TWICClient
import io
import zipfile


class TestTWICClient(TestCase):
    def setUp(self) -> None:
        self.client = TWICClient()

    def test_get_available_pgn_game_urls(self):
        response = """<html>
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
        """
        with mock.patch(
            "src.twic_client.requests.get", return_value=mock.Mock(text=response)
        ):
            result = self.client.get_available_pgn_game_urls()

        self.assertEqual(
            result,
            {
                "2023-03-06": "https://theweekinchess.com/zips/twic1478g.zip",
                "2023-02-27": "https://theweekinchess.com/zips/twic1477g.zip",
            },
        )

    def test_download_pgn_game(self):
        pgn_text = "PGN GAME CONTENT"

        # We need to compress the content, as the download_pgn_game method expects a zip file from the website.
        zipped_pgn = io.BytesIO()
        with zipfile.ZipFile(zipped_pgn, "w") as zip_file:
            zip_file.writestr("game.pgn", pgn_text)

        with mock.patch(
            "src.twic_client.requests.get",
            return_value=mock.Mock(content=zipped_pgn.getvalue()),
        ):
            result = self.client.download_pgn_game("https://theweekinchess.com")

        assert result == pgn_text

    def test_download_pgn_from_date(self):
        with mock.patch.object(
            self.client,
            "get_available_pgn_game_urls",
            return_value={"2020-01-01": "pgn_url"},
        ), mock.patch.object(
            self.client, "download_pgn_game", return_value="pgn_content"
        ) as download_pgn_game:
            result = self.client.download_pgn_from_date("2020-01-01")
            download_pgn_game.assert_called_once_with("pgn_url")

        assert result == "pgn_content"

    def test_download_pgn_from_date_no_pgn_available(self):
        with mock.patch.object(
            self.client, "get_available_pgn_game_urls", return_value={}
        ), mock.patch.object(
            self.client, "download_pgn_game", return_value="pgn_content"
        ), self.assertRaises(
            ValueError
        ):
            self.client.download_pgn_from_date("2020-01-01")

    def test_download_all_pgns(self):
        with mock.patch.object(
            self.client,
            "get_available_pgn_game_urls",
            return_value={
                "2020-01-01": "pgn_url_1",
                "2020-01-02": "pgn_url_2",
            },
        ), mock.patch.object(
            self.client,
            "download_pgn_game",
            side_effect=["pgn_content_1", "pgn_content_2"],
        ) as download_pgn_game:
            result = self.client.download_all_pgns()
            download_pgn_game.assert_any_call("pgn_url_1")
            download_pgn_game.assert_any_call("pgn_url_2")

        assert result == {
            "2020-01-01": "pgn_content_1",
            "2020-01-02": "pgn_content_2",
        }
