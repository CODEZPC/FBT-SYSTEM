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
    "LB.choice.none",  # 空
    "LB.choice.1",  # 抽取1-9人
    "LB.choice.2",
    "LB.choice.3",
    "LB.choice.4",
    "LB.choice.5",
    "LB.choice.6",
    "LB.choice.7",
    "LB.choice.8",
    "LB.choice.9",
    "LB.pool",  # 抽取池
    "LB.set",  # 设置
]  # 需要的语言键值对
INFO = {"VERSION": "2.3.3"}
tk.destroy()


def codeapi(File, Repositories="CodeAPI"):
    """
    获取CodeAPI

    :param File: API上的文件路径
    :param Repositories: API存储库
    """
    site = f"http://codezpc.github.io/{Repositories}/{File}"
    try:
        # 发送HTTP GET请求
        response = requests.get(site)
        response.raise_for_status()  # 如果请求失败则抛出异常
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching file: {e}")
        return "{\"$Status\": \"Fail\"}"


class LanguageFileNotCompletely(Exception):
    """
    自定义错误：文件残缺
    """

    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


class ApiDisabled(Exception):
    """
    自定义错误：Api禁用
    """

    def __init__(self, ErrorInfo):
        super().__init__(self)
        self.errorinfo = ErrorInfo

    def __str__(self):
        return self.errorinfo


class Trial:
    def __init__(self):
        global LANG
        initialize_window = Tk()  # 初始化窗口
        initialize_window.overrideredirect(True)  # 去除窗口修饰
        initialize_window.geometry(
            f"400x105+{int((CONFIG["INFO_SCREEN_WIDTH"] - 400) / 2)}+{int((CONFIG["INFO_SCREEN_HEIGHT"] - 105) / 2)}"
        )  # 居中
        initialize_window.resizable(False, False)  # 禁用缩放
        initialize_window.title("启动")
        initialize_window.configure(bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]])
        info = Label(
            initialize_window,
            text="\n启动……\n准备……",
            font=("汉仪文黑-85W", 15),
            fg=CONFIG["COLOR_TITLE"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
            justify=CENTER,
        )
        info.pack()
        initialize_window.update()
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
            initialize_window.update()
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
            initialize_window.destroy()
            exit()
        except LanguageFileNotCompletely as e:  # 文件缺少必要项
            with open("ERROR.txt", "w", encoding="UTF-8") as f:
                f.write(str(e))
            status(
                f"\n语言文件缺少必要项目，详见ERROR.txt\n3秒后退出",
                t=3,
                failure=True,
            )
            initialize_window.destroy()
            exit()
        except SyntaxError:
            status(
                f"\n语言文件格式错误，检查文件格式后重试\n3秒后退出",
                t=3,
                failure=True,
            )
            initialize_window.destroy()
            exit()

        # 读取API数据
        try:
            with open("set/KEY", "r") as f:
                status(f"\n{LANG["LB.title"]}正在启动……\n获取API-KEY……")
                self.KEY = f.read()
            if self.KEY == "NONE":
                raise ApiDisabled(True)
        except FileNotFoundError:
            status(
                f"\n{LANG["LB.title"]}正在启动……\n获取API-KEY失败", t=1, failure=True
            )
            CONFIG["NAME"] = {"$Status": "Fail"}
        except ApiDisabled:
            status(f"\n{LANG["LB.title"]}正在启动……\nAPI已禁用")
            CONFIG["NAME"] = {"$Status": "Disable"}
        else:
            status(f"\n{LANG["LB.title"]}正在启动……\n获取API数据……")
            CONFIG["NAME"] = eval(codeapi(f"LB/{self.KEY}/names.json", "CodeAPI"))

        # 处理本地名单
        if "$Status" in list(CONFIG["NAME"].keys()):
            if CONFIG["NAME"]["$Status"] == "Fail":
                status(
                    f"\n{LANG["LB.title"]}正在启动……\n获取API数据失败，获取本地数据……",
                    failure=True,
                )
            else:
                status(
                    f"\n{LANG["LB.title"]}正在启动……\n获取本地数据……",
                )
            try:
                with open("./set/names.json", "r", encoding="utf-8") as f:
                    CONFIG["NAME"] = eval(f.read())
            except FileNotFoundError:
                status("\n获取数据失败\n3秒后退出", t=3, failure=True)
                initialize_window.destroy()
                exit()

        # 解析名单文件
        status(f"\n{LANG["LB.title"]}正在启动……\n解析抽取池……")
        CONFIG["LIST"] = CONFIG["NAME"].keys()
        status(f"\n{LANG["LB.title"]}正在启动……\n应用抽取池……")
        CONFIG["TABLE"] = CONFIG["NAME"][list(CONFIG["LIST"])[0]]
        status("\n完成", t=1)
        initialize_window.destroy()

        self.load_ui()

    def choice(self, amount):
        choices = []
        if amount > len(CONFIG["TABLE"]):
            for i in range(amount):
                choices.append("Error")
            return choices
        pool = [i for i in range(1, len(CONFIG["TABLE"]) + 1)]
        for i in range(amount):
            get = random.randint(0, len(pool) - 1)
            choices.append(CONFIG["TABLE"][pool[get] - 1])
            del pool[get]
        return choices

    def draw_thread(self, amount):
        thread = threading.Thread(target=self.draw, args=(amount,))
        thread.start()

    def draw(self, amount):
        def dw():
            self.name.grid_forget()
            names = self.choice(amount)
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
        self.start.configure(text=LANG[arg])

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
        self.startbutton = []
        for i in range(1, 10):
            self.startbutton.append(
                Button(
                    tk,
                    text=f"{i}",
                    font=("汉仪文黑-85W", 20),
                    fg=CONFIG["COLOR_TITLE"][CONFIG["THEME"]],
                    bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
                    command=lambda i=i: self.draw_thread(i),
                    width=3,
                )
            )
            self.startbutton[i - 1].grid(row=3, column=i)
            self.startbutton[i - 1].bind(
                "<Enter>", lambda event, i=i: self.function(event, f"LB.choice.{i}")
            )
            self.startbutton[i - 1].bind(
                "<Leave>", lambda event: self.function(event, "LB.choice.none")
            )

        # === 下拉菜单 === #

        self.combo_style = Style()
        self.combo_style.theme_create(
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
        self.combo_style.theme_use("combostyle")

        self.pool_select = Combobox(tk, values=list(CONFIG["LIST"]), state="readonly")

        def option_selected(event):
            CONFIG["TABLE"] = CONFIG["NAME"][self.pool_select.get()]

        self.pool_select.bind("<<ComboboxSelected>>", option_selected)
        self.pool_select.grid(row=5, column=1, columnspan=9)
        self.pool_select.bind("<Enter>", lambda event: self.function(event, "LB.pool"))
        self.pool_select.bind(
            "<Leave>", lambda event: self.function(event, "LB.choice.none")
        )

        # === 工具栏 === #

        self.set = Button(
            tk,
            text="设置",
            font=("汉仪文黑-85W", 8),
            fg=CONFIG["COLOR_TITLE"][CONFIG["THEME"]],
            bg=CONFIG["COLOR_BACKGROUND"][CONFIG["THEME"]],
            command=self.setting,
            width=8,
        )
        self.set.grid(row=4, column=1, columnspan=9)
        self.set.bind("<Enter>", lambda event: self.function(event, "LB.set"))
        self.set.bind("<Leave>", lambda event: self.function(event, "LB.choice.none"))


if __name__ == "__main__":
    Trial()
    mainloop()
