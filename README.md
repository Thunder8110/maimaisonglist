# About it

This is a list of inner levels of maimai.

## Structure

- (Array)
  - version (*)
  - sort (*)
  - type (STD: 0, DX: 1)
  - diff (BAS: 0, ADV: 1, EXP: 2, MAS: 3, ReMAS: 4)
  - level (Displayed level)
  - inner_level (Used in rating calculations, and it has been multiplied by 10; also called the constant)
  - status
    - 0: Inner level fixed.
    - 1: Inner level has not fixed.
    - 2: Inner level from previous version available.

(*): from https://maimai.sega.jp/data/maimai_songs.json

## Other informations

- Composite key for song: [version, sort]
- Composite key for score: [version, sort, type, diff]
