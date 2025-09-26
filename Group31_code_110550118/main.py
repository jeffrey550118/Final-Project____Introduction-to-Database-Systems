import tkinter as tk
from PIL import Image, ImageTk
import psycopg2


def open_second_window_on_click(NAME, rs):
    second_window = tk.Toplevel(root)
    if rs == 1 or rs == 2:
        second_window.title(f"{NAME}(稀有{rs})-圖片")
    else:
        second_window.title(f"{NAME}-圖片")
    second_window.geometry("500x500")

    img = Image.open(f"菇菇栽培圖片/{NAME}{rs}.png")
    photo = ImageTk.PhotoImage(img)
    second_label = tk.Label(second_window, image=photo)
    second_label.image = photo 
    second_label.pack()

def menu_select(str):
    if str == "請":
        return "0"
    else:
        return str
    
def show_star(Rarity):
    star = ""
    if Rarity == 1:
        star = "★☆☆☆☆"
    elif Rarity == 2:
        star = "★★☆☆☆"
    elif Rarity == 3:
        star = "★★★☆☆"
    elif Rarity == 4:
        star = "★★★★☆"
    elif Rarity == 5:
        star = "★★★★★"
    
    return star

def insert_image(text_widget, image_path):
    img = Image.open(image_path)
    img = img.resize((200, 200))
    photo = ImageTk.PhotoImage(img)
    text_widget.photo = photo
    text_widget.image_create(tk.END, image=photo)
    text_widget.insert(tk.END, '\n')

def search_all_mushrooms():
    # 建立連接
    # 有帳密資訊，故移除

    # 建立遊標
    cur = conn.cursor()

    # 搜尋所有菇菇
    cur.execute("SELECT * FROM mushroom_dictionary order by theme_id, id, rare_state asc")
    mushroom_data = cur.fetchall()
    mushroom_info_text.delete('1.0', tk.END)  # 清空Text區域

    # 顯示菇菇列表到UI中
    for data in mushroom_data:
        if data[4] == 1 or data[4] == 2:
            mushroom_info_text.insert(tk.END, f"菇菇名稱: {data[3]}(稀有{data[4]})\n栽培主題: {data[1]}\n編號: {data[2]}\n")
        else:
            mushroom_info_text.insert(tk.END, f"菇菇名稱: {data[3]}\n栽培主題: {data[1]}\n編號: {data[2]}\n")
        mushroom_info_text.insert(tk.END, f"賣價: {data[6]} NP\n")
        mushroom_info_text.insert(tk.END, f"稀有度: {show_star(data[5])}\n")
        mushroom_info_text.tag_configure(f"圖片{data[3]}{data[4]}", foreground="blue", underline=True)
        mushroom_info_text.tag_bind(f"圖片{data[3]}{data[4]}", "<Button-1>", lambda event, name=data[3], rs=data[4]: open_second_window_on_click(name, rs))
        if data[4] == 1 or data[4] == 2:
            mushroom_info_text.insert(tk.END, f"{data[3]}(稀有{data[4]})-圖片\n", f"圖片{data[3]}{data[4]}")
        else:
            mushroom_info_text.insert(tk.END, f"{data[3]}-圖片\n", f"圖片{data[3]}{data[4]}")
        mushroom_info_text.insert(tk.END, f"----------------------\n")

    # 關閉遊標和連接
    cur.close()
    conn.close()

