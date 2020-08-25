import requests
from bs4 import BeautifulSoup


KEYWORD = input("比較したい商品を入力してください:\n")


"""楽天での価格を取得する"""
def get_rakuten():
    # 楽天ではURLの最後にf=2で送料無料の商品のみ表示、s=2で価格の安い順にソート
    url = "https://search.rakuten.co.jp/search/mall/" + KEYWORD + "?f=2&s=2"
    responce = requests.get(url)
    # htmlの情報を取得
    html = responce.text
    # 得られたhtmlの情報を解析
    soup = BeautifulSoup(html, "html.parser")
    # 楽天では、CSSセレクタがsearchresultitemの中に商品名が書かれていた
    items = soup.select(".searchresultitem")
    # 自分で選べるように番号を割り振る
    item_number = 1
    # 価格をリストに格納していく
    price_list = []
    for item in items:
        title = item.select_one(".title").text.replace("\n", "")
        # int型にするため数字のみのこす
        price = item.select_one(".important").text.replace(",", "").replace("円", "")
        price_list.append(price)
        print(item_number)
        print(title)
        print(price + "\n")
        item_number += 1

    selected_item_number = int(input("楽天：商品番号を入力してください：\n"))
    selected_price = int(price_list[selected_item_number - 1])
    return selected_price

"""yahooでの価格を取得する"""
def get_yahoo():
    # yahooではURLの最後にship=onで送料無料の商品のみ表示、X＝2で価格の安い順にソート
    url = "https://shopping.yahoo.co.jp/search?&p=" + KEYWORD + '&X=2&ship=on'
    responce = requests.get(url)
    html = responce.text
    soup = BeautifulSoup(html, "html.parser")
    items = soup.select(".LoopList__item")

    item_number = 1
    price_list = []
    for item in items:
        title = item.select_one(".WeRPqEQO_DMj").text.replace("\n", "")
        price = item.select_one("._3-CgJZLU91dR").text.replace(",", "").replace("円", "")
        price_list.append(price)
        print(item_number)
        print(title)
        print(price + "\n")
        item_number += 1
    selected_item_number = int(input("yahoo：商品番号を入力してください：\n"))
    selected_price = int(price_list[selected_item_number - 1])
    return selected_price

rakuten_price = get_rakuten()
print("################################")
yahoo_price = get_yahoo()

if rakuten_price > yahoo_price:
    print("yahooの方が" + str(abs(rakuten_price - yahoo_price)) + "円安いです！")

elif yahoo_price > rakuten_price:
    print("楽天の方が" + str(abs(rakuten_price - yahoo_price)) + "円安いです！")
    
else:
    print("楽天とyahooで同じ値段です")
