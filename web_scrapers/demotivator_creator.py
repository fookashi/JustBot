import re
from io import BytesIO
import random

import aiohttp

from models.images import DemotivatorImage, ImageToDemotivator

DEMO_TEXTS = (
    'Петербургский феномен', 'все просто',
    'Кушетка Андрея Бахметьева', 'Тут даже я/ахуел',
    'Два месяца на дваче/И это нихуя, блять, не смешно',
    'Я БЛЯТЬ ХОЧУ ЕБАТЬСЯ/я блудна сучка хочу чтоб ты выебал мене',
    'ВСЕ НА ЧТО СПОСОБНО/НАШЕ ПОКОЛЕНИЕ',
    'Что дальше?/Чайник с функцией жопа?',
    'Самсунг гэлэкси джей один мини/ебал коня',
    'мужик ты чего...', 'ядрена/копоть', 'Ъ/ъ',
    'Добрый чел/позитивный', 'хуйня',
    'окей гугл/fuck your mother in her houl',
    'почему когда дрочишь/не играет песня играй рука балдей писюн?',
    'как скачать?', 'Ладно./текст', 'Мыний гесли/Демотец окрасской рутии',
    'Айр мер вор еркинес ес, сурб егеци анун ко. Екесце аркаютюн ко егеци камк'
    'ко ворпес еркинес ев еркври. Ев тох мез зпартис мер ворпес ев мек тохумк мероц'
    'партапанац./Ев ми танир змез и порцутюн. Айл пркеа ез и чаре. Зи кое аркаютюн. Амен',
    'How?/Текст', 'Я клитор/Запомнили?'
)


class DemotivatorCreator:
    def __init__(self):
        self.url = "https://ademotivatory.ru/create/rezult.php"

    async def create_demotivator(self, text: str, image: ImageToDemotivator) -> DemotivatorImage | None:
        form_data = aiohttp.FormData()
        if text == "do_random":
            text = random.choice(DEMO_TEXTS)
        try:
            text1, text2 = text.split('/')
        except ValueError:
            text1 = text
            text2 = ''
        form_data.add_field('photo', image.image, filename=image.name, content_type=image.content_type)
        form_data.add_field('text1', text1, content_type='text/plain; charset="cp1251"')
        form_data.add_field('text2', text2, content_type='text/plain; charset="cp1251"')
        form_data.add_field('size1', '40')
        form_data.add_field('size2', '30')
        form_data.add_field('bgcolor', '000000')
        form_data.add_field('fontcolor', 'FFFFFF')
        form_data.add_field('bordercolor', 'FFFFFF')
        form_data.add_field('fbcolor', '000000')
        form_data.add_field('size3', '2000')
        form_data.add_field('font', 'Univers_Medium')

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, data=form_data) as resp:
                if resp.status != 200:
                    return None
                text = await resp.text()
                try:
                    link = next(re.finditer(r'http://ademotivatory\.ru/create/dem\S*', text)).group()[:-1]
                except:
                    raise Exception('Не получилось обработать изображение:(')

            async with session.get(link) as resp:
                if resp.status != 200:
                    return None
                data = BytesIO(await resp.read())
                name = link.split('/')[-1]
                return DemotivatorImage(name=name, image=data)
