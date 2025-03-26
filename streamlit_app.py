# Import python packages
import streamlit as st
import requests
from snowflake.snowpark.functions import col

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom Smoothie")

name_on_order = st.text_input("Name on Smoothie")
st.write("The name of your Smoothie will be:", name_on_order)

#option = st.selectbox(
#    "What is your favorite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
#    index=None,
#    placeholder="Select favorite fruit...",
#)

#st.write("You selected:", option)

cnx = st. connection ("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select (col ('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_List = st.multiselect(
    "Choose up to 5 ingredients",
    my_dataframe,
    max_selections=5
)

if ingredients_List:
    #st.write(ingredients_List)
    #st.text(ingredients_List)
    ingredients_string = ''

    for fruit_chosen in ingredients_List:
        ingredients_string += fruit_chosen + " "
    #st.write(ingredients_string)

    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order + """' )"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button("Submit order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie '+ name_on_order+ ' is ordered!', icon="✅")

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)
