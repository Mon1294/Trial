import sqlite3

import pandas as pd
import streamlit as st
from streamlit_lottie import st_lottie

import functions as ft
import takeoutfood as tkf
import interface as itf

img = itf.get_img_as_base64("Picture2.png")
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("data:image/png;base64,{img}");
background-size: 100%;
background-repeat: no-repeat;
background-attachment: local;
}}
</style>
"""

nutrition = pd.read_csv("Nutrition.csv")
portion = pd.read_csv("Portion.csv")
foodchoice = nutrition['Main food description']

# ---

con = sqlite3.connect("database.db")  # create a connection to the database database.db
cur = con.cursor()  # create cursor to execute SQL statements and fetch results from SQL queries
cur.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER, username VARCHAR PRIMARY KEY, password VARCHAR)''')
cur.execute(
    """CREATE TABLE IF NOT EXISTS storage (id INTEGER, foodname VARCHAR, foodcode INTEGER, foodweight FLOAT, exp VARCHAR, expstatus VARCHAR)""")

itf.local_css(r"style.css")

selected = itf.streamlit_menu()

if selected == "About Us":
    st.markdown(page_bg_img, unsafe_allow_html=True)
    flake1 = "🍞"
    flake2 = "🥦"
    flake3 = "🍗"
    flake4 = "🥗"
    flake5 = "🍙"
    flake6 = "🍜"
    flake7 = "🍏"
    flake8 = "🥝"
    st.markdown(
        f"""
        <div class="snowflake">{flake1}</div>
        <div class="snowflake">{flake2}</div>
        <div class="snowflake">{flake3}</div>
        <div class="snowflake">{flake4}</div>
        <div class="snowflake">{flake5}</div>
        <div class="snowflake">{flake6}</div>
        <div class="snowflake">{flake7}</div>
        <div class="snowflake">{flake8}</div>
    """,
        unsafe_allow_html=True, )
    st.markdown("""<h1 style='text-align: center; font-family: Candara; font-size: 50px'>
                YOUR FOOD MANAGEMENT
                </h1>""", unsafe_allow_html=True)
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""<p style='color: #244939; text-align: center; font-family: Cambria;'>
                        introductionnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
                        nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
                        nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
                        nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
                        nnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnnn
                        </p>""", unsafe_allow_html=True)
        with col2:
            # insert gif
            ani_1 = itf.load_lottieurl("https://assets10.lottiefiles.com/packages/lf20_TmewUx.json")
            st_lottie(ani_1, speed=1, reverse=False, loop=True, quality="high", height=None, width=None, key=None)
    st.markdown("""<h1 style='text-align: center; font-size: 15px; font-family: Candara;'>
                Go to Home Page to start
                </h1>""", unsafe_allow_html=True)

