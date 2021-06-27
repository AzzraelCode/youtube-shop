import codecs
import subprocess
from config import get_path


def create_image(template=0, data={}):
    # готовлю Html
    prepare_html(template, data)

    # собираю команду конвертации
    cmd = " ".join([
        get_path("bin\wkhtmltoimage.exe"),
       " --height 1080 --width 1920",
       " --enable-local-file-access", # чтобы получить доступ к картинкам
        "-q", # чтобы не выводить лишнего
        get_path("templates\prepared.html"),
        get_path("data\image.jpg"),
    ])

    # выполняю команду конвертации html в картинку
    subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)



def prepare_html(template, data):
    """
    Передаю текст который нужно написать на картинке
    и выбираю шаблон с которым работать
    сохраняю в итоговый html, кот. потом буду конвертить в картинку
    :param template:
    :param data:
    :return:
    """
    with codecs.open(get_path(f"templates/image-{template}.html"), 'r', 'utf-8') as f:
        t = f.read()

    # для локальных файлов в шаблоне нужно передать абсолютный путь до корня проекта
    t = t.replace('{root_path}', get_path('').replace('\\','/'))
    # и поскакали реплейсить контент
    t = t.replace('{title}', data.get('title', 'Тут должен быть заголовок'))

    with codecs.open(get_path(f"templates/prepared.html"), 'w', 'utf-8') as f:
        f.write(t)
