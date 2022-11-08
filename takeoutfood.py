import pandas as pd
import streamlit as st
import functions as ft
import sqlite3

connect = sqlite3.connect("database.db", check_same_thread=False)
cur = connect.cursor()


def calculatecalo(foodcode, currentid, i, food_removed):
    portion = pd.read_csv("Portion.csv")
    nutrion = pd.read_csv("Nutrition.csv")
    unitchoice_0 = portion.loc[portion['Food code'] == foodcode]
    unitchoice_0 = unitchoice_0.loc[unitchoice_0['weight'] != 0]['Descr']
    unitchoice = unitchoice_0.tolist()
    unitchoice.append('1 grams')
    unitcol, expcol, weightcol = st.columns(3)
    with unitcol:
        foodunit = st.selectbox('Choose the unit:', unitchoice, key=i + 1)
    with expcol:
        cur.execute('''SELECT exp FROM storage WHERE id=? AND foodcode=?''', (currentid, foodcode))
        expchoice = cur.fetchall()
        expchoice = [list(exp)[0] for exp in expchoice]
        foodexp = st.selectbox("EXP", expchoice, key=i+2)
    with weightcol:
        cur.execute("SELECT foodweight FROM storage WHERE id=? AND foodcode=? AND exp=?",
                    (currentid, foodcode, foodexp))
        foodweight_limit = cur.fetchall()
        foodweight_limit = list(foodweight_limit[0])[0]
        if foodunit != '1 grams':
            portionratio = portion.loc[(portion['Food code'] == foodcode) & (unitchoice_0 == foodunit)]
            foodweight_limit = foodweight_limit/int(portionratio['weight'])
        foodweight = st.number_input('Enter the number you want to have:', max_value=foodweight_limit, key=i + 3)
        if foodunit != '1 grams':
            portionratio = portion.loc[(portion['Food code'] == foodcode) & (unitchoice_0 == foodunit)]
            foodweight = int(portionratio['weight']) * foodweight
    nutri = nutrion.loc[nutrion['Food code'] == foodcode]
    temp = {'id': currentid, 'foodcode': foodcode, 'foodexp': foodexp, 'weight_remove': foodweight}
    food_removed.append(temp)
    return foodweight, nutri, food_removed


def add(options, i, calo, protein, carb, fat, currentid, food_removed):
    foodcode = ft.get_data(tablename='storage', category_find='foodname', category_select='foodcode', data=options)
    st.write('Product:', options)
    foodweight, nutri, food_removed = calculatecalo(foodcode, currentid, i, food_removed)
    calo += int(nutri['Energy']) * (foodweight / 100)
    protein += int(nutri['Protein (g)']) * (foodweight / 100)
    carb += int(nutri['Carbohydrate (g)']) * (foodweight / 100)
    fat += int(nutri['Total Fat (g)']) * (foodweight / 100)
    i += 3
    return calo, protein, carb, fat, i, food_removed


def finish(calo, protein, carb, fat):
    st.write(f'Total calo: {calo} kcal')
    st.write(f'Total carb: {carb} g')
    st.write(f'Total protein: {protein} g')
    st.write(f'Total fat: {fat} g')


def take_out(currentid):
    prd_data = set(ft.get_data(tablename='storage', category_select='foodname', category_find='id',
                               data=currentid, get_one=False))
    gram, calo, protein, carb, fat, i = 0, 0, 0, 0, 0, 0
    food_removed = []
    multichoice = st.multiselect('Pick products', prd_data)
    for options in multichoice:
        calo, protein, carb, fat, i, food_removed = add(options, i, calo, protein, carb, fat, currentid, food_removed)
    finish(calo, protein, carb, fat)
    if st.button('confirm'):
        for i in food_removed:
            ft.take_out_food(currentid=i['id'], foodcode=i['foodcode'], foodexp=i['foodexp'],
                             foodweight=i['weight_remove'])