def search_mushrooms_by_name():
    # 建立連接
    # 有帳密資訊，故移除

    # 建立遊標
    cur = conn.cursor()

    # 搜尋菇菇
    mushroom_name = search_name_entry.get()  # 獲取輸入的菇菇名稱
    mushroom_name = "%" + mushroom_name + "%"
    cur.execute("SELECT * FROM mushroom_dictionary WHERE name like %s order by theme_id, id, rare_state asc;", (mushroom_name,))
    mushroom_data = cur.fetchall()

    # 顯示菇菇列表到UI中
    if mushroom_data and (mushroom_name != "%" + "%"):
        mushroom_info_text.delete('1.0', tk.END)  # 清空Text區域
        for data in mushroom_data:
            if data[4] == 1 or data[4] == 2:
                mushroom_info_text.insert(tk.END, f"菇菇名稱: {data[3]}(稀有{data[4]})\n栽培主題: {data[1]}\n編號: {data[2]}\n")
            else:
                mushroom_info_text.insert(tk.END, f"菇菇名稱: {data[3]}\n栽培主題: {data[1]}\n編號: {data[2]}\n")
            mushroom_info_text.insert(tk.END, f"賣價: {data[6]} NP\n")
            mushroom_info_text.insert(tk.END, f"稀有度: {show_star(data[5])}\n")
            mushroom_info_text.tag_configure(f"圖片{data[3]}{data[4]}", foreground="blue", underline=True)
            mushroom_info_text.tag_bind(f"圖片{data[3]}{data[4]}", "<Button-1>", lambda event, name=data[3], rs=data[4]: open_second_window_on_click(name, rs))
            if data[4] == 1 or data[4] == 2:
                mushroom_info_text.insert(tk.END, f"{data[3]}(稀有{data[4]})-圖片\n", f"圖片{data[3]}{data[4]}")
            else:
                mushroom_info_text.insert(tk.END, f"{data[3]}-圖片\n", f"圖片{data[3]}{data[4]}")
            mushroom_info_text.insert(tk.END, f"----------------------\n")
    else:
        mushroom_info_text.delete('1.0', tk.END)
        mushroom_info_text.insert(tk.END, "無搜尋結果")

    # 關閉遊標和連接
    cur.close()
    conn.close()

def search_mushrooms_by_theme():
    # 建立連接
    # 有帳密資訊，故移除

    # 建立遊標
    cur = conn.cursor()

    # 搜尋菇菇
    mushroom_theme_name = search_theme_entry.get()  # 獲取輸入的栽培主題名稱
    mushroom_theme_name = "%" + mushroom_theme_name + "%"
    cur.execute("SELECT * FROM mushroom_dictionary WHERE theme_name like %s order by theme_id, id, rare_state asc;", (mushroom_theme_name,))
    mushroom_data = cur.fetchall()

    # 顯示菇菇列表到UI中
    if mushroom_data and (mushroom_theme_name != "%" + "%"):
        mushroom_info_text.delete('1.0', tk.END)  # 清空Text區域
        if mushroom_theme_name != "%" + "%":
            cur.execute("SELECT * FROM mushroom_dictionary WHERE theme_name = 'all' order by theme_id, id, rare_state asc;")
            mushroom_data2 = cur.fetchall()
            for data in mushroom_data2:
                if data[4] == 1 or data[4] == 2:
                    mushroom_info_text.insert(tk.END, f"菇菇名稱: {data[3]}(稀有{data[4]})\n栽培主題: {data[1]}\n編號: {data[2]}\n")
                else:
                    mushroom_info_text.insert(tk.END, f"菇菇名稱: {data[3]}\n栽培主題: {data[1]}\n編號: {data[2]}\n")
                mushroom_info_text.insert(tk.END, f"賣價: {data[6]} NP\n")
                mushroom_info_text.insert(tk.END, f"稀有度: {show_star(data[5])}\n")
                mushroom_info_text.tag_configure(f"圖片{data[3]}{data[4]}", foreground="blue", underline=True)
                mushroom_info_text.tag_bind(f"圖片{data[3]}{data[4]}", "<Button-1>", lambda event, name=data[3], rs=data[4]: open_second_window_on_click(name, rs))
                if data[4] == 1 or data[4] == 2:
                    mushroom_info_text.insert(tk.END, f"{data[3]}(稀有{data[4]})-圖片\n", f"圖片{data[3]}{data[4]}")
                else:
                    mushroom_info_text.insert(tk.END, f"{data[3]}-圖片\n", f"圖片{data[3]}{data[4]}")
                mushroom_info_text.insert(tk.END, f"----------------------\n")
        for data in mushroom_data:
            if data[4] == 1 or data[4] == 2:
                mushroom_info_text.insert(tk.END, f"菇菇名稱: {data[3]}(稀有{data[4]})\n栽培主題: {data[1]}\n編號: {data[2]}\n")
            else:
                mushroom_info_text.insert(tk.END, f"菇菇名稱: {data[3]}\n栽培主題: {data[1]}\n編號: {data[2]}\n")
            mushroom_info_text.insert(tk.END, f"賣價: {data[6]} NP\n")
            mushroom_info_text.insert(tk.END, f"稀有度: {show_star(data[5])}\n")
            mushroom_info_text.tag_configure(f"圖片{data[3]}{data[4]}", foreground="blue", underline=True)
            mushroom_info_text.tag_bind(f"圖片{data[3]}{data[4]}", "<Button-1>", lambda event, name=data[3], rs=data[4]: open_second_window_on_click(name, rs))
            if data[4] == 1 or data[4] == 2:
                mushroom_info_text.insert(tk.END, f"{data[3]}(稀有{data[4]})-圖片\n", f"圖片{data[3]}{data[4]}")
            else:
                mushroom_info_text.insert(tk.END, f"{data[3]}-圖片\n", f"圖片{data[3]}{data[4]}")
            mushroom_info_text.insert(tk.END, f"----------------------\n")
            
    else:
        mushroom_info_text.delete('1.0', tk.END)
        mushroom_info_text.insert(tk.END, "無搜尋結果")

    # 關閉遊標和連接
    cur.close()
    conn.close()

