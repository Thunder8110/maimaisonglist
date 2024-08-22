import json
import pathlib
import rapidfuzz

GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

DIRECTORY = pathlib.Path(__file__).parent
TYPE_ARR = ["STD", "DX"]
DIFF_ARR = ["BAS", "ADV", "EXP", "MAS", "ReMAS"]

SCORE_HEADER = "".join(f"  {diff:>5s}  " for diff in [""] + DIFF_ARR)

def main():
  inner_level_data = None
  key_map = {}

  with open(DIRECTORY / "maimai_innerlevel.json", "r", encoding="utf-8") as f:
    inner_level_data = json.load(f)
    for i, score in enumerate(inner_level_data):
      key = (score["version"], score["sort"], score["type"], score["diff"])
      key_map[key] = i

  song_map = {}

  with open(DIRECTORY / "maimai.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    for song in data:
      if song["catcode"] == "宴会場":
        continue

      version = int(song["version"])
      sort = int(song["sort"])
      title = song["title"]
      artist = song["artist"]

      if title not in song_map:
        song_map[title] = {}
      song_map[title][artist] = (version, sort)

  while True:
    title = input("Title input: ")

    if title == "":
      break

    if title not in song_map:
      (title, ratio, _) = rapidfuzz.process.extract(title, song_map.keys())[0]
      if ratio < 70:
        print(f"Could not find {title}\n")
        continue

    version, sort = (None, None)
    if len(song_map[title]) == 1:
      artist = next(iter(song_map[title]))
      version, sort = song_map[title][artist]

    elif len(song_map[title]) > 1:
      artist = input("Artist input: ")

      if artist not in song_map[title]:
        (artist, ratio, _) = rapidfuzz.process.extract(artist, song_map[title].keys())[0]
        if ratio < 70:
          print(f"Could not find {artist}\n")
          continue

      version, sort = song_map[title][artist]

    score_data = [[(None, None)] * 5 for _ in range(2)]
    for type_ in range(2):
      for diff in range(5):
        key = (version, sort, type_, diff)
        if key in key_map:
          score = inner_level_data[key_map[key]]
          score_data[type_][diff] = (score["inner_level"], score["status"])

    def col(val, status):
      if status == 0:
        return f"  {GREEN}{val:>5s}{RESET}  "
      elif status == 1:
        return f"  {YELLOW}{val:>5s}{RESET}  "
      elif status == 2:
        return f"  {BLUE}{val:>5s}{RESET}  "
      else:
        return f"  {val:>5s}  "

    score_rows = [[(TYPE_ARR[type_], None)] + [(str(innerlv), status) for innerlv, status in score_data[type_]] for type_ in range(2)]
    score_display = [
      [col(val, status) for val, status in score_rows[type_]]
      for type_ in range(2)
    ]

    print()
    print(f"Title: {title}")
    print(f"Artist: {artist}")
    print(SCORE_HEADER)
    for i in range(2):
      print("".join(score_display[i]))
    print()

def green(text):
  return f"{GREEN}{text}{RESET}"

def yellow(text):
  return f"{YELLOW}{text}{RESET}"

def blue(text):
  return f"{BLUE}{text}{RESET}"

if __name__ == "__main__":
  main()