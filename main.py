from tkinter.ttk import *
from tkinter import *
import os
import sys
import random
import requests
import threading
import time

tk = Tk()  # 创建窗口获取屏幕信息后销毁
CONFIG = {
    # ===以下为系统配置获取=== #
    "INFO_SCREEN_WIDTH": tk.winfo_screenwidth(),  # 屏幕宽
    "INFO_SCREEN_HEIGHT": tk.winfo_screenheight(),  # 屏幕高
    # ===以下为颜色配置=== #
    "COLOR_TITLE": ["#767F89", "#23272E"],
    "COLOR_CONTEXT": ["#C8C8C8", "#23272E"],
    "COLOR_BACKGROUND": ["#23272E", "#DEDEDE"],
    "THEME": 0,
    # ===以下为名单配置初始化=== #
    "NAME": {},
    "LIST": [],
    "TABLE": [],
}
LANG = {}  # 语言文件（读入）
LANGKEY = [
    "LB.title",  # 程序标题
]  # 需要的语言键值对
INFO = {"VERSION": "2.3.3"}
tk.destroy()


def codeapi(File, Repositories="CodeAPI"):
    site = f"http://codezpc.github.io/{Repositories}/{File}"
    try:
        # 发送HTTP GET请求
        response = requests.get(site)
        response.raise_for_status()  # 如果请求失败则抛出异常
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching file: {e}")
        return "None"

class LanguageFileNotCompletely(Exception):
    """
    自定义错误：文件残缺
    """
    def __init__(self,ErrorInfo):
        super().__init__(self)
        self.errorinfo=ErrorInfo
    def __str__(self):
        return self.errorinfo