def search_mushrooms_by_rarity(Rarity):
    # 建立連接
    # 有帳密資訊，故移除

    # 建立遊標
    cur = conn.cursor()

    # 搜尋菇菇
    cur.execute("SELECT * FROM mushroom_dictionary WHERE rarity = " + str(Rarity) + " order by theme_id, id, rare_state asc;")
    mushroom_data = cur.fetchall()

    # 顯示菇菇列表到UI中
    if mushroom_data:
        mushroom_info_text.delete('1.0', tk.END)  # 清空Text區域
        for data in mushroom_data:
            if data[4] == 1 or data[4] == 2:
                mushroom_info_text.insert(tk.END, f"菇菇名稱: {data[3]}(稀有{data[4]})\n栽培主題: {data[1]}\n編號: {data[2]}\n")
            else:
                mushroom_info_text.insert(tk.END, f"菇菇名稱: {data[3]}\n栽培主題: {data[1]}\n編號: {data[2]}\n")
            mushroom_info_text.insert(tk.END, f"賣價: {data[6]} NP\n")
            mushroom_info_text.insert(tk.END, f"稀有度: {show_star(data[5])}\n")
            mushroom_info_text.tag_configure(f"圖片{data[3]}{data[4]}", foreground="blue", underline=True)
            mushroom_info_text.tag_bind(f"圖片{data[3]}{data[4]}", "<Button-1>", lambda event, name=data[3], rs=data[4]: open_second_window_on_click(name, rs))
            if data[4] == 1 or data[4] == 2:
                mushroom_info_text.insert(tk.END, f"{data[3]}(稀有{data[4]})-圖片\n", f"圖片{data[3]}{data[4]}")
            else:
                mushroom_info_text.insert(tk.END, f"{data[3]}-圖片\n", f"圖片{data[3]}{data[4]}")
            mushroom_info_text.insert(tk.END, f"----------------------\n")
    else:
        mushroom_info_text.delete('1.0', tk.END)
        mushroom_info_text.insert(tk.END, "無搜尋結果")

    # 關閉遊標和連接
    cur.close()
    conn.close()

def search_mushrooms_by_price():
    # 建立連接
    # 有帳密資訊，故移除

    # 建立遊標
    cur = conn.cursor()

    # 搜尋菇菇
    mushroom_price1 = search_price_entry1.get()  # 獲取輸入的賣價下限
    mushroom_price2 = search_price_entry2.get()  # 獲取輸入的賣價上限
    if search_price_entry1.get() != "" and search_price_entry2.get() != "":
        cur.execute("SELECT * FROM mushroom_dictionary WHERE NP >= %s and NP <= %s order by NP, theme_id, id, rare_state asc;", (str(mushroom_price1), str(mushroom_price2)))
    else:
        cur.execute("SELECT * FROM mushroom_dictionary WHERE NP = -1 order by NP, theme_id, id, rare_state asc;")
    mushroom_data = cur.fetchall()

    # 顯示菇菇列表到UI中
    if mushroom_data:
        mushroom_info_text.delete('1.0', tk.END)  # 清空Text區域
        for data in mushroom_data:
            if data[4] == 1 or data[4] == 2:
                mushroom_info_text.insert(tk.END, f"菇菇名稱: {data[3]}(稀有{data[4]})\n栽培主題: {data[1]}\n編號: {data[2]}\n")
            else:
                mushroom_info_text.insert(tk.END, f"菇菇名稱: {data[3]}\n栽培主題: {data[1]}\n編號: {data[2]}\n")
            mushroom_info_text.insert(tk.END, f"賣價: {data[6]} NP\n")
            mushroom_info_text.insert(tk.END, f"稀有度: {show_star(data[5])}\n")
            mushroom_info_text.tag_configure(f"圖片{data[3]}{data[4]}", foreground="blue", underline=True)
            mushroom_info_text.tag_bind(f"圖片{data[3]}{data[4]}", "<Button-1>", lambda event, name=data[3], rs=data[4]: open_second_window_on_click(name, rs))
            if data[4] == 1 or data[4] == 2:
                mushroom_info_text.insert(tk.END, f"{data[3]}(稀有{data[4]})-圖片\n", f"圖片{data[3]}{data[4]}")
            else:
                mushroom_info_text.insert(tk.END, f"{data[3]}-圖片\n", f"圖片{data[3]}{data[4]}")
            mushroom_info_text.insert(tk.END, f"----------------------\n")
    else:
        mushroom_info_text.delete('1.0', tk.END)
        mushroom_info_text.insert(tk.END, "無搜尋結果")

    # 關閉遊標和連接
    cur.close()
    conn.close()

