
import streamlit
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents Healthy dinner')
streamlit.header('Breakfast menu')
streamlit.text(' 🥣 idly')
streamlit.text('🥗 salad')
streamlit.text('🥑 avacado shake')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

import pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#create function
import requests
import pandas
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice) 
    streamlit.write('The fruit entered ', this_fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json()) 
    return fruityvice_normalized  

# new section display fruityviceapi
streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("please select a fruit to get information")
    else:
        back_from_function=get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)                
except URLError as e:
    streamlit.error()
    
streamlit.header('fruit load list contains:')
#snowflake function
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
            my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
            return my_cur.fetchall()
#add buttoe to load fruit
if streamlit.button('GET FRUIT LIST'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows =get_fruit_load_list()
    streamlit.dataframe(my_data_rows) 
 
#allow user to add fruit
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into  FRUIT_LOAD_LIST values ('from streamlit')")
        return  "Thanks for adding" + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('add a fruit to list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function =insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_function)

streamlit.stop()     

streamlit.write('The user entered ', fruit_choice)
#import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#streamlit.text(fruityvice_response.json())

# json and normalise
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# data table
streamlit.dataframe(fruityvice_normalized)


#import snowflake.connector

add_fruit = streamlit.text_input('add fruit?','Kiwi')
streamlit.write('The user entered ', add_fruit)
#import requests
my_add_fruit =  fruit_choice
streamlit.text(my_add_fruit)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("insert into  FRUIT_LOAD_LIST values ('" + my_add_fruit +"')")
my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
my_data_rows = my_cur.fetchall()
streamlit.header("THE FRUIT LOAD LIST CONTAINS")
streamlit.dataframe(my_data_rows)