else:
    st.markdown(page_bg_img, unsafe_allow_html=True)
    col0_1, col0_2, col0_3, col0_4 = st.columns(4)
    with col0_1:
        pass
    with col0_2:
        st.image("Picture1.png", width=315)
    with col0_1:
        pass
    with col0_1:
        pass
    st.markdown("""<h1 style='text-align: center; font-family: Candara; font-size: 50px'>
                        YOUR FOOD MANAGEMENT
                        </h1>""", unsafe_allow_html=True)

    col1_1, col1_2= st.sidebar.columns(2)
    with col1_1:
        signinbutton = st.button('Sign In')
    with col1_2:
        signupbutton = st.button('Sign Up')

    if 'signup' not in st.session_state:
        st.session_state.signup = False
    if (signupbutton or st.session_state.signup) and signinbutton == False:
        st.session_state.signup = True
        st.session_state.signin = False
        st.sidebar.write('Create New Account')
        new_user_id = ft.get_all_data('users')
        new_user_id = len(new_user_id) + 1
        new_username = st.sidebar.text_input("Username")
        new_password = st.sidebar.text_input("Password", type='password')
        if st.sidebar.button('sign up'):
            try:
                cur.execute('''INSERT INTO users (id, username, password) VALUES (?, ?, ?)''',
                                (new_user_id, new_username, new_password))
                con.commit()
                st.sidebar.success("Succesfully. Sign In to begin")
            except:
                st.sidebar.warning('Username Already Exists.')

    if 'signin' not in st.session_state:
        st.session_state.signin = False
    if (signinbutton or st.session_state.signin) and signupbutton == False:
        st.session_state.signin = True
        st.session_state.signup = False
        st.sidebar.write('Sign In to Your Food Management')
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type='password')
        if 'signinsubmit' not in st.session_state:
            st.session_state.signinsubmit = False
        if st.sidebar.button('sign in') or st.session_state.signinsubmit == True:
            st.session_state.signinsubmit = True
            check_signin = ft.check_signin(username, password)
            if not check_signin:
                st.sidebar.warning("Incorrect password/username.")
            else:
                st.sidebar.success(f"Logged in as {username}.")
                currentid = ft.get_data(tablename='users', category_find='username', category_select='id',
                                        data=username)
                currentdata = ft.get_data(tablename='storage', category_find='id', data=currentid, convert_list=False)
                currentdata = pd.DataFrame(currentdata,
                                           columns=["ID", "Food Name", "Food Code", "Food Weight (Grams)", "EXP",
                                                    "Days Remained"])
                currentdata.index += 1
                st.table(currentdata)
                col2_1, col2_2, col2_3, col2_4, col2_5, col2_6 = st.columns(6)
                with col2_1:
                    pass
                with col2_2:
                    pass
                with col2_3:
                    addbutton = st.button('Add New')
                with col2_4:
                    takebutton = st.button('Take Out')
                with col2_5:
                    pass
                with col2_6:
                    pass

                if 'add' not in st.session_state:
                    st.session_state.add = False
                if (addbutton or st.session_state.add) and takebutton == False:
                    st.session_state.add = True
                    foodname = st.selectbox("Ingredient", foodchoice)
                    # enterfood = st.button('enter')
                    # if enterfood:
                    with st.form('enter'):
                        st.write(foodname)
                        unitchoice = portion.loc[portion['Main food description'] == foodname]
                        unitchoice = unitchoice.loc[unitchoice['weight'] != 0]['Descr'].tolist()
                        unitchoice.append('1 grams')
                        foodunit = st.selectbox("Unit", unitchoice)
                        foodweight = st.number_input("Quantity")
                        foodcode = \
                            nutrition.loc[portion['Main food description'] == foodname]['Food code'].tolist()[0]
                        foodexp = st.date_input("Expiry Day")
                        foodexpstatus = ft.expiry_date(foodexp)
                        submitted = st.form_submit_button("Submit")
                        if submitted:
                            if foodunit != '1 grams':
                                portionratio = portion.loc[(portion['Main food description'] == foodname)]
                                portionratio = \
                                    portionratio.loc[portionratio['Descr'] == foodunit]['weight'].tolist()[0]
                                foodweight = foodweight * portionratio
                            cur.execute("SELECT * FROM storage WHERE id = ? AND foodcode = ? AND exp = ?",
                                        (currentid, foodcode, foodexp))
                            datacheck = cur.fetchall()
                            if not datacheck:
                                cur.execute(
                                    'INSERT INTO storage (id, foodname, foodcode, foodweight, exp, expstatus)'
                                    'VALUES (?, ?, ?, ?, ?, ?)',
                                    (currentid, foodname, foodcode, foodweight, foodexp, foodexpstatus))
                                con.commit()
                            else:
                                currentweight = list(datacheck[0])[-3]
                                foodweight += currentweight
                                cur.execute('UPDATE storage SET foodweight=? WHERE id=? AND foodcode=? AND exp = ?',
                                            (currentid, foodweight, foodcode, foodexp))
                                con.commit()
                if 'take' not in st.session_state:
                    st.session_state.take = False
                if (takebutton or st.session_state.take) and addbutton == False:
                    st.session_state.take = True
                    tkf.take_out(currentid)






