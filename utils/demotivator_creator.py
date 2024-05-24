import re
from io import BytesIO
from random import choice
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
    'Почему когда дрочишь/не играет песня играй рука балдей писюн?',
    'как скачать?', 'Ладно./текст', 'Мыний гесли/Демотец окрасской рутии',
    'How?/Текст', 'Я клитор/Запомнили?', 'Подумай о будущем/купи сигарет на завтра',
    'в мои времена поп ит/выглядел так', 'квадратное уравнение/через дискриминант',
    'ДИДЖЕЙ ТЕЙП/АБУ БЭ БУБЭ БУБЭЭЭ', 'Признайся/захотел', 'Кто-нибудь знает/как избавиться от этой хуйни',
    'в поисках папы', 'Ебать его хуй/это же огузок шелбии', 'Ну американцы/и тут преуспели'
)


class DemotivatorCreator:
    def __init__(self):
        self.url = "https://ademotivatory.ru/create/rezult.php"

    async def create_demotivator(
        self,
        image: ImageToDemotivator,
        text: str = None
    ) -> DemotivatorImage | None:
        form_data = aiohttp.FormData()

        if text is None:
            text = choice(DEMO_TEXTS)
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
                except Exception as e:
                    return print(e)

            async with session.get(link) as resp:
                if resp.status != 200:
                    return None
                data = BytesIO(await resp.read())
                name = link.split('/')[-1]
                return DemotivatorImage(name=name, image=data)
