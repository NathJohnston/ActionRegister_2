# Import statements
import streamlit
import pandas

import requests
import snowflake.connector
#use this for Control of Flow changes - error message handling
from urllib.error import URLError

streamlit.title('Actions and Issues Tracker')

#streamlit.header('Breakfast Menu')
#streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')

#test snowflake connection
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * FROM tblTruckPayloadTargets")

#my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()

streamlit.header("Action/ Issue Register")
#streamlit.dataframe(my_data_row)

df = pandas.DataFrame(
   my_data_rows,
   columns=('test', 'test1', 'test2', 'test3', 'test4')

streamlit.dataframe(df)


# new action variables
action_date = streamlit.text_input('Action date:')
