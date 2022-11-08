import sqlite3
from datetime import datetime, date
import streamlit as st
from pretty_notification_box import notification_box

connect = sqlite3.connect("database.db", check_same_thread=False)
cur = connect.cursor()


def get_data(tablename, category_find, data, category_select='*', convert_list=True, get_one=True):
    command = f'SELECT {category_select} FROM {tablename} WHERE {category_find} = ?'
    cur.execute(command, (data,))
    result = cur.fetchall()
    if convert_list:
        result = [list(i)[0] for i in result]
        if get_one:
            result = result[0]
    return result


def get_all_data(table_name):
    command = f'SELECT * FROM {table_name}'
    cur.execute(command)
    result = cur.fetchall()
    return result


def get_current_food(currentid, foodcode, foodexp, category_select='*', get_one=True):
    command = f"SELECT {category_select} FROM storage WHERE id =? AND foodcode=? AND exp=?"
    cur.execute(command, (currentid, foodcode, foodexp))
    result = cur.fetchall()
    result = [list(i)[0] for i in result]
    if get_one:
        result = result[0]
    return result


def check_signin(username, password):
    cur.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    result = cur.fetchall()
    return result


def take_out_food(currentid, foodcode, foodexp, foodweight):
    currentweight = get_current_food(currentid, foodcode, foodexp, 'foodweight')
    currentweight = currentweight - foodweight
    if currentweight > 0:
        cur.execute('UPDATE storage SET foodweight=? WHERE foodcode=? AND exp = ?', (currentweight, foodcode, foodexp))
        connect.commit()
    elif currentweight <= 0:
        cur.execute("DELETE FROM storage WHERE id = ? AND foodcode = ? AND exp = ?", (currentid, foodcode, foodexp))
        connect.commit()


# test
def expiry_date(foodexp):
    # experation_date: ngay het han
    # today_date: ngay hien tai
    # time_gap: khoang cach thoi gian giua 2 ngay
    # experation_date = datetime.strptime(foodexp, "%y-%m-%d").date()
    today_date = date.today()
    time_gap = foodexp - today_date
    if time_gap.days < 0:
        expstatus = 'expired'
    else:
        expstatus = time_gap.days
    return expstatus


# color table
def color_coding(data):
    if data["Days Remained"].lower() == 'expired':
        color = '#F3DEBA'
    elif 0 <= int(data["Days Remained"]) <= 2:
        color = '#FFEFD6'
    else:
        color = 'white'
    return [f'background-color: {color}'] * len(data)


# new: delete all expired
def delete_expired(currentid):
    currentdata = get_data(tablename='storage', category_find='id', data=currentid, convert_list=False)
    for i in currentdata:
        if i[-1].lower() == 'expired':
            cur.execute("DELETE FROM storage WHERE id = ? AND foodcode = ? AND exp = ?", (currentid, i[2], i[-2]))
            connect.commit()


# new: update days remained (when new day begins)
def update_days_remained(currentid):
    currentdata = get_data(tablename='storage', category_find='id', data=currentid, convert_list=False)
    for i in currentdata:
        exp = datetime.strptime(i[-2], "%Y-%m-%d").date()
        currentdayremained = expiry_date(exp)
        cur.execute('UPDATE storage SET expstatus=? WHERE id=? AND foodcode=? AND exp = ?',
                    (currentdayremained, currentid, i[2], exp))
        connect.commit()


# new: noti
def noti(currentdata):
    key = 0
    for i in currentdata:
        key += 1
        if i[-1] == 'expired':
            notification_box(icon='warning', title='Warning',
                             textDisplay=f"{i[1]} has expired",
                             styles=None, key=key, externalLink=None, url=None)
        elif 0 < int(i[-1]) <= 5:
            notification_box(icon='warning', title='Warning',
                             textDisplay=f"{i[1]} has {i[-1]} days left",
                             styles=None, key=key, externalLink=None, url=None)
