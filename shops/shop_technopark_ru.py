import json
import re

from shops.shop import Shop

class TechnoparkRu(Shop):

    def __init__(self):
        Shop.__init__(self, "technopark.ru")

    def get_lot_static(self, url='https://www.technopark.ru/televizor-samsung-ue55tu7540u/'):
        """
        Парсим карточку товара
        !!! Парсинг поплывет как только источник изменит верстку
        :param url: ссылка на карточку
        :return:
        """
        lot = {}
        try:
            dom = self.query(url)

            # удобный тег
            el = self.xp(dom, "//section[@itemtype='http://schema.org/Product']", throw_exc=True, attr_name=None)

            lot = {
                'title': el.get("data-product-name"),
                'price': int(el.get("data-product-price")),
                'lot_id': int(el.get("data-product-id")),
                'img': self.xp(dom, "//div[@class='swiper-container']//img[1]", throw_exc=True, attr_name='src'),
                'description': '',
            }

            self.download_image(lot['img'], f"{self.shop_name}-{lot['lot_id']}")

            print("lot = ", json.dumps(lot, ensure_ascii=False))
            return lot

        except Exception as e:
            print("err:", e)
            return self.add_error(e, True)


