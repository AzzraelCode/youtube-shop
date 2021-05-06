import json
import re

from shops.shop import Shop

class AkusherstvoRu(Shop):

    def __init__(self):
        Shop.__init__(self, "akusherstvo.ru")

    def get_lot_static(self, url='https://www.akusherstvo.ru/catalog/88971-avtokreslo-siger-egida-lyuks/'):
        """
        Парсим карточку товара
        !!! Парсинг поплывет как только источник изменит верстку
        :param url: ссылка на карточку
        :return:
        """
        lot = {}
        try:
            dom = self.query(url)

            # удобный тег - из аттр. content получю цену, а из id - lot_id
            el = self.xp(dom, '//span[@itemprop="price"]', throw_exc=True, attr_name=None)
            lot['lot_id']   = int(re.sub("[^0-9]", "", el.get("id"))) # из tover_price_123456 выделяю id товара
            lot['price']    = int(el.get('content'))

            lot['title']    = self.xp(dom, '//title', throw_exc=True)
            lot['img']      = "https:" + self.xp(dom, "//div[@id='itemCard']//div[contains(@class,'itemImg')]//img[1]", throw_exc=True, attr_name='src')
            self.download_image(lot['img'], f"{self.shop_name}-{lot['lot_id']}")

            t = self.xp(dom, '//div[@itemprop="description"]', throw_exc=False, ret_none="")
            lot['description'] = re.sub("(\t|\n|\r)", "", t)[:160]

            print("lot = ", json.dumps(lot, ensure_ascii=False))

            return lot

        except Exception as e:
            print("err:", e)
            return self.add_error(e, True)


