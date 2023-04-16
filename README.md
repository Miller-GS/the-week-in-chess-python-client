# the-week-in-chess-python-client

This is a Python client for downloading weekly PGN-format chess game collections from The Week In Chess (TWIC) website, curated and maintained by Mark Crowther.

It provides a class called **TWICClient**, which has the following methods:
* get_available_pgn_game_urls: Returns a dictionary with all available PGNs for download. The key is the publishing date,
and the value is the URL of the PGN zip file.
* download_pgn_game: Given the URL of the PGN zip file, downloads it and returns its content as a string.
* download_pgn_from_date: Given the date, downloads and returns the PGN, if available.
* download_all_pgns: Downloads all available PGNs, returning them in a dictionary with dates as keys.

## Demo

The following code shows the user the 10 most recent available URLs.
Then, asks the user for the desired date, showing the entire PGN if available.

```python
from twic import TWICClient

client = TWICClient()
available_pgn_game_urls = client.get_available_pgn_game_urls()

print("Last 10 available PGN game URLs:")
for date, url in list(available_pgn_game_urls.items())[:10]:
    print(f"{date}: {url}")

desired_date = input("Enter the date of the game you want to download (YYYY-MM-DD): ")

try:
    pgn_game = client.download_pgn_from_date(desired_date)
    print(pgn_game)
except ValueError:
    print("No PGN game available for the given date.")
```

You can run it yourself in the demo folder.

# License

This project is licensed under the MIT License.