# 建立主視窗
root = tk.Tk()
root.title("菇菇栽培圖鑑")

# 所有搜尋框
search_theme_button = tk.Button(root, text="所有", command=search_all_mushrooms) # 搜尋框
search_theme_button.grid(row=0, column=9, padx=5, pady=5,)

# 輸入菇菇名稱
search_name_label = tk.Label(root, text="輸入菇菇名稱:")
search_name_label.grid(row=0, column=0, padx=5, pady=5)

search_name_entry = tk.Entry(root)
search_name_entry.grid(row=0, column=1, padx=5, pady=5)

search_name_button = tk.Button(root, text="搜尋", command=search_mushrooms_by_name) # 搜尋框
search_name_button.grid(row=0, column=2, padx=5, pady=5)

# 輸入菇菇名稱和栽培主題的空格
search_blank_label = tk.Label(root, text="             ")
search_blank_label.grid(row=0, column=3, padx=5, pady=5)

# 輸入栽培主題
search_theme_label = tk.Label(root, text="輸入栽培主題:")
search_theme_label.grid(row=0, column=4, padx=5, pady=5)

search_theme_entry = tk.Entry(root)
search_theme_entry.grid(row=0, column=5, padx=5, pady=5)

search_theme_button = tk.Button(root, text="搜尋", command=search_mushrooms_by_theme) # 搜尋框
search_theme_button.grid(row=0, column=6, padx=5, pady=5)

# 選擇稀有度
search_rarity_label = tk.Label(root, text="請選擇稀有度:")
search_rarity_label.grid(row=1, column=0, padx=1, pady=5, sticky="ew")

options = ["請選擇","1星", "2星", "3星", "4星", "5星"]
selected_rarity = tk.StringVar(root)
selected_rarity.set(options[0])

search_rarity_entry = tk.OptionMenu(root, selected_rarity, *options, command=lambda x: search_mushrooms_by_rarity(menu_select(selected_rarity.get()[0])))
search_rarity_entry.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

search_blank_label = tk.Label(root, text="             ")
search_blank_label.grid(row=1, column=2, padx=5, pady=5)

search_blank_label = tk.Label(root, text="             ")
search_blank_label.grid(row=1, column=3, padx=5, pady=5)

# 輸入菇菇名稱
search_price_label = tk.Label(root, text="賣價NP範圍:")
search_price_label.grid(row=1, column=4, padx=5, pady=5)

search_price_entry1 = tk.Entry(root)
search_price_entry1.grid(row=1, column=5, padx=5, pady=5)

search_price_label = tk.Label(root, text="~")
search_price_label.grid(row=1, column=6, padx=5, pady=5)

search_price_entry2 = tk.Entry(root)
search_price_entry2.grid(row=1, column=7, padx=5, pady=5)

search_price_button = tk.Button(root, text="搜尋", command=search_mushrooms_by_price) # 搜尋框
search_price_button.grid(row=1, column=8, padx=5, pady=5)

mushroom_info_text = tk.Text(root)
mushroom_info_text.grid(row=2, column=0,  padx=5, pady=5, rowspan=30, columnspan=150)

# 運行主視窗
root.mainloop()
