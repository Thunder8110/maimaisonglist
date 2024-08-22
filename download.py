import requests

def download(url):
  response = requests.get(url)
  return response.text

def main():
  url = "https://maimai.sega.jp/data/maimai_songs.json"
  data = download(url)
  open("maimai.json", "w", encoding="utf-8").write(data)

if __name__ == "__main__":
  main()