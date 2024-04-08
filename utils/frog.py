import random

from utils import weekday_to_string

FROG_LINKS = {
    # monday
    0: [
      'https://i.imgur.com/GlXexz3.jpg',
      'https://i.imgur.com/IJ4Y0Ku.png',
      'https://i.imgur.com/jyncHsa.png',
      'https://i.imgur.com/9WTtCJd.jpg',
      'https://i.imgur.com/Tioa26u.png',
    ],
    # tuesday
    1: [
      'https://i.imgur.com/Hza7wmw.png',
      'https://i.imgur.com/5sffeZV.png',
      'https://i.imgur.com/Tioa26u.png',
      'https://i.imgur.com/tRTTFnN.jpg',
      'https://i.imgur.com/fdAhtRy.jpg',
      'https://i.imgur.com/fNaCgnq.jpg',
      'https://i.imgur.com/k2RW9ZN.jpg',
      'https://i.imgur.com/kRodDQE.jpg',
      'https://i.imgur.com/GlXexz3.jpg',
      'https://i.imgur.com/IJ4Y0Ku.png',
      'https://i.imgur.com/jyncHsa.png',
    ],
    # wednsday
    2: [
      'https://i.imgur.com/bwdxIEh.jpg',
      'https://i.imgur.com/T3DUpmG.png',
      'https://i.imgur.com/ZZyeTZj.jpg',
      'https://i.imgur.com/x8IKfDQ.jpg',
      'https://i.imgur.com/SGgYdO1.jpg',
      'https://i.imgur.com/xR815oG.jpg',
      'https://i.imgur.com/bfqnp7c.jpg',
      'https://i.imgur.com/VRC34VF.jpg',
      'https://i.imgur.com/u19hicR.jpg',
      'https://i.imgur.com/wwiRFCD.jpg',
      'https://i.imgur.com/f2TT4oA.jpg',
      'https://i.imgur.com/0GXWFoT.jpg',
      'https://i.imgur.com/2zlRpNH.jpg',
      'https://i.imgur.com/wqpnVxd.jpg',
      'https://i.imgur.com/CDzAR39.png',
      'https://i.imgur.com/lzLHUxa.jpg',
      'https://i.imgur.com/DHbXJHC.jpg',
      'https://i.imgur.com/caxb2SK.png',
      'https://i.imgur.com/5kE8OOg.png',
      'https://i.imgur.com/VL7b87T.jpg',
      'https://i.imgur.com/PSYOMKz.png',
      'https://i.imgur.com/M2NpO75.png',
      'https://i.imgur.com/ZlK2aK0.png',
      'https://i.imgur.com/QeIkQQx.jpg',
      'https://i.imgur.com/bD3Uj3y.png',
      'https://i.imgur.com/4pTKArH.png',
      'https://i.imgur.com/HTmeJ7K.jpg',
      'https://i.imgur.com/dECkIuJ.jpg',
      'https://i.imgur.com/gTh5pA3.jpg',
      'https://i.imgur.com/TY0XG9n.png',
      'https://i.imgur.com/oI9TJ0e.jpg',
      'https://i.imgur.com/h09m9JJ.png',
      'https://i.imgur.com/ZxhyppT.jpg',
      'https://i.imgur.com/kJRLMuk.png',
      'https://i.imgur.com/lrHDc3B.png',
      'https://i.imgur.com/tMiwB6k.jpg',
      'https://i.imgur.com/0etyoGJ.png',
      'https://i.imgur.com/5JxRRIn.png',
      'https://i.imgur.com/6vuEt0w.png',
      'https://i.imgur.com/MeM1e37.jpg',
      'https://i.imgur.com/bN1cdRq.jpg',
      'https://i.imgur.com/eD8Z8d0.jpg',
      'https://i.imgur.com/VbJGRKh.png',
      'https://i.imgur.com/GE6eTBD.jpg',
      'https://i.imgur.com/C0FYcx8.jpg',
      'https://i.imgur.com/1jwAFFK.png',
      'https://i.imgur.com/hxt4pLK.jpg',
      'https://i.imgur.com/uKYR1Yr.jpg',
      'https://i.imgur.com/oXEW3wB.jpg',
      'https://i.imgur.com/D7SmhVa.png',
      'https://i.imgur.com/u6TeocD.png',
      'https://i.imgur.com/qmQxn9A.png',
      'https://i.imgur.com/7SnEEPo.png',
      'https://i.imgur.com/HsVtnn9.png',
      'https://i.imgur.com/ULmrFsM.jpg',
      'https://i.imgur.com/jmqlkRc.jpg',
      'https://i.imgur.com/fLhFj25.jpg',
      'https://i.imgur.com/X51EzQ0.jpg',
      'https://i.imgur.com/jTKoBc6.jpg',
      'https://i.imgur.com/e4625tL.jpg',
      'https://i.imgur.com/ocRNoXe.jpg',
      'https://i.imgur.com/LDE2Xhm.jpg',
      'https://i.imgur.com/RoQCS7z.jpg',
      'https://i.imgur.com/lJykHzg.png',
      'https://i.imgur.com/hUYdWjt.png',
      'https://i.imgur.com/j9hKjce.png',
      'https://i.imgur.com/taLRoH3.jpg',
      'https://i.imgur.com/oVYaHWo.jpg',
      'https://i.imgur.com/5OfMZ0Q.png',
      'https://i.imgur.com/PtY1Jsz.png',
      'https://i.imgur.com/O63mb6U.png',
      'https://i.imgur.com/H78ce90.png',
      'https://i.imgur.com/lSCeq6Z.png',
      'https://i.imgur.com/530lgdv.jpg',
      'https://i.imgur.com/FoupGuq.jpg',
      'https://i.imgur.com/maJb06u.png',
      'https://i.imgur.com/idtoVA9.png',
      'https://i.imgur.com/HRLt94d.jpg',
      'https://i.imgur.com/ZqWseO7.png',
      'https://i.imgur.com/EhbRIhw.png',
      'https://i.imgur.com/yYs2r93.png',
      'https://i.imgur.com/YED3zp6.png',
      'https://i.imgur.com/TuzVbsY.png',
      'https://i.imgur.com/DEeR0vu.jpg',
      'https://i.imgur.com/MxiSGB8.png',
      'https://i.imgur.com/ZFwuUMM.jpg',
      'https://i.imgur.com/fTNthmA.png',
      'https://i.imgur.com/EGipqja.png',
      'https://i.imgur.com/0YfhQSb.png',
      'https://i.imgur.com/DkmZi95.jpg',
      'https://i.imgur.com/oWxtBGA.jpg',
      'https://i.imgur.com/7CYqfrL.jpg',
      'https://i.imgur.com/gHHHT2T.jpg',
      'https://i.imgur.com/BlbtyMA.jpg',
      'https://i.imgur.com/W4WTe9O.jpg',
      'https://i.imgur.com/uC71wJ8.jpg',
      'https://i.imgur.com/FHeytBl.jpg',
      'https://i.imgur.com/KiZt03Y.jpg',
      'https://i.imgur.com/mgJoS4Z.png',
      'https://i.imgur.com/B6YeZwP.png',
      'https://i.imgur.com/Cwt1VjN.jpg',
      'https://i.imgur.com/OsjolA0.jpg',
      'https://i.imgur.com/Dyft9vx.jpg',
      'https://i.imgur.com/HhGDG1f.jpg',
      'https://i.imgur.com/BL4Im8y.jpg',
      'https://i.imgur.com/d9hwRIj.png',
      'https://i.imgur.com/BVs0VM7.jpg',
      'https://i.imgur.com/3iYzLhw.png',
      'https://i.imgur.com/IB5iHXQ.jpg',
      'https://i.imgur.com/qu1oqrO.jpg',
      'https://i.imgur.com/VmT5D3O.jpg',
      'https://i.imgur.com/yuaI1hH.jpg',
      'https://i.imgur.com/J9UYigA.jpg',
      'https://i.imgur.com/GnJK6Xs.png',
      'https://i.imgur.com/ZBArsY0.png',
      'https://i.imgur.com/19B3dmO.jpg',
      'https://i.imgur.com/68E4DfJ.png',
      'https://i.imgur.com/41JMr08.jpg',
      'https://i.imgur.com/tCHpusu.jpg',
      'https://i.imgur.com/3yyuN7P.png',
      'https://i.imgur.com/WtddfnQ.jpg',
      'https://i.imgur.com/CyIsfNA.jpg',
      'https://i.imgur.com/LWctbN6.jpg',
      'https://i.imgur.com/AG5cSky.jpg',
      'https://i.imgur.com/1AFoB7t.png',
      'https://i.imgur.com/YzCekZM.jpg',
      'https://i.imgur.com/ZRNtvdR.png',
      'https://i.imgur.com/T5pGBNP.png',
      'https://i.imgur.com/AhSa3vE.png',
      'https://i.imgur.com/nIvXwdX.png',
      'https://i.imgur.com/iDKkjdD.png',
      'https://i.imgur.com/eu53jgO.jpg',
      'https://i.imgur.com/E5jTkuK.png',
      'https://i.imgur.com/B4BrvoN.jpg',
    ],
    # thursday
    3: [
      'https://i.imgur.com/pFnqk0S.jpg',
      'https://i.imgur.com/WM73Dog.jpg',
      'https://i.imgur.com/TSHZCr7.jpg',
      'https://i.imgur.com/c1dHJP8.png',
      'https://i.imgur.com/Sty5GMZ.jpg',
      'https://i.imgur.com/QoAtJjA.png',
      'https://i.imgur.com/Flupiea.png',
      'https://i.imgur.com/ym1CNuN.png',
      'https://i.imgur.com/SEGgQBl.jpg',
      'https://i.imgur.com/Mffp0Ho.jpg',
    ],
    # friday
    4: [
      'https://i.imgur.com/OnfVaHt.png',
      'https://i.imgur.com/v8redB6.jpg',
    ],
    # saturday
    5: [
      'https://i.imgur.com/DCD0OB3.jpg',
      'https://i.imgur.com/t9Q98AJ.jpg',
    ],
    # sunday
    6: [
      'https://i.imgur.com/IFIS02O.jpg',
      'https://i.imgur.com/3iJaILL.jpg',
    ]
}
ANY = [
    'https://i.imgur.com/dcR8HrD.jpg',
    'https://i.imgur.com/krav1NI.jpg',
    'https://i.imgur.com/8ycxJka.png',
    'https://i.imgur.com/vgy26bm.jpg',
    'https://i.imgur.com/MpJpaNI.jpg',
]
NOT_WEDNSDAYs_LINKS = [
    'https://i.imgur.com/Gjy73VS.png',
    'https://i.imgur.com/niDB8uh.png',
    'https://i.imgur.com/5W1JWL5.jpg',
    'https://i.imgur.com/l1NZRjK.jpg',
    'https://i.imgur.com/CmOGdEo.jpg',
    'https://i.imgur.com/GjIPeGu.png',
    'https://i.imgur.com/9RL5UdD.jpg',
    'https://i.imgur.com/Q043FrN.png',
    'https://i.imgur.com/5hMSxot.png',
    'https://i.imgur.com/iz5woiD.png',
    'https://i.imgur.com/ejTdmVN.png',
    'https://i.imgur.com/ceYyuIi.png',
    'https://i.imgur.com/LOIQGqs.png',
    'https://i.imgur.com/f0JCZkP.jpg',
    'https://i.imgur.com/jdyS5LY.jpg',
    'https://i.imgur.com/6kR9W9o.jpg',
    'https://i.imgur.com/rLtHyGx.jpg',
]
FROG_LINKS = {k: v for k, v in FROG_LINKS.items() if v.extend(ANY) is None}
FROG_LINKS = {k: v for k, v in FROG_LINKS.items() if (k != 2 and v.extend(NOT_WEDNSDAYs_LINKS) is None) or k == 2}


