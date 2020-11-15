import pandas as pd
import streamlit as st
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt
from front_draw import *

#read DataFrame
df = pd.read_csv('sample.csv', sep=';', index_col=0)
df['purchdate'] = pd.to_datetime(df['purchdate'].apply(lambda x: x.split(' ')[0]))
df.set_index('purchdate', inplace=True)

#Streamlit!!!
## Header
st.title('Pactum')
st.sidebar.title('Укажите параметры')

stores = df.store_name.unique() # все магазины (и не только)

req_store = st.sidebar.selectbox("Укажите наименование магазина?", stores)
subdf = df[df['store_name']==req_store]

if bool(req_store)==True:
    merchants = subdf.merchant_name.unique()
    req_merch = st.sidebar.selectbox("Укажите наименование торговой точки?", merchants)
    subdf = subdf[subdf['merchant_name']==req_merch]

st.write("Ваша база данных:")
st.write(subdf)


## trade characteristics
st.header('Основные показатели торговой точки')

Iord = subdf.sort_index(ascending=True).index.unique()
Imin = subdf.index.min()
Imax = subdf.index.max()
m_min, m_max = st.sidebar.select_slider(
                'Выберите интервал времени для анализа',
                options=list(Iord),
                value=(Imin, Imax), 
                format_func=lambda x: str(x).split(' ')[0])

m_df = subdf.loc[(subdf.index >= m_min) & (subdf.index <= m_max)]


if st.button('Анализ'):
    pre_analysis(m_df)
    tmp ,avage, avtrans = draw_analysis(m_df)
    post_analysis(tmp ,avage, avtrans)
    

## Advertisement
st.header('Формирование рекламного предложения')

option = st.selectbox(
            'Выберите тип рекламного предложения',
            ('Скидка', 'Подарок', 'Действие'))

if option == 'Скидка':
    discont = st.slider('Процент Скидки', min_value=0., max_value=100.0, value=10.0)
    cashb_bool = st.checkbox('Кэшбэк')
    cashb_disc = 0
    if cashb_bool:
        cashb_p = st.slider('Процент Кэшбэка (базовый = 5%)', min_value=0., max_value=50.0, value=5.0)
        if cashb_p > 5.0:
            st.markdown("Вы превысили базовый кэшбэк, отлично! Мы сделаем Вам скидку на это рекламное предложение, за то что согласились проинвестировать дополнительный кэшбэк. Мы рады сотрудничать с Вами!")
            cashb_disc = cashb_p - 5.0
    agemin, agemax = st.select_slider(
                'Выберите возрастную категорию',
                options=list(np.arange(18, 100)),
                value=(18, 25))
    
    sex_bool = st.checkbox('Проводить рассылку для мужчин?')
    sex_bool = st.checkbox('Проводить рассылку для женщин?')
    good = st.selectbox(
            'Выберите тип товара',
            ('Кофе', 'Другие напитки', 'Выпечка'))
    
    price = st.number_input('Введите стоимость товара или услуги', min_value=0.0, max_value=None, value=150.)
    
    frequency = st.selectbox(
            'Как часто отправлять предложение покупателю?',
            ('Иногда', 'Часто', 'Очень часто'))
    price_dict = dict(zip(('Иногда', 'Часто', 'Очень часто'),(100, 380, 790)))
    ad_price = price_dict[frequency]
    
    client_price = price * (1-discont/100)
    if cashb_bool:
        client_cashb = price * (1-discont/100) * cashb_p/100
    pure_revenue = (1-cashb_disc/100) * price * (1-discont/100)
    adv_disc = cashb_disc/2
    ad_price = ad_price*(1 - adv_disc/100)
    
    st.markdown('Стоимость покупки для клиента: **{0}** р.'.format(round(client_price, 1)))
    if cashb_bool:
        st.markdown('Кэшбэк клиента: ``{0}`` р.'.format(round(client_cashb, 1)))
    st.markdown('Ваш чистый доход: ``{0}`` р.'.format(round(pure_revenue, 1)))
    st.markdown('Ваша скидка на рекламное предложение: ``{0}``%'.format(round(adv_disc, 1)))
    st.markdown('Стоимость рекламного предложения: ``{0}`` р.'.format(round(ad_price, 1)))
    
    
if st.button('Сформировать предложение'):
    if cashb_bool:
        st.markdown('Привет! Мы нашли для тебя кофейню, буквально в 107 метрах. Твой любимый Кофе там самый выгодный, смотри сам: Скидка {0}%, да ещё и кэшбэк {1}%. Поспеши!'.format(discont, cashb_p))

if st.button('Опубликовать предложение'):
    st.markdown("Спасибо!")