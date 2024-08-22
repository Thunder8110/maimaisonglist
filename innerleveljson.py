import json
import pathlib

DIRECTORY = pathlib.Path(__file__).parent
SCORES = [
  ["lev_bas", "lev_adv", "lev_exp", "lev_mas", "lev_remas"],
  ["dx_lev_bas", "dx_lev_adv", "dx_lev_exp", "dx_lev_mas", "dx_lev_remas"]
]

def main():
  inner_level_data = []

  with open(DIRECTORY / "maimai.json", "r", encoding="utf-8") as f:
    data = json.load(f)
    for song in data:
      if song["catcode"] == "宴会場":
        continue

      version = int(song["version"])
      sort = int(song["sort"])
      for t, types in enumerate(SCORES):
        for d, diff in enumerate(types):
          if diff not in song:
            continue
          level = song[diff]

          tentative = int(level.replace("+", "")) * 10
          if level.endswith("+"):
            tentative += 6

          inner_level_data.append({
            "version": version,
            "sort": sort,
            "type": t,
            "diff": d,
            "level": level,
            "inner_level": tentative,
            "status": 1
          })

  with open(DIRECTORY / "maimai_innerlevel_template.json", "w", encoding="utf-8") as f:
    json.dump(inner_level_data, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
  main()