class FrogTextConstructor:
    def __init__(self):

        self.NOT_WEDNSDAYS_DAY = ('похуй, главное, что не среда', 'точно не среда', 'не среда',
                                  'не не не среда', 'не лягуший день', 'обычный день недели', 'сегодня')
        self.WEDNSDAYS_DAY = ('СВЯЩЕННЫЙ ДЕНЬ', 'ЕБУЧАЯ МАТЬ ЕГО СРЕДА', 'МОЙ ЛЮБИМЫЙ ДЕНЬ НЕДЕЛИ', 'КВА-КВА-КВА ДЕНЬ',
                              'ТОТ САМЫЙ ДЕНЬ', 'просто среда, ладно я шучу, АХУННАЯ МАТЬ ЕГО СРЕДА', 'среда моя среда',
                              'хороший день, то есть среда', 'среда', 'ДЕНЬ X')
        self.NOT_WEDNSDAYS_ENDINGS = ('Может следующий день будет особенным?(например средой)',
                                      'Ну ничего, среда уже скоро', 'Не ничего, и на нашей улице будет среда',
                                      'Хорошо, что среда уже скоро')
        self.WEDNSDAYS_ENDINGS = ('Из плохих новостей: следующая среда будет только через неделю',
                                  'Ладно, это просто обычный день недели, КОТОРЫЙ ПИЗЖЕ В СТО РАЗ ЛЮБОГО ДРУГОГО ДНЯ',
                                  'Помолимся же жабьему богу за этот чудесный день', 'Какой же это кааааайф')

    def create_text(self, weekday_num: int):
        weekday = weekday_to_string(weekday_num)
        if weekday_num != 2:
            weekday_text = random.choices((weekday, random.choice(self.NOT_WEDNSDAYS_DAY)), (0.4, 0.6), k=1)[0]
            weekday_ending = random.choices(('', random.choice(self.NOT_WEDNSDAYS_ENDINGS)), (0.4, 0.6), k=1)[0]
        else:
            weekday_text = random.choices((weekday, random.choice(self.WEDNSDAYS_DAY)), (0.4, 0.6), k=1)[0]
            weekday_ending = random.choices(('', random.choice(self.WEDNSDAYS_ENDINGS)), (0.4, 0.6), k=1)[0]
        return f"Сегодня {weekday_text}, мои чюваки. {weekday_ending}\n"