class Trial:
    def __init__(self):
        global LANG
        ini = Tk()  # 初始化窗口
        ini.overrideredirect(True)  # 去除窗口修饰
        ini.geometry(
            f"400x105+{int((CONFIG["INFO_SCREEN_WIDTH"] - 400) / 2)}+{int((CONFIG["INFO_SCREEN_HEIGHT"] - 105) / 2)}"
        )  # 居中
        ini.resizable(False, False)  # 禁用缩放
        ini.title("启动")
        ini.configure(bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]])
        info = Label(
            ini,
            text="\n启动……\n准备……",
            font=("汉仪文黑-85W", 15),
            fg=CONFIG["COLOR_TITLE"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
            justify=CENTER,
        )
        info.pack()
        ini.update()
        time.sleep(0.4)

        def status(text, t=0.3, failure=False):
            """
            启动时的信息显示

            :param text: 信息
            :param t: 延迟时间
            :param failure: 反馈为错误
            """
            info.configure(
                text=text,
                fg="#AE7A7A" if failure else CONFIG["COLOR_TITLE"][CONFIG["THEME"]],
            )
            ini.update()
            time.sleep(t)

        # 读取语言文件
        try:
            with open("set/lang.json", "r", encoding="UTF-8") as f:
                LANG = eval(f.read())

            # 检测文件完整性
            errors = []
            for i in LANGKEY:
                try:
                    LANG[i]  # 尝试读取一次
                except KeyError:
                    errors.append(i)
            if errors != []:
                raise LanguageFileNotCompletely("".join(f"{i}\n" for i in errors))
        except FileNotFoundError:
            status(
                f"\n获取语言文件失败\n3秒后退出",
                t=3,
                failure=True,
            )
            ini.destroy()
            exit()
        except LanguageFileNotCompletely as e: # 文件缺少必要项
            with open("ERROR.txt", "w", encoding="UTF-8") as f:
                f.write(str(e))
            status(
                f"\n语言文件缺少必要项目，详见ERROR.txt\n3秒后退出",
                t=3,
                failure=True,
            )
            ini.destroy()
            exit()
        except SyntaxError:
            status(
                f"\n语言文件格式错误，检查文件格式后重试\n3秒后退出",
                t=3,
                failure=True,
            )
            ini.destroy()
            exit()

        # 读取API数据
        try:
            with open("set/KEY", "r") as f:
                status(f"\n{LANG["LB.title"]}正在启动……\n获取API-KEY……")
                self.KEY = f.read()
        except FileNotFoundError:
            status(
                f"\n{LANG["LB.title"]}正在启动……\n获取API-KEY失败", t=1, failure=True
            )
            CONFIG["NAME"] = None
        else:
            status(f"\n{LANG["LB.title"]}正在启动……\n获取API数据……")
            CONFIG["NAME"] = eval(codeapi(f"LB/{self.KEY}/names.json", "CodeAPI"))

        # 处理本地名单
        if not CONFIG["NAME"]:
            try:
                with open("./set/names.json", "r", encoding="utf-8") as f:
                    status(
                        f"\n{LANG["LB.title"]}正在启动……\n获取API数据失败，获取本地数据……",
                        failure=True,
                    )
                    CONFIG["NAME"] = eval(f.read())
            except FileNotFoundError:
                status("\n获取数据失败\n3秒后退出", t=3, failure=True)
                ini.destroy()
                exit()

        # 解析名单文件
        status(f"\n{LANG["LB.title"]}正在启动……\n解析抽取池……")
        CONFIG["LIST"] = CONFIG["NAME"].keys()
        status(f"\n{LANG["LB.title"]}正在启动……\n应用抽取池……")
        CONFIG["TABLE"] = CONFIG["NAME"][list(CONFIG["LIST"])[0]]
        status("\n完成", t=1)
        ini.destroy()

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
        self.board.title(f"{LANG["LB.title"]}")
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
        self.setting_board.title(f"{LANG["LB.title"]} - 设置")
        self.setting_board.geometry("400x300")
        self.setting_board.resizable(False, False)
        empty = Label(
            self.setting_board,
            text="     ",
            font=("汉仪文黑-85W", 20),
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
        )
        empty.pack()
        self.key_change = Button(
            self.setting_board,
            text="Custom KEY...",
            fg=CONFIG["COLOR_TITLE"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
            font=("汉仪文黑-85W", 20),
        )
        self.key_change.pack()
        # TODO settings

    def function(self, event, arg):
        show = {
            0: "选择人数以开始",
            1: "抽取1人",
            2: "抽取2人",
            3: "抽取3人",
            4: "抽取4人",
            5: "抽取5人",
            6: "抽取6人",
            7: "抽取7人",
            8: "抽取8人",
            9: "抽取9人",
            "pool": "抽取池……？",
            "set": "设置……？",
        }
        self.start.configure(text=show[arg])

    def load_ui(self):
        tk = Tk()
        # 居中
        # tk.geometry(
        #     f"""{800}x{450}+{int((CONFIG["INFO_SCREEN_WIDTH"] - 1280) / 2)}+{int((CONFIG["INFO_SCREEN_HEIGHT"] - 720) / 2)}"""
        # )
        # 禁止缩放
        tk.resizable(False, False)
        # 标题
        tk.title(f"{LANG["LB.title"]} by CODEZPC - {INFO["VERSION"]}")
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
            text=f"{LANG["LB.title"]}",
            font=("汉仪文黑-85W", 40),
            fg=CONFIG["COLOR_TITLE"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
            justify=CENTER,
        )
        self.title.grid(row=1, column=1, columnspan=9)
        self.start = Label(
            tk,
            text="选择人数以开始",
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
        self.startbutton1.bind("<Enter>", lambda event: self.function(event, 1))
        self.startbutton2.bind("<Enter>", lambda event: self.function(event, 2))
        self.startbutton3.bind("<Enter>", lambda event: self.function(event, 3))
        self.startbutton4.bind("<Enter>", lambda event: self.function(event, 4))
        self.startbutton5.bind("<Enter>", lambda event: self.function(event, 5))
        self.startbutton6.bind("<Enter>", lambda event: self.function(event, 6))
        self.startbutton7.bind("<Enter>", lambda event: self.function(event, 7))
        self.startbutton8.bind("<Enter>", lambda event: self.function(event, 8))
        self.startbutton9.bind("<Enter>", lambda event: self.function(event, 9))
        self.startbutton1.bind("<Leave>", lambda event: self.function(event, 0))
        self.startbutton2.bind("<Leave>", lambda event: self.function(event, 0))
        self.startbutton3.bind("<Leave>", lambda event: self.function(event, 0))
        self.startbutton4.bind("<Leave>", lambda event: self.function(event, 0))
        self.startbutton5.bind("<Leave>", lambda event: self.function(event, 0))
        self.startbutton6.bind("<Leave>", lambda event: self.function(event, 0))
        self.startbutton7.bind("<Leave>", lambda event: self.function(event, 0))
        self.startbutton8.bind("<Leave>", lambda event: self.function(event, 0))
        self.startbutton9.bind("<Leave>", lambda event: self.function(event, 0))

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
        pool_select.bind("<Enter>", lambda event: self.function(event, "pool"))
        pool_select.bind("<Leave>", lambda event: self.function(event, 0))

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

        self.set = Button(
            tk,
            text="设置",
            font=("汉仪文黑-85W", 8),
            fg=CONFIG["COLOR_TITLE"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
            command=self.setting,
            width=5,
        )
        self.set.grid(row=5, column=1, columnspan=9)
        self.set.bind("<Enter>", lambda event: self.function(event, "set"))
        self.set.bind("<Leave>", lambda event: self.function(event, 0))


if __name__ == "__main__":
    Trial()
    mainloop()
