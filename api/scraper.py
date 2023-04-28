import requests
import bs4

class Scraper():
    def google_search(self, search_keyword):
        # 指定したキーワードで検索
        search_url = 'https://www.google.co.jp/search?q='+search_keyword
        search_response = requests.get(search_url)

        # 検索結果をパース
        soup = bs4.BeautifulSoup(search_response.text, 'lxml')
        parsed_page = soup.select('div.kCrYT>a')

        # タイトル、URLの抽出
        items = []
        rank = 1
        for site in parsed_page:
            item = {
                'rank': rank,
                'title': site.select('h3.zBAuLc')[0].text,
                'url': site.get('href').split(
                    '&sa=U&')[0].replace('/url?q=', '')
            }
            rank += 1
            items.append(item)
        return items