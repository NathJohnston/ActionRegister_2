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
my_cnx.close()

#my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()


streamlit.header("Action/ Issue Register")
#streamlit.dataframe(my_data_row)

df = pandas.DataFrame(
   my_data_rows,
   columns=("PAYLOADTARGETID", "HUB", "TRUCKCLASS", "PAYLOADTARGET", "VIMS_PAYLOAD"))

streamlit.dataframe(df)


# new action variables
action_date = streamlit.text_input('Action date:')
hub = streamlit.text_input('What Hub?')
truck_class = streamlit.text_input('Enter truck class:')
target_payload = streamlit.text_input('Enter target payload:')
vims_payload = streamlit.text_input('Enter vims payload:')

# Use a Function and Button to Add new record
# Allow the end user to add a new record to the action list
def insert_row_snowflake(hub, truck_class, target_payload, vims_payload):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("INSERT INTO tblTruckPayloadTargets VALUES (11, '"+ hub +"', '"+ truck_class +"', '"+ target_payload +"', '"+ vims_payload +"')")
      return "Thanks for adding " + truck_class

# don't run anything past here while I troubleshoot
#streamlit.stop()
   
if streamlit.button('Create new Action'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function = insert_row_snowflake(hub, truck_class, target_payload, vims_payload)
   my_cnx.close()
   streamlit.text(back_from_function)
