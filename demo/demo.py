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
