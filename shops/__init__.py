from urllib.parse import urlparse

from shops.shop_akusherstvo_ru import AkusherstvoRu
from shops.shop_technopark_ru import TechnoparkRu


def instance_by_url(url):
    """
    Передаю ссылку на карточку кот собираюсь парсить
    проверяю что могу парсить такие карточки
    и возвращаю объект соотв. класса для дальнейшего парсинга
    :param url:
    :return:
    """
    # проверка что перена ссылка
    r = urlparse(url)
    if not r.scheme.startswith('http'): return None, "Это вообще не ссылка"

    host = r.hostname.replace("www.", "").lower() # чищу от www для унификации
    # определяю по хосту c каким классом работать
    classes = {
        'technopark.ru': lambda : TechnoparkRu(), # лямбда чтобы не создавать лишние объекты
        'akusherstvo.ru': lambda : AkusherstvoRu(),
    }

    if host not in classes: return None, "Не умею работать с такими ссылками"

    return classes[host](), None