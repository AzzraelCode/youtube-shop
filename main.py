from shops.shop_akusherstvo_ru import AkusherstvoRu
from shops.shop_technopark_ru import TechnoparkRu

if __name__ == '__main__':
    print("** Hola Hey, Azzrael_YT subs!!!\n")

    shop = AkusherstvoRu()
    shop.get_lot_static("https://www.akusherstvo.ru/catalog/1114362-progulochnaya-kolyaska-farfello-bino-angel-plus-2021/")
    # shop = TechnoparkRu()
    # shop.get_lot_static("https://www.technopark.ru/moyschik-okon-hobot-198/")
