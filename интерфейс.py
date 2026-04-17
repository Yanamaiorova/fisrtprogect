import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import webbrowser
from datetime import datetime
import random

DATA_FILE = 'pylearn_data.json'

# Предопределённые популярные курсы
POPULAR_COURSES = [
    {
        "title": "Основы Python",
        "desc": "Изучите синтаксис, типы данных\nи основы алгоритмов на самом\nпопулярном языке программирования.",
        "color": "#4A9FFF"
    },
    {
        "title": "Python для школьников",
        "desc": "Курс для школьников: основы\nPython в увлекательной форме,\nмного практических задач,\nадаптирован под возраст.",
        "color": "#4A9FFF"
    },
    {
        "title": "Как упростить жизнь с помощью\nнейросетей",
        "desc": "Бесплатный курс: что такое\nнейросети, их применение в быту\nи работе, создание текстов и\nкартинок с помощью ИИ.",
        "color": "#4A9FFF"
    }
]

# Курсы по умолчанию
DEFAULT_ENROLLED = [
    {"title": "Продвинутый Python", "progress": 60, "url": "https://realpython.com/python-advanced/"},
    {"title": "Веб-разработка на Django", "progress": 30, "url": "https://docs.djangoproject.com/"}
]

COURSE_URLS = [
    "https://realpython.com/",
    "https://www.w3schools.com/python/",
    "https://www.learnpython.org/",
    "https://stepik.org/catalog?query=python",
    "https://www.codecademy.com/learn/learn-python-3"
]


class PyLearnApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("PyLearn - Курсы Python")
        self.root.geometry("1280x720")
        self.root.configure(bg="#f4f4f4")
        self.root.resizable(False, False)

        self.load_data()

        self.create_top_bar()

        self.main_content = tk.Frame(self.root, bg="#f4f4f4")
        self.main_content.pack(fill="both", expand=True)

        if not self.data.get('registered', False):
            self.show_registration()
        else:
            self.show_courses_page()

        self.root.mainloop()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
            except:
                self.data = self.get_default_data()
        else:
            self.data = self.get_default_data()

    def get_default_data(self):
        return {
            'registered': False,
            'username': 'Пользователь',
            'email': '',
            'city': 'г. Москва',
            'reg_date': datetime.now().strftime('%d.%m.%Y'),
            'description': 'Учусь разработке на Python. Интересуюсь анализом данных и веб-разработкой на Django.\nВ свободное время пишу пет-проекты и помогаю новичкам в сообществе.',
            'stats': {'active': 4, 'hours': 10.5, 'certs': 2},
            'enrolled': DEFAULT_ENROLLED.copy(),
            'skills': ['Python', 'Django', 'SQL', 'Git', 'Docker', 'NumPy']
        }

    def save_data(self):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def create_top_bar(self):
        top_frame = tk.Frame(self.root, bg="white", height=60)
        top_frame.pack(fill="x")
        top_frame.pack_propagate(False)

        # Логотип
        tk.Label(top_frame, text="PyLearn", font=("Segoe UI", 18, "bold"),
                 fg="#4A9FFF", bg="white").pack(side="left", padx=20)

        # Вкладки
        self.tab_courses = tk.Button(top_frame, text="Курсы", font=("Segoe UI", 11, "bold"),
                                     fg="#333", bg="white", bd=0, command=self.show_courses_page)
        self.tab_courses.pack(side="left", padx=10)

        self.tab_my_courses = tk.Button(top_frame, text="Мои курсы", font=("Segoe UI", 11, "bold"),
                                        fg="#333", bg="white", bd=0, command=self.show_my_courses_page)
        self.tab_my_courses.pack(side="left", padx=10)

        self.tab_help = tk.Button(top_frame, text="Помощь", font=("Segoe UI", 11, "bold"),
                                  fg="#333", bg="white", bd=0, command=self.show_help_page)
        self.tab_help.pack(side="left", padx=10)

        # Правая часть
        right_frame = tk.Frame(top_frame, bg="white")
        right_frame.pack(side="right", padx=25)

        # Поиск
        tk.Label(right_frame, text="🔍", font=("Segoe UI", 17), bg="white").pack(side="left")
        self.search_entry = tk.Entry(right_frame, width=22, relief="flat", bg="#f0f0f0",
                                     font=("Segoe UI", 10))
        self.search_entry.pack(side="left", padx=8)

        # Уведомления
        tk.Label(right_frame, text="🛎", font=("Segoe UI", 18), bg="white").pack(side="left", padx=(15, 20))

        user_frame = tk.Frame(right_frame, bg="white")
        user_frame.pack(side="left")

        # Аватар
        self.avatar_frame = tk.Frame(user_frame, bg="#2C3E50", width=40, height=40, cursor="hand2")
        self.avatar_frame.pack(side="left", padx=(0, 8))
        self.avatar_frame.pack_propagate(False)

        self.avatar_label = tk.Label(self.avatar_frame, text="👤", font=("Segoe UI", 22),
                                     fg="white", bg="#2C3E50")
        self.avatar_label.pack(expand=True)

        # Имя пользователя
        self.username_label = tk.Label(user_frame,
                                       text=self.data.get('username', 'Пользователь'),
                                       font=("Segoe UI", 11, "bold"),
                                       bg="white",
                                       fg="#2C3E50",
                                       cursor="hand2")
        self.username_label.pack(side="left", pady=8)

        # Привязываем клики к открытию профиля
        for widget in (self.avatar_frame, self.avatar_label, self.username_label):
            widget.bind("<Button-1>", lambda e: self.show_profile())

            # Подсветка при наведении
            widget.bind("<Enter>", lambda e: e.widget.config(
                bg="#34495E" if hasattr(e.widget, 'cget') and e.widget.cget("bg") in ["#2C3E50", "#34495E"] else "#f0f0f0"))
            widget.bind("<Leave>", lambda e: e.widget.config(
                bg="#2C3E50" if hasattr(e.widget, 'cget') and e.widget.cget("bg") in ["#2C3E50", "#34495E"] else "white"))

    def show_registration(self):
        self.clear_content()

        reg_frame = tk.Frame(self.main_content, bg="#f4f4f4")
        reg_frame.pack(expand=True)

        tk.Label(reg_frame, text="Регистрация в PyLearn", font=("Segoe UI", 20, "bold"), bg="#f4f4f4").pack(pady=20)

        tk.Label(reg_frame, text="Логин", font=("Segoe UI", 11), bg="#f4f4f4").pack(anchor="w", padx=80)
        self.login_entry = tk.Entry(reg_frame, width=40, font=("Segoe UI", 11))
        self.login_entry.pack(pady=5, padx=80)

        tk.Label(reg_frame, text="Эл. почта", font=("Segoe UI", 11), bg="#f4f4f4").pack(anchor="w", padx=80)
        self.email_entry = tk.Entry(reg_frame, width=40, font=("Segoe UI", 11))
        self.email_entry.pack(pady=5, padx=80)

        self.reg_status = tk.Label(reg_frame, text="", font=("Segoe UI", 11), fg="red", bg="#f4f4f4")
        self.reg_status.pack(pady=10)

        btn_frame = tk.Frame(reg_frame, bg="#f4f4f4")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="Зарегистрироваться", bg="#4A9FFF", fg="white", font=("Segoe UI", 11, "bold"),
                  width=20, height=2, relief="flat", command=self.register_user).pack(side="left", padx=10)
        tk.Button(btn_frame, text="Войти", bg="#666", fg="white", font=("Segoe UI", 11, "bold"),
                  width=15, height=2, relief="flat", command=self.try_login).pack(side="left", padx=10)

    def register_user(self):
        login = self.login_entry.get().strip()
        email = self.email_entry.get().strip()
        if not login or not email:
            self.reg_status.config(text="Заполните все поля!", fg="red")
            return

        self.data['registered'] = True
        self.data['username'] = login
        self.data['email'] = email
        self.data['reg_date'] = datetime.now().strftime('%d.%m.%Y')
        self.save_data()

        # Обновляем имя в верхней панели
        if hasattr(self, 'username_label'):
            self.username_label.config(text=login)

        messagebox.showinfo("Успех", "Регистрация прошла успешно!")
        self.show_courses_page()

    def try_login(self):
        if not self.data.get('registered', False):
            self.reg_status.config(text="Сначала зарегистрируйтесь!", fg="red")
        else:
            self.show_courses_page()

    def clear_content(self):
        for widget in self.main_content.winfo_children():
            widget.destroy()

    def show_courses_page(self):
        self.clear_content()
        self.tab_courses.config(fg="#4A9FFF", font=("Segoe UI", 11, "bold"))
        self.tab_my_courses.config(fg="#333", font=("Segoe UI", 11, "bold"))
        self.tab_help.config(fg="#333", font=("Segoe UI", 11, "bold"))

        # Баннер
        banner = tk.Frame(self.main_content, bg="#4A9FFF", height=120)
        banner.pack(fill="x")
        banner.pack_propagate(False)

        tk.Label(banner, text=f"Добро пожаловать, {self.data['username']}!",
                 font=("Segoe UI", 18, "bold"), fg="white", bg="#4A9FFF").pack(pady=(30, 5), anchor="w", padx=40)
        tk.Label(banner, text="Продолжайте свое обучение вместе с нами",
                 font=("Segoe UI", 12), fg="white", bg="#4A9FFF").pack(anchor="w", padx=40)

        # Статистика
        stats_frame = tk.Frame(self.main_content, bg="#f4f4f4")
        stats_frame.pack(fill="x", padx=40, pady=20)

        self.create_stat_card(stats_frame, "📖", "Активных курсов", str(self.data['stats']['active']))
        self.create_stat_card(stats_frame, "⏰", "Часов изучено", str(self.data['stats']['hours']))
        self.create_stat_card(stats_frame, "🏅", "Сертификатов", str(self.data['stats']['certs']))

        # Популярные курсы
        tk.Label(self.main_content, text="Популярные курсы", font=("Segoe UI", 14, "bold"), bg="#f4f4f4").pack(anchor="w", padx=40, pady=(20, 10))

        courses_container = tk.Frame(self.main_content, bg="#f4f4f4")
        courses_container.pack(fill="x", padx=40)

        for course in POPULAR_COURSES:
            card = tk.Frame(courses_container, bg="white", bd=2, relief="groove", width=320, height=220)
            card.pack(side="left", padx=15, pady=10)
            card.pack_propagate(False)

            tk.Label(card, text=course["title"], font=("Segoe UI", 13, "bold"), bg="white", wraplength=280).pack(anchor="w", padx=15, pady=(15, 5))
            tk.Label(card, text=course["desc"], font=("Segoe UI", 10), bg="white", fg="#555", justify="left", wraplength=280).pack(anchor="w", padx=15)

            btn = tk.Button(card, text="Начать", bg="#4A9FFF", fg="white", font=("Segoe UI", 10, "bold"),
                            relief="flat", command=lambda c=course: self.start_course(c))
            btn.pack(side="bottom", pady=15)

    def create_stat_card(self, parent, icon, title, value):
        frame = tk.Frame(parent, bg="white", bd=2, relief="groove", width=240, height=90)
        frame.pack(side="left", padx=15)
        frame.pack_propagate(False)

        tk.Label(frame, text=icon, font=("Segoe UI", 28), bg="white").pack(side="left", padx=20)

        inner = tk.Frame(frame, bg="white")
        inner.pack(side="left")

        tk.Label(inner, text=title, font=("Segoe UI", 10), bg="white", fg="#666").pack(anchor="w")
        tk.Label(inner, text=value, font=("Segoe UI", 18, "bold"), bg="white").pack(anchor="w")

    def start_course(self, course):
        if not any(c['title'] == course["title"] for c in self.data['enrolled']):
            self.data['enrolled'].append({
                "title": course["title"],
                "progress": 0,
                "url": random.choice(COURSE_URLS)
            })
            self.data['stats']['active'] += 1
            self.save_data()
            messagebox.showinfo("Готово", f"Курс «{course['title']}» добавлен в «Мои курсы»!")
        else:
            messagebox.showinfo("Уже есть", "Курс уже в ваших курсах.")

    def show_my_courses_page(self):
        self.clear_content()
        self.tab_courses.config(fg="#333", font=("Segoe UI", 11, "bold"))
        self.tab_my_courses.config(fg="#4A9FFF", font=("Segoe UI", 11, "bold"))
        self.tab_help.config(fg="#333", font=("Segoe UI", 11, "bold"))

        tk.Label(self.main_content, text="Активные курсы", font=("Segoe UI", 16, "bold"), bg="#f4f4f4").pack(anchor="w", padx=40, pady=20)

        container = tk.Frame(self.main_content, bg="#f4f4f4")
        container.pack(fill="both", expand=True, padx=40)

        if not self.data['enrolled']:
            tk.Label(container, text="У вас пока нет активных курсов.\nНажмите «Начать» в разделе «Курсы»",
                     font=("Segoe UI", 12), fg="#888", bg="#f4f4f4", justify="center").pack(pady=50)
            return

        for course in self.data['enrolled'][:]:
            card = tk.Frame(container, bg="white", bd=2, relief="groove")
            card.pack(fill="x", pady=8)

            tk.Label(card, text=course["title"], font=("Segoe UI", 13, "bold"), bg="white").pack(anchor="w", padx=20, pady=10)

            progress_frame = tk.Frame(card, bg="white")
            progress_frame.pack(fill="x", padx=20, pady=5)
            prog = ttk.Progressbar(progress_frame, length=400, mode='determinate', value=course["progress"])
            prog.pack(side="left")
            tk.Label(progress_frame, text=f"{course['progress']}%", bg="white").pack(side="left", padx=10)

            btn_frame = tk.Frame(card, bg="white")
            btn_frame.pack(anchor="e", padx=20, pady=10)

            tk.Button(btn_frame, text="Продолжить", bg="#4A9FFF", fg="white", font=("Segoe UI", 10, "bold"),
                      command=lambda c=course: self.continue_course(c)).pack(side="left", padx=5)
            tk.Button(btn_frame, text="Закончить курс", bg="#FF4D4D", fg="white", font=("Segoe UI", 10, "bold"),
                      command=lambda c=course: self.finish_course(c)).pack(side="left", padx=5)

    def continue_course(self, course):
        webbrowser.open(course.get("url", random.choice(COURSE_URLS)))

    def finish_course(self, course):
        if messagebox.askyesno("Закончить курс?", f"Завершить курс «{course['title']}» и убрать из списка?"):
            self.data['enrolled'].remove(course)
            self.data['stats']['active'] = max(0, self.data['stats']['active'] - 1)
            self.save_data()
            self.show_my_courses_page()

    def show_help_page(self):
        self.clear_content()
        self.tab_courses.config(fg="#333", font=("Segoe UI", 11, "bold"))
        self.tab_my_courses.config(fg="#333", font=("Segoe UI", 11, "bold"))
        self.tab_help.config(fg="#4A9FFF", font=("Segoe UI", 11, "bold"))

        tk.Label(self.main_content, text="Сообщество PyLearn", font=("Segoe UI", 18, "bold"), bg="#f4f4f4").pack(pady=20)
        tk.Label(self.main_content, text="Задавай вопросы, делись опытом и учись быстрее вместе\nс тысячами студентов по всему миру.",
                 font=("Segoe UI", 11), bg="#f4f4f4", justify="center").pack()

        tk.Button(self.main_content, text="Задать вопрос", bg="#FFCC00", fg="black", font=("Segoe UI", 11, "bold"),
                  command=lambda: messagebox.showinfo("Форум", "Вопрос отправлен! (имитация)")).pack(pady=10)

        posts = [
            ("Ошибка SyntaxError при использовании f-строк в Python 3.8", "2 часа назад"),
            ("Как правильно организовать структуру проекта на Django?", "5 часов назад")
        ]
        for title, time in posts:
            post_frame = tk.Frame(self.main_content, bg="white", bd=1, relief="solid")
            post_frame.pack(fill="x", padx=60, pady=8)
            tk.Label(post_frame, text=title, font=("Segoe UI", 11, "bold"), bg="white", anchor="w").pack(anchor="w", padx=15, pady=5)
            tk.Label(post_frame, text=time, font=("Segoe UI", 9), fg="#888", bg="white").pack(anchor="w", padx=15)

    def show_profile(self):
        prof = tk.Toplevel(self.root)
        prof.title("Профиль")
        prof.geometry("700x620")
        prof.configure(bg="#f4f4f4")
        prof.grab_set()

        # Аватар
        avatar = tk.Frame(prof, bg="#222222", width=120, height=120)
        avatar.pack(pady=20)
        avatar.pack_propagate(False)
        tk.Label(avatar, text="👤", font=("Segoe UI", 60), fg="white", bg="#222222").pack(expand=True)

        tk.Label(prof, text=self.data['username'], font=("Segoe UI", 18, "bold"), bg="#f4f4f4").pack()
        tk.Label(prof, text=self.data['description'], font=("Segoe UI", 10), bg="#f4f4f4",
                 justify="center", wraplength=500).pack(pady=5)

        # Информация
        info = tk.Frame(prof, bg="#f4f4f4")
        info.pack(pady=10)
        tk.Label(info, text="📍 " + self.data['city'], font=("Segoe UI", 11), bg="#f4f4f4").pack(side="left", padx=20)
        tk.Label(info, text="📅 Дата регистрации: " + self.data['reg_date'],
                 font=("Segoe UI", 11), bg="#f4f4f4").pack(side="left")

        tk.Button(prof, text="Редактировать профиль", bg="#4A9FFF", fg="white", font=("Segoe UI", 10, "bold"),
                  command=lambda: self.edit_profile(prof)).pack(pady=15)

        # Статистика
        stat_frame = tk.Frame(prof, bg="white", bd=2, relief="groove")
        stat_frame.pack(pady=20, padx=40, fill="x")
        stats_data = [("4", "Курса"), ("10.5", "Часов"), ("2", "Сертификатов"), ("906", "Очков опыта")]
        for val, label in stats_data:
            col = tk.Frame(stat_frame, bg="white")
            col.pack(side="left", expand=True, fill="x", padx=10)
            tk.Label(col, text=val, font=("Segoe UI", 22, "bold"), bg="white").pack()
            tk.Label(col, text=label, font=("Segoe UI", 10), fg="#666", bg="white").pack()

        # Навыки
        tk.Label(prof, text="Навыки", font=("Segoe UI", 12, "bold"), bg="#f4f4f4").pack(anchor="w", padx=40, pady=(10,5))
        skills_frame = tk.Frame(prof, bg="#f4f4f4")
        skills_frame.pack(anchor="w", padx=40)
        for skill in self.data['skills']:
            tk.Label(skills_frame, text=skill, bg="#E0E0E0", padx=12, pady=4, relief="flat").pack(side="left", padx=3, pady=5)

        tk.Button(prof, text="Выйти из аккаунта", bg="#FF4D4D", fg="white", font=("Segoe UI", 11, "bold"), height=2,
                  command=lambda: self.logout(prof)).pack(side="bottom", pady=30)

    def edit_profile(self, parent):
        parent.destroy()
        edit_win = tk.Toplevel(self.root)
        edit_win.title("Редактировать профиль")
        edit_win.geometry("500x400")
        edit_win.configure(bg="#f4f4f4")

        tk.Label(edit_win, text="Город", bg="#f4f4f4").pack(anchor="w", padx=30, pady=(20,5))
        city_entry = tk.Entry(edit_win, width=50)
        city_entry.insert(0, self.data['city'])
        city_entry.pack(padx=30)

        tk.Label(edit_win, text="Описание", bg="#f4f4f4").pack(anchor="w", padx=30, pady=(15,5))
        desc_text = tk.Text(edit_win, height=8, width=50)
        desc_text.insert("1.0", self.data['description'])
        desc_text.pack(padx=30)

        def save_edit():
            self.data['city'] = city_entry.get()
            self.data['description'] = desc_text.get("1.0", "end").strip()
            self.save_data()
            edit_win.destroy()
            self.show_profile()

        tk.Button(edit_win, text="Сохранить изменения", bg="#4A9FFF", fg="white", command=save_edit).pack(pady=20)

    def logout(self, win):
        win.destroy()
        if messagebox.askyesno("Выход", "Сбросить все данные и выйти?"):
            if os.path.exists(DATA_FILE):
                os.remove(DATA_FILE)
            self.root.quit()

if __name__ == "__main__":
    PyLearnApp()