import tkinter as tk # библиотека tkinter
import tkinter.messagebox # вывод сообщений
import webbrowser # для открытия ссылок в браузере по умолчанию
from tkinter import ttk # модуль с более настраиваемыми виджетами

import shops

class Window:
    """
    Полезные ссылки
    https://tcl.tk/
    https://tkdocs.com/tutorial/widgets.html
    https://realpython.com/python-gui-tkinter/
    https://python-scripts.com/tkinter

    установка pip install tk
    """
    def __init__(self):
        """
        Конструктор класса в кот. готовлю элементы окошка к отрисовки
        и связываю кнопки
        """
        self.w = tk.Tk()
        # текст в заголовке окна
        self.w.title("YouTube Shop | Парсинг интернет магазина и генерация видео | Azzrael")

        self.w.geometry("680x680+50+25") # размеры и положение окна WxH+x+y
        self.w.resizable(0, 0)

        # заполняем окно элементами
        self.els = {}
        self.layout()

        # процесс окошка
        self.w.mainloop()


    def layout(self):
        """
        Элементы управления - поля и кнопки
        """
        style = ttk.Style()
        style.configure('TEntry', padding='5 5 5 5')
        style.configure('TButton', padding='5 4 5 4')
        style.configure('TCombobox', padding='5 5 5 5')

        # поле для ввода ссылки на товар для парсинга и кнопка для старта парсинга
        tk.Label(text="Ссылка на страницу товара", justify=tk.LEFT).place(x=5, y=5)
        self.els['url'] = ttk.Entry(self.w, width=63, style="TEntry") # ширина в символах, а не в пикселях !!!
        self.els['url'].focus_set() # при открытии окна фокурсируюсь на этом поле
        self.els['url'].place(x=7, y=30)

        self.els['url'].insert(0, "https://www.technopark.ru/moyschik-okon-hobot-198/") # для тестов на dev todo: remove

        ttk.Button(self.w, text="Парсить", width=25, style="TButton", command=self.action_btn_parse).place(x=480, y=29)

        # поле для ввода заголовка
        tk.Label(text="Текст на видео и обложке", justify=tk.LEFT).place(x=5, y=75)
        self.els['video_text'] = ttk.Entry(self.w, width=63, style="TEntry")
        self.els['video_text'].place(x=7, y=100)

        # поле для ввода партнерской ссылки
        tk.Label(text="Партнерская ссылка", justify=tk.LEFT).place(x=5, y=135)
        self.els['goto'] = ttk.Entry(self.w, width=63, style="TEntry")
        self.els['goto'].place(x=7, y=160)

        # комбо для выбора шаблона генерации видео
        cb_video_tmpl_values = ['С заставкой', 'Без заставки', 'Длинный']
        tk.Label(text="Шаблон для генерации видео", justify=tk.LEFT).place(x=5, y=195)
        self.els['cb_video_tmpl'] = ttk.Combobox(self.w, width=61, style="TCombobox", values=cb_video_tmpl_values, state="readonly")
        self.els['cb_video_tmpl'].place(x=7, y=220)
        self.els['cb_video_tmpl'].current(0) # шаблон по умолчанию

        ttk.Button(self.w, text="Создать видео", width=25, style="TButton", command=self.action_btn_create_video()).place(x=480, y=218)

        # комбо для выбора шаблона генерации обложки
        cb_intro_img_values = ['Простая', 'Яркая', 'Без заставки']
        tk.Label(text="Заставка к видео", justify=tk.LEFT).place(x=5, y=255)
        self.els['cb_intro_img'] = ttk.Combobox(self.w, width=61, style="TCombobox", values=cb_intro_img_values, state="readonly")
        self.els['cb_intro_img'].place(x=7, y=280)
        self.els['cb_intro_img'].current(0)  # шаблон по умолчанию

        # поле для ввода заголовка видео
        tk.Label(text="Заголовок видео", justify=tk.LEFT).place(x=5, y=315)
        self.els['yt_title'] = ttk.Entry(self.w, width=63, style="TEntry")
        self.els['yt_title'].place(x=7, y=340)

        # поле для ввода тегов
        tk.Label(text="Теги, через зпт", justify=tk.LEFT).place(x=5, y=375)
        self.els['yt_tags'] = ttk.Entry(self.w, width=63, style="TEntry")
        self.els['yt_tags'].place(x=7, y=400)

        # поле для ввода описания
        tk.Label(text="Описание", justify=tk.LEFT).place(x=5, y=435)
        self.els['yt_desc'] = tk.Text(self.w, width=50, height=7)
        self.els['yt_desc'].place(x=7, y=460)

        ttk.Button(self.w, text="Подготовить описание", width=25, style="TButton", command=self.action_btn_create_desc()).place(x=480, y=460)

        # поле для ввода заголовка видео
        tk.Label(text="Загрузи видео на YT и добавь ссылку на загруженное (или id видео)", justify=tk.LEFT).place(x=5, y=615)
        self.els['yt_video_id'] = ttk.Entry(self.w, width=63, style="TEntry")
        self.els['yt_video_id'].place(x=7, y=640)

        ttk.Button(self.w, text="Обновить описание к видео", width=25, style="TButton", command=self.action_btn_parse).place(x=480, y=640)

    def action_btn_create_desc(self):
        pass

    def action_btn_create_video(self):
        pass


    def action_btn_parse(self):
        """
        Жму на кнопку парсинга
        :return:
        """
        try:
            url = self.els['url'].get().strip()
            if len(url) < 3: raise Exception("Ты забыл про ссылку на карточку товара")

            # в классе Shop определяю каким классом буду парсить
            o, err = shops.instance_by_url(url)
            if not o: raise Exception(err) # если такой сайт парсить не умею

            r = o.get_lot_static(url)
            if not r: raise o.first_error()
            self.els['title'].insert(0, r.get('title', '-'))

            print(o)

        except Exception as e:
            self.error(self.els['url'], str(e))

    def error(self, target, message):
        """
        Для вывода сообщения об ошибке и фокуса на поле, где допущена ошибка
        :param target:
        :param message:
        :return:
        """
        tk.messagebox.showerror("Ошибка", message=message)
        target.focus_set()