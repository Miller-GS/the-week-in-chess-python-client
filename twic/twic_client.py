import requests
import chardet
import zipfile
import io
import re
import datetime


class TWICClient:
    """
    This class is used to download PGN games from the Week in Chess website.
    """

    DOWNLOAD_PAGE_URL = "https://theweekinchess.com/twic"
    BASE_ZIP_PAGE_URL = "https://theweekinchess.com/zips"

    # These headers are used to make the requests look like they are coming from a browser.
    DEFAULT_HEADERS = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
    }

    def get_available_pgn_game_urls(self) -> dict:
        """
        Returns a dictionary with the available PGN games from the Week in Chess website.
        The keys are the dates in yyyy-MM-dd format, and the values are the URLs to download the PGN games.
        """

        response = requests.get(self.DOWNLOAD_PAGE_URL, headers=self.DEFAULT_HEADERS)

        # Get the list of games from the HTML. First item from the tuple will be the ID, second will be the date.
        game_matches = re.findall(
            r"<td>(.*)</td>\s*<td>(\d{2}\/\d{2}\/\d{4})<\/td>", response.text
        )
        games = {}

        for game in game_matches:
            # Convert the date to a yyyy-MM-dd format.
            date = datetime.datetime.strptime(game[1], "%d/%m/%Y").strftime("%Y-%m-%d")
            games[date] = f"{self.BASE_ZIP_PAGE_URL}/twic{game[0]}g.zip"

        return games

    def download_pgn_game(self, url: str) -> str:
        """
        Download a PGN game from the Week in Chess website, from a specific URL.

        Returns the PGN game as a string.
        """

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
        }
        response = requests.get(url, headers=headers)
        zip_file = zipfile.ZipFile(io.BytesIO(response.content))
        pgn_content_bytes = zip_file.read(zip_file.namelist()[0])
        encoding = chardet.detect(pgn_content_bytes)["encoding"]
        pgn_content = pgn_content_bytes.decode(encoding)

        return pgn_content

    def download_pgn_from_date(self, date: str) -> str:
        """
        Download a PGN game from the Week in Chess website, from a specific date.
        The date must be in yyyy-MM-dd format.
        Returns the PGN game as a string.
        """

        available_games = self.get_available_pgn_game_urls()
        if date in available_games:
            return self.download_pgn_game(available_games[date])
        else:
            raise ValueError(f"No game found for date {date}")

    def download_all_pgns(self) -> dict:
        """
        Download all the PGN games from the Week in Chess website.
        Returns a dictionary of all the available PGN games on the Week in Chess website.
        The key is the date of the upload in yyyy-MM-dd, the value is the PGN content.
        """

        available_games = self.get_available_pgn_game_urls()
        games = {}

        for date, url in available_games.items():
            games[date] = self.download_pgn_game(url)

        return games
