# STAT DISABLE
# DEL NUM SHOW

from tkinter.ttk import *
from tkinter import *
import os
import sys
import random
import threading

tk = Tk()
CONFIG = {
    # ===以下为系统配置获取=== #
    "INFO_SCREEN_WIDTH": tk.winfo_screenwidth(),  # 屏幕宽
    "INFO_SCREEN_HEIGHT": tk.winfo_screenheight(),  # 屏幕高
    # ===以下为颜色配置=== #
    "COLOR_TITLE": ["#767F89", "#23272E"],
    "COLOR_CONTEXT": ["#C8C8C8", "#23272E"],
    "COLOR_BACKGROUND": ["#23272E", "#DEDEDE"],
    "THEME": 0,
    "NAME": {},
    "LIST": [],
    "TABLE": [],
}


class Trial:
    def __init__(self):
        with open("./set/names.json", "r", encoding="utf-8") as f:
            CONFIG["NAME"] = eval(f.read())
        CONFIG["LIST"] = CONFIG["NAME"].keys()
        CONFIG["TABLE"] = CONFIG["NAME"][list(CONFIG["LIST"])[0]]
        self.load_ui()

    def choice(self, pl):
        choices = []
        if pl > len(CONFIG["TABLE"]):
            for i in range(pl):
                choices.append("Error")
            return choices
        li = [i for i in range(1, len(CONFIG["TABLE"]) + 1)]
        for i in range(pl):
            t = random.randint(0, len(li) - 1)
            choices.append(CONFIG["TABLE"][li[t] - 1])
            del li[t]
        return choices

    def drawt(self, pl):
        thread = threading.Thread(target=self.draw, args=(pl,))
        thread.start()

    def draw(self, pl):
        def dw():
            self.name.grid_forget()
            names = self.choice(pl)
            name_text = ""
            for i in range(len(names)):
                if i in [3, 6]:
                    name_text += "\n"
                elif i != 0:
                    name_text += "  "
                name_text += names[i]
            self.name.configure(text=name_text)
            self.name.pack()

        self.board = Toplevel()
        self.board.configure(bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]])
        self.board.title("联邦审判")
        self.board.attributes("-topmost", True)
        self.board.attributes("-fullscreen", True)
        self.empty1 = Label(
            self.board,
            text="",
            font=("汉仪文黑-85W", 40),
            fg=CONFIG["COLOR_CONTEXT"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
        )
        self.empty1.pack()
        self.empty2 = Label(
            self.board,
            text="",
            font=("汉仪文黑-85W", 40),
            fg=CONFIG["COLOR_CONTEXT"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
        )
        self.empty2.pack(side="bottom")
        self.exit = Button(
            self.board,
            text="退出",
            font=("汉仪文黑-85W", 25),
            fg=CONFIG["COLOR_CONTEXT"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
            command=self.board.destroy,
            width=30,
        )
        self.exit.pack(side="bottom")
        self.again = Button(
            self.board,
            text="再抽一次",
            font=("汉仪文黑-85W", 25),
            fg=CONFIG["COLOR_CONTEXT"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
            command=dw,
            width=30,
        )
        self.again.pack(side="bottom")
        self.name = Label(
            self.board,
            text="",
            font=("汉仪文黑-85W", 75),
            fg=CONFIG["COLOR_CONTEXT"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
        )
        dw()

    def restart(self):
        os.execl(sys.executable, sys.executable, *sys.argv)
        exit()

    def setting(self):
        self.setting_board = Toplevel()
        self.setting_board.configure(bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]])
        self.setting_board.title("联邦审判 - 设置")
        self.setting_board.resizable(False, False)
        # TODO settings

    def load_ui(self):
        # 居中
        # tk.geometry(
        #     f"""{800}x{450}+{int((CONFIG["INFO_SCREEN_WIDTH"] - 1280) / 2)}+{int((CONFIG["INFO_SCREEN_HEIGHT"] - 720) / 2)}"""
        # )
        # 禁止缩放
        tk.resizable(False, False)
        # 标题
        tk.title("联邦审判 by CODEZPC - 2.3.0-α1")
        # 背景颜色
        tk.configure(bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]])
        self.lempty = Label(
            tk,
            text="     ",
            font=("汉仪文黑-85W", 40),
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
        )
        self.lempty.grid(row=0, column=0)
        self.rempty = Label(
            tk,
            text="     ",
            font=("汉仪文黑-85W", 40),
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
        )
        self.rempty.grid(row=1000, column=1000)
        self.title = Label(
            tk,
            text="联邦审判",
            font=("汉仪文黑-85W", 40),
            fg=CONFIG["COLOR_TITLE"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
            justify=CENTER,
        )
        self.title.grid(row=1, column=1, columnspan=9)
        self.start = Label(
            tk,
            text="选择人数并开始",
            font=("汉仪文黑-85W", 20),
            fg=CONFIG["COLOR_TITLE"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
            justify=CENTER,
        )
        self.start.grid(row=2, column=1, columnspan=9)
        self.startbutton1 = Button(
            tk,
            text="1",
            font=("汉仪文黑-85W", 20),
            fg=CONFIG["COLOR_TITLE"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
            command=lambda: self.drawt(1),
            width=3,
        )
        self.startbutton2 = Button(
            tk,
            text="2",
            font=("汉仪文黑-85W", 20),
            fg=CONFIG["COLOR_TITLE"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
            command=lambda: self.drawt(2),
            width=3,
        )
        self.startbutton3 = Button(
            tk,
            text="3",
            font=("汉仪文黑-85W", 20),
            fg=CONFIG["COLOR_TITLE"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
            command=lambda: self.drawt(3),
            width=3,
        )
        self.startbutton4 = Button(
            tk,
            text="4",
            font=("汉仪文黑-85W", 20),
            fg=CONFIG["COLOR_TITLE"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
            command=lambda: self.drawt(4),
            width=3,
        )
        self.startbutton5 = Button(
            tk,
            text="5",
            font=("汉仪文黑-85W", 20),
            fg=CONFIG["COLOR_TITLE"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
            command=lambda: self.drawt(5),
            width=3,
        )
        self.startbutton6 = Button(
            tk,
            text="6",
            font=("汉仪文黑-85W", 20),
            fg=CONFIG["COLOR_TITLE"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
            command=lambda: self.drawt(6),
            width=3,
        )
        self.startbutton7 = Button(
            tk,
            text="7",
            font=("汉仪文黑-85W", 20),
            fg=CONFIG["COLOR_TITLE"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
            command=lambda: self.drawt(7),
            width=3,
        )
        self.startbutton8 = Button(
            tk,
            text="8",
            font=("汉仪文黑-85W", 20),
            fg=CONFIG["COLOR_TITLE"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
            command=lambda: self.drawt(8),
            width=3,
        )
        self.startbutton9 = Button(
            tk,
            text="9",
            font=("汉仪文黑-85W", 20),
            fg=CONFIG["COLOR_TITLE"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
            command=lambda: self.drawt(9),
            width=3,
        )
        self.startbutton1.grid(row=3, column=1)
        self.startbutton2.grid(row=3, column=2)
        self.startbutton3.grid(row=3, column=3)
        self.startbutton4.grid(row=3, column=4)
        self.startbutton5.grid(row=3, column=5)
        self.startbutton6.grid(row=3, column=6)
        self.startbutton7.grid(row=3, column=7)
        self.startbutton8.grid(row=3, column=8)
        self.startbutton9.grid(row=3, column=9)

        combo_style = Style()
        combo_style.theme_create(
            "combostyle",
            parent="alt",
            settings={
                "TCombobox": {
                    "configure": {
                        "foreground": CONFIG["COLOR_TITLE"][CONFIG["THEME"]],
                        "selectbackground": CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
                        "fieldbackground": CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
                        "background": CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
                    }
                }
            },
        )
        combo_style.theme_use("combostyle")

        pool_select = Combobox(tk, values=list(CONFIG["LIST"]), state="readonly")
        def option_selected(event):
            CONFIG["TABLE"] = CONFIG["NAME"][pool_select.get()]

        pool_select.bind("<<ComboboxSelected>>", option_selected)
        pool_select.grid(row=4, column=1, columnspan=9)

        # self.stat = Button(
        #     tk,
        #     text="统计",
        #     font=("汉仪文黑-85W", 20),
        #     fg=CONFIG["COLOR_TITLE"][CONFIG["THEME"]],
        #     bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
        #     command=self.stat_mode,
        #     width=23,
        # )
        # self.stat.grid(row=6, column=1, columnspan=9)


if __name__ == "__main__":
    Trial()
    mainloop()
