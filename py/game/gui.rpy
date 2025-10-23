################################################################################
## Инициализация
################################################################################

## Оператор init offset повышает приоритет инициализации в этом файле над
## другими файлами, из-за чего инициализация здесь запускается первее.
init offset = -2

## Вызываю gui.init, чтобы сбросить стили, чувствительные к стандартным
## значениям, и задать высоту и ширину окна игры.
init python:
    gui.init(1080, 1920)

init python:
    import requests
    import json
    import os

    #url сервера
    URL = "https://localhost:8000/"

    KEY = {"id": None, "token": None}

    screen = Screen("Main_screen")

    class Main():
        def __init__(self, last):
            del last
            if is_key():
                key_db = get_key()
                if key_db[0] == True:
                    json_db = {
                        "command" : "token",
                        "id"      : key_db[1]["id"],
                        "token"   : key_db[1]["token"]
                    }
                    db = Post(json_db)
                    if db["result"] == "True":
                        KEY = key_db[1]
                        if db["why"] == "user":
                            User_Main(self)
                        elif db["why"] == "admin":
                            Admin_Main(self)
                        else:
                            Compani_Main(self)
                del_key()

            self.button_to_guest  = None
            self.button_to_regist = None
            self.button_to_login  = None

            self.gui()

        def gui(self):
            pass
        def gui_del(self):
            pass

        def to_guest(self):
            pass

        def to_regist(self):
            self.gui_del()
            User_Regist(self)

        def to_login(self):
            self.gui_del()
            User_Login(self)


    class User_Main():
        def __init__(self, last):
            del last

    class Compani_Main():
        def __init__(self, last):
            del last

    class Admin_Main():
        def __init__(self, last):
            del last

    class User_Login():
        def __init__(self, last):
            del last

            self.why = "user"

            self.user_login  = None
            self.user_passwd = None

            self.compani_INN    = None
            self.compani_passwd = None

            self.entry_user_login  = None
            self.entry_user_passwd = None

            self.entry_compani_INN    = None
            self.entry_compani_passwd = None

            self.label_user_login  = None
            self.label_user_passwd = None

            self.label_compani_INN    = None
            self.label_compani_passwd = None

            self.button_login  = None
            self.label_massage = None
            self.button_back   = None
            self.button_why    = None

            self.gui_user()

        #Вернуться на вступительное окно
        def back(self):
            self.gui_del()
            Main(self)

        #Выполнить попытку входа
        def login(self):
            pass

        #Выставить под кем регестрироваться
        def why(self):
            if self.why == "user":
                self.why = "compani"
                self.gui_del()
                self.gui_compani()
            else:
                self.why = "user"
                self.gui_del()
                self.gui_user()

        #гуи регистрации пользователя или компании и фнк удаления гуи
        def gui_user(self):
            pass
        def gui_compani(self):
            pass
        def gui_del(self):
            pass

        #вывод сообщения об ошибке
        def message(self, tip, msg):
            if tip == False:
                pass

        #получено подтверждение
        def result_true(self, db):
            KEY = {
                "id"   : db["id"],
                "token": db["token"]
            }
            save_key(KEY)

            self.gui_del()
            if self.why == "user":
                User_Main(self)
            elif self.why == "admin":
                Admin_Main(self)
            else:
                Compani_Main(self)

        #Вход
        def login_post(self):
            if self.why == "user":
                json_db = {
                    "command" : "login",
                    "why"     : "user",
                    "login"   : self.user_login,
                    "passwd"  : self.user_passwd
                }
            elif self.why == "compani":
                json_db = {
                    "command" : "login",
                    "why"     : "compani",
                    "INN"     : self.compani_INN,
                    "passwd"  : self.compani_passwd
                }
            db = Post(json_db)
            if db["result"] == "True":
                if "id" in db and "token" in db:
                    self.result_true(db)
                else:
                    self.message(False, {
                        "result": "ERROR",
                        "type"  : "No ID or Token"
                    })
            else:
                self.message(False, db)

    #Класс регистрации (гуи + логика)
    class User_Regist():
        #Создание переменных для значений и графических объектов
        def __init__(self, last):
            del last

            self.why = "user"

            self.user_login  = None
            self.user_email  = None
            self.user_passwd = None

            self.compani_fio    = None
            self.compani_name   = None
            self.compani_INN    = None
            self.compani_email  = None
            self.compani_telef  = None
            self.compani_passwd = None

            self.entry_user_login  = None
            self.entry_user_email  = None
            self.entry_user_passwd = None

            self.entry_compani_fio    = None
            self.entry_compani_name   = None
            self.entry_compani_INN    = None
            self.entry_compani_email  = None
            self.entry_compani_telef  = None
            self.entry_compani_passwd = None

            self.label_user_login  = None
            self.label_user_email  = None
            self.label_user_passwd = None

            self.label_compani_fio    = None
            self.label_compani_name   = None
            self.label_compani_INN    = None
            self.label_compani_email  = None
            self.label_compani_telef  = None
            self.label_compani_passwd = None

            self.button_regist = None
            self.label_massage = None
            self.button_back   = None
            self.button_why    = None

            self.gui_user()

        #Вернуться на вступительное окно
        def back(self):
            self.gui_del()
            Main(self)

        #Выполнить попытку регистрации
        def regist(self):
            pass

        #Выставить под кем регестрироваться
        def why(self):
            if self.why == "user":
                self.why = "compani"
                self.gui_del()
                self.gui_compani()
            else:
                self.why = "user"
                self.gui_del()
                self.gui_user()

        #гуи регистрации пользователя или компании и фнк удаления гуи
        def gui_user(self):
            pass
        def gui_compani(self):
            pass
        def gui_del(self):
            pass

        #вывод сообщения об ошибке
        def message(self, tip, msg):
            if tip == False:
                pass

        #получено подтверждение
        def result_true(self, db):
            KEY = {
                "id"   : db["id"],
                "token": db["token"]
            }
            save_key(KEY)

            self.gui_del()
            if self.why == "user":
                User_Main(self)
            else:
                Compani_Main(self)

        #Регистрация
        def regist_post(self):
            if self.why == "user":
                json_db = {
                    "command" : "register",
                    "why"     : "user",
                    "login"   : self.user_login,
                    "email"   : self.user_email,
                    "passwd"  : self.user_passwd
                }
            elif self.why == "compani":
                json_db = {
                    "command" : "register",
                    "why"     : "compani",
                    "fio"     : self.compani_fio,
                    "name"    : self.compani_name,
                    "INN"     : self.compani_INN,
                    "email"   : self.compani_email,
                    "telef"   : self.compani_telef,
                    "passwd"  : self.compani_passwd
                }
            db = Post(json_db)
            if db["result"] == "True":
                if "id" in db and "token" in db:
                    self.result_true(db)
                else:
                    self.message(False, {
                        "result": "ERROR",
                        "type"  : "No ID or Token"
                    })
            else:
                self.message(False, db)

    #проверка на существование ключа
    def is_key():
        if "key.json" in os.listdir(config.savedir):
            return True
        return False

    #получение ключа
    def get_key():
        try:
            with open(os.path.join(config.savedir, "key.json"), "r", encoding="utf-8") as t:
                key_db = json.load(f)
            if "id" in key_db and "token" in key_db:
                return True, key_db
            else:
                return False
        except:
            return False

    #сохранение ключа
    def save_key(key_db):
        try:
            with open(os.path.join(config.savedir, "key.json", "w", encoding="utf-8") as t:
                json.dump(key_db, t, ensure_ascii=False, indent=2)
            return True
        except:
            return False

    def del_key():
        os.remove(os.path.join(config.savedir, "key.json"))

    #Отправка запроса в формате словаря и получение ответа в формате словаря
    def Post(json_db):
        global URL
        try:
            headers = {'Content-Type': 'application/json'}
            response = requests.post(URL, json=json_db, headers=headers, timeout=10)
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                return {"result":"ERROR", "type": f"HTTP {response.status_code}"}
        except Exception as e:
            return {"result":"ERROR", "type": str(e)}


## Включить проверку на недопустимые или нестабильные свойства в экранах или
## преобразованиях
define config.check_conflicting_properties = True


################################################################################
## Конфигурируемые Переменные GUI
################################################################################


## Цвета #######################################################################
##
## Цвета текста в интерфейсе.

## Акцентный цвет используется в заголовках и подчёркнутых текстах.
define gui.accent_color = '#99ccff'

## Цвет, используемый в текстовой кнопке, когда она не выбрана и не наведена.
define gui.idle_color = '#888888'

## Small_color используется в маленьком тексте, который должен быть ярче/
## темнее, для того, чтобы выделяться.
define gui.idle_small_color = '#aaaaaa'

## Цвет, используемых в кнопках и панелях, когда они наведены.
define gui.hover_color = '#c1e0ff'

## Цвет, используемый текстовой кнопкой, когда она выбрана, но не наведена.
## Кнопка может быть выбрана, если это текущий экран или текущее значение
## настройки.
define gui.selected_color = '#ffffff'

## Цвет, используемый текстовой кнопкой, когда она не может быть выбрана.
define gui.insensitive_color = '#8888887f'

## Цвета, используемые для частей панелей, которые не заполняются. Они
## используются не напрямую, а только при воссоздании файлов изображений.
define gui.muted_color = '#3d5166'
define gui.hover_muted_color = '#5b7a99'

## Цвета, используемые в тексте диалогов и выборов.
define gui.text_color = '#ffffff'
define gui.interface_text_color = '#ffffff'


## Шрифты и их размеры #########################################################

## Шрифт, используемый внутриигровым текстом.
define gui.text_font = "DejaVuSans.ttf"

## Шрифт, используемый именами персонажей.
define gui.name_text_font = "DejaVuSans.ttf"

## Шрифт, используемый текстом вне игры.
define gui.interface_text_font = "DejaVuSans.ttf"

## Размер нормального текста диалога.
define gui.text_size = 33

## Размер имён персонажей.
define gui.name_text_size = 45

## Размер текста в пользовательском интерфейсе.
define gui.interface_text_size = 33

## Размер заголовков в пользовательском интерфейсе.
define gui.label_text_size = 36

## Размер текста на экране уведомлений.
define gui.notify_text_size = 24

## Размер заголовка игры.
define gui.title_text_size = 75


## Локализация #################################################################

## Эта настройка контролирует доступ к разрыву линий. Стандартная настройка
## подходит для большинства языков. Список доступных значений можно найти на
## https://www.renpy.org/doc/html/style_properties.html#style-property-language

define gui.language = "unicode"


################################################################################
## Мобильные устройства
################################################################################

init python:

    ## Этот параметр увеличивает размер быстрых кнопок, чтобы сделать их
    ## доступнее для нажатия на планшетах и телефонах.
    @gui.variant
    def touch():

        gui.quick_button_borders = Borders(60, 21, 60, 0)

    ## Это изменяет размеры и интервалы различных элементов GUI, чтобы
    ## убедиться, что они будут лучше видны на телефонах.
    @gui.variant
    def small():

        ## Размеры шрифтов.
        gui.text_size = 45
        gui.name_text_size = 54
        gui.notify_text_size = 38
        gui.interface_text_size = 45
        gui.button_text_size = 45
        gui.label_text_size = 51

        ## Регулирует местоположение текстового окна.
        gui.textbox_height = 360
        gui.name_xpos = 120
        gui.dialogue_xpos = 135
        gui.dialogue_width = 1650

        ## Изменяет размеры и интервалы различных объектов.
        gui.slider_size = 54

        gui.choice_button_width = 1860
        gui.choice_button_text_size = 45

        gui.navigation_spacing = 30
        gui.pref_button_spacing = 15

        gui.history_height = 285
        gui.history_text_width = 1035

        gui.quick_button_text_size = 30

        ## Местоположение кнопок слотов.
        gui.file_slot_cols = 2
        gui.file_slot_rows = 2

        ## Режим NVL.
        gui.nvl_height = 255

        gui.nvl_name_width = 458
        gui.nvl_name_xpos = 488

        gui.nvl_text_width = 1373
        gui.nvl_text_xpos = 518
        gui.nvl_text_ypos = 8

        gui.nvl_thought_width = 1860
        gui.nvl_thought_xpos = 30

        gui.nvl_button_width = 1860
        gui.nvl_button_xpos = 30
