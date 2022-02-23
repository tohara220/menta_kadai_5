import datetime
import os
import eel

import desktop
import pos

# 基本設定
now = datetime.datetime.now()
ymdhms = f"{now:%Y%m%d%H%M%S}"
CSV_PATH = "item_master.csv"
RECEIPT_DIR = "./receipt"
receipt_path = RECEIPT_DIR + f"/{ymdhms}.log"

# アプリケーションの設定
app_name="html"
end_point="index.html"
size=(700,600)

@ eel.expose
def make_instance():
    '''マスタ登録
    起動と同時に実行する'''
    # グローバル変数の設定
    # global order
    # # レシートを格納するフォルダを作成
    # os.makedirs(RECEIPT_DIR, exist_ok=True)
    # # csvファイルからアイテムマスターを登録
    # item_master = pos.item_master_from_csv(CSV_PATH)
    # # オーダークラスのインスタンス化
    # order = pos.Order(item_master)
    # order.master_id_list()
    
@ eel.expose
def read_master(input_csv):
    """CSVの登録ボタンをクリックで起動"""
    # グローバル変数の設定
    global order
    # レシートを格納するフォルダを作成
    os.makedirs(RECEIPT_DIR, exist_ok=True)
    # csvファイルからアイテムマスターを登録
    item_master = pos.item_master_from_csv(input_csv)
    # オーダークラスのインスタンス化
    order = pos.Order(item_master)
    order.master_id_list()
    

@ eel.expose
def register_order(item_code, item_quantity):
    '''オーダーをhtmlから登録'''
    try:
        master_id_list = order.master_id_list()
        order.register_order(item_code, item_quantity, master_id_list)
    except:
        eel.view_log_js(f"CSVファイルを読み込ませてください。")
    
@ eel.expose
def confirm_order():
    print("--- ご注文明細 ---")
    order.view_order_list(order.item_order_list, order.item_order_quantity_list)
    
@ eel.expose
def settlement(deposit_amount):
    order.settlement(deposit_amount, order.total_price)
    
desktop.start(app_name,end_point,size)
#desktop.start(size=size,appName=app_name,endPoint=end_point)