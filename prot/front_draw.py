import pandas as pd
import streamlit as st
import numpy as np
import seaborn as sns
from matplotlib import pyplot as plt

def pre_analysis(m_df):
    st.markdown('Всего транзакций за период: ``{0}``'.format(m_df.shape[0]))
    st.markdown('Суммарный оборот за период: ``{0}`` рублей'.format(int(m_df.amount.sum())))
    st.markdown('Число уникальных покупателей за период: ``{0}``'.format(m_df.cnum.unique().shape[0]))

#@st.cache()#show_spinner=False, suppress_st_warning=True)
def draw_analysis(m_df):

    fig, ax = plt.subplots(2,2, figsize=(15,15))
    plt.rc('axes', titlesize=14) 
    plt.rc('axes', labelsize=14)
    ####
    logrub = np.log10(m_df['amount'])
    sns.distplot(logrub[logrub>-1.0], ax=ax[0,0], color='seagreen')
    ax[0,0].set_title('Распределение логарифма величины транзакций')
    ax[0,0].axvline(logrub.mean(), color='slateblue', 
                    label='Средний возраст')
    ax[0,0].set_xlabel('log10(значение транзакции)')

    # ax[0,1].axvline(m_df['amount'].mean(), color='orange', 
    #                 label='Средний возраст')

    ####
    sns.distplot(m_df.groupby('cnum')['age'].mean(), ax=ax[0,1])
    ax[0,1].set_title('Распределение уникальных покупателей по возрасту')
    ax[0,1].axvline(m_df.groupby('cnum')['age'].mean().mean(), color='orange', 
                    label='Средний возраст')
    ax[0,1].legend()
    ax[0,1].set_xlabel('Возраст')

    ####
    tmp = m_df.groupby('cnum').agg({'amount':'sum', 
                             'age':'mean', 
                             'married_':lambda x: x.unique()[0],
                             'gender':lambda x: x.unique()[0]})
    marmap = {'married':'в браке', 'not_married':'не в браке'}
    tmp['Семья'] = tmp['married_'].apply(lambda x: marmap[x])
    avtrans = tmp['amount'].median()
    tmp['log'] = np.log10(tmp['amount'])

    sns.scatterplot(data=tmp, x='age', y='log', ax=ax[1,0], 
                   hue=tmp['Семья'])
    #ax[1,0].scatter()
    # ax[1,0].scatter(x=tmp['age'],y=tmp['amount'], 
    #                 c=tmp['categorycode'].map(color_map))
    ax[1,0].set_title('Возраст vs log(Сумма транзакций) \nна уникального покупателя')
    ax[1,0].set_ylabel('log(Сумма транзакций)')
    ax[1,0].set_xlabel('Возраст')
    ax[1,0].legend(fontsize=14)

    ####
    ax[1,1].set_title('Возраст vs средняя сумма транзакций \n всех уникальных покупателей')
    avage = tmp['age'].mean()
    tmp['age'] = tmp['age']//10*10
    bot = tmp[tmp['gender']=='F'].groupby('age')['amount'].mean()
    up = tmp[tmp['gender']=='M'].groupby('age')['amount'].mean()
    hist = pd.merge(up, bot, how='outer', left_index=True, right_index=True).fillna(0)

    ax[1,1].bar(hist.index, hist['amount_x'], width=10, color='skyblue')
    ax[1,1].bar(hist.index, hist['amount_y'], bottom=hist['amount_x'], width=10, color='darksalmon')
    ax[1,1].set_xlabel('Возраст')
    ax[1,1].legend(['М', 'Ж'], fontsize=14)

    ####
    st.pyplot(fig)
    return tmp ,avage, avtrans
    ####
def post_analysis(tmp ,avage, avtrans):
    st.markdown('Средний возраст вашего покупателя: ``{0}``'.format(int(avage)))
    st.markdown('Медианная транзакция: ``{0}`` рублей'.format(int(avtrans) ))
    if len(tmp[tmp['gender']=='M']) > 3*len(tmp[tmp['gender']=='F']):
        st.markdown('Ваша аудитория преимущественно мужская')
    elif len(tmp[tmp['gender']=='M'])*3 < len(tmp[tmp['gender']=='F']):
        st.markdown('Ваша аудитория преимущественно женская')
    else:
        st.markdown('Ваша аудитория сбалансирована по полу')