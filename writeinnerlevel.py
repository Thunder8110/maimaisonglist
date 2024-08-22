import json
import pathlib
import csv
import rapidfuzz

DIRECTORY = pathlib.Path(__file__).parent
DELETED = [
  "テリトリーバトル",
  "アンダーキッズ",
  "あの世行きのバスに乗ってさらば。",
  "くらべられっ子",
  "泥の分際で私だけの大切を奪おうだなんて",
]
TYPE_MAP = {"STD": 0, "DX": 1}
DIFF_MAP = {"BAS": 0, "ADV": 1, "EXP": 2, "MAS": 3, "ReMAS": 4}

def main():
  inner_level_data = None
  key_map = {}

  with open(DIRECTORY / "maimai_innerlevel_template.json", "r", encoding="utf-8") as f:
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

  with open(DIRECTORY / "innerlevel.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    for row in reader:
      (title, type_, diff, prev_inner, inner_level) = row

      if title in DELETED:
        continue

      artist = None

      if title not in song_map:
        if title == "Link_N":
          title = "Link"
          artist = "Circle of friends(天月-あまつき-・un:c・伊東歌詞太郎・コニー・はしやん)"
        elif title == "Link_M":
          title = "Link"
          artist = "Clean Tears feat. Youna"
        else:
          (title, ratio, _) = rapidfuzz.process.extract(title, song_map.keys())[0]
          if ratio < 70:
            print(f"Could not find {title}")
            continue
          # print(f"Corrected {title}")

      version, sort = (None, None)
      if len(song_map[title]) == 1:
        artist = list(song_map[title].keys())[0]
        version, sort = song_map[title][artist]
      if len(song_map[title]) > 1:
        version, sort = song_map[title][artist]

      id_ = key_map[(version, sort, TYPE_MAP[type_], DIFF_MAP[diff])]

      prev_inner_num = None
      try:
        prev_inner_num = int(float(prev_inner) * 10)
      except ValueError:
        pass

      inner_level_num = None
      try:
        inner_level_num = int(float(inner_level) * 10)
      except ValueError:
        pass

      if inner_level_num is None:
        if prev_inner_num is None:
          pass
        else: # prev_inner_num is not None
          inner_level_data[id_]["inner_level"] = prev_inner_num
          inner_level_data[id_]["status"] = 2
      else: # inner_level_num is not None
        inner_level_data[id_]["inner_level"] = inner_level_num
        inner_level_data[id_]["status"] = 0

  with open(DIRECTORY / "maimai_innerlevel.json", "w", encoding="utf-8") as f:
    json.dump(inner_level_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
  main()