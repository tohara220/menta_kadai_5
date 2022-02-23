import pandas as pd
import datetime
import os
import eel

# 定数、変数
now = datetime.datetime.now()
ymdhms = f"{now:%Y%m%d%H%M%S}"
RECEIPT_DIR = "./receipt"
receipt_path = RECEIPT_DIR + f"/{ymdhms}.log"
sales_summary_path = "sales_summary.csv"

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
        
    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self,item_master):
        # 商品マスタ
        self.item_master=item_master
        self.item_master_code_list = []
        # オーダー
        self.item_order_list=[]
        self.item_order_quantity_list = []
        self.total_price = 0
        self.total_quantity = 0
        
    def add_item_order(self,item_code):
        '''オーダーした商品をリストに追加（商品番号のみ）'''
        self.item_order_list.append(item_code)
        
    def add_item_quantity(self, quantity):
        '''オーダー数量を記録'''
        self.item_order_quantity_list.append(quantity)
        
    def view_item_list(self):
        for item in self.item_order_list:
            print("商品コード:{}".format(item))
    
    def view_name_price(self, item_code):
        '''オーダー済み商品の名前、価格を表示する'''
        for m in self.item_master:
            if m.item_code == item_code:
                return m.item_name, m.price
            
    def view_order_list(self, item_order_list, item_order_quantity_list):
        '''オーダーした商品の一覧と合計を表示 + レシート出力'''
        # レシートの見出しを出力
        make_receipt("----------\nご注文明細")
        # 注文済み商品の商品番号と数量をループで回す
        for code, quantity in zip(item_order_list, item_order_quantity_list):
            # 商品番号より商品名と価格を呼び出す
            try:
                name, price = self.view_name_price(code)
            except:
                print(f"商品が見つかりません. code={code}")
                continue
            # テキストエリアに表示
            eel.result_js(f"[{name} ¥{price}] {quantity}個")
            # コンソールに表示
            print(f"[{name} ¥{price}] {quantity}個")
            # レシートに追記
            make_receipt(f"[{name} ¥{price}] {quantity}個")
            # 合計金額に加算
            self.total_price += (int(price) * int(quantity))
            # 合計数量に加算
            self.total_quantity += int(quantity)
            
        # テキストエリアに表示
        eel.result_js(f"[合計金額:{self.total_price}, 合計数量:{self.total_quantity}]")
        # コンソールに表示
        print(f"[合計金額:{self.total_price}, 合計数量:{self.total_quantity}]")
        # レシートに追記
        make_receipt(f"[合計金額:{self.total_price}, 合計数量:{self.total_quantity}]")
        
    def settlement(self, deposit_amount, total_price):
        '''受け取り金額の入力とお釣りの計算 + レシート追記'''
        if int(total_price) - int(deposit_amount) > 0:
            eel.oturi_js("受け取り金額が不足しています。")
        else:
            oturi = int(deposit_amount) - int(total_price)
            # テキストエリアに表示
            eel.oturi_js(f"お釣りは{oturi}円です。\nありがとうございました。")
            print(f"お釣りは{oturi}円です。\nありがとうございました。")
            # レシートに追記
            make_receipt(f"[お受け取り金額:{deposit_amount},お釣り:{oturi}]\n----------")
            # sales_sumamryがなければ作成
            if not os.path.exists(sales_summary_path):
                with open(sales_summary_path, mode="w", encoding="utf-8_sig") as f:
                    f.write("item_code, item_quantity\n")
                    
            # sales_summaryに追記する
            for item_code, item_quantity in zip(self.item_order_list, self.item_order_quantity_list):
                with open(sales_summary_path, mode="a", encoding="utf-8_sig") as f:
                    f.write(f"{item_code}, {item_quantity}\n")            
        
    def master_id_list(self):
        '''マスター（IDのみ）のリストを作成'''
        for master_elm in self.item_master:
            self.item_master_code_list.append(master_elm.item_code)
        return self.item_master_code_list
                
    def register_order(self, order_code, order_quantity, master_id_list):
        print(master_id_list)
        # 商品コードを3桁ゼロ埋め
        order_code = str(order_code).zfill(3)
        ### 入力されたデータ形式を判定する
        if not order_code.isdecimal and order_quantity.isdecimal:
            print("商品番号と個数は数値で入力してください。")
        # 入力された商品番号の存在確認
        elif order_code in master_id_list:
            # 商品番号と数量を登録
            self.add_item_order(str(order_code).zfill(2))
            self.add_item_quantity(order_quantity)
            # textareaに情報を出力
            eel.view_log_js(f"{order_code}を{order_quantity}個注文しました。")
            
            eel.view_log_js(f"[現在の注文内容]{self.item_order_list}")
        else:
            eel.view_log_js(f"[失敗]入力された値が不正のため登録に失敗しました。")
            
                
def item_master_from_csv(CSV_PATH):
    '''CSVファイルからマスタ登録する'''
    item_master = []
    df = pd.read_csv(CSV_PATH)
    print("--- 商品マスタ登録 ---")
    for code, name, price in zip(list(df["item_code"]), list(df["item_name"]), list(df["price"])):
        item_master.append(Item(str(code).zfill(3), name, price))
        print(str(code).zfill(3), name, price)
    print("--- 商品マスタ登録完了 ---")
    return item_master

def make_receipt(txt):
    with open(receipt_path, mode="a", encoding="utf-8_sig")as f:
        f.write(txt + "\n")