# Import statements
import streamlit
import pandas

import requests
import snowflake.connector
#use this for Control of Flow changes - error message handling
from urllib.error import URLError

streamlit.title('Actions and Issues Tracker')



#test snowflake connection
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# ---- test my connection----------------------------------------------------
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text(my_data_row)
# ---------------------------------------------------------------------------

# don't run anything past here while I troubleshoot
streamlit.stop()
my_cur.execute("SELECT * FROM tbl_OperationalActionRegister")
my_cnx.close()



#my_data_row = my_cur.fetchone()
my_data_rows = my_cur.fetchall()


streamlit.header("Action/ Issue Register")
#streamlit.dataframe(my_data_row)

df = pandas.DataFrame(
   my_data_rows,
   columns=("Action ID", "Entry Date", "Action", "Owner", "Due Date", "Status"))

streamlit.dataframe(df)


# new action variables
action_date = streamlit.text_input('Action date:') # Date picker
Action = streamlit.text_input('Action details:')
Owner = streamlit.text_input('Action Owner:')
DueDate = streamlit.text_input('Action Due Date:') # Date picker
Status = streamlit.text_input('Current Status:') # Status dropdown box

# Use a Function and Button to Add new record
# Allow the end user to add a new record to the action list
def insert_row_snowflake(hub, truck_class, target_payload, vims_payload):
   with my_cnx.cursor() as my_cur:
      my_cur.execute("INSERT INTO tbl_OperationalActionRegister (EntryDate, Action, Owner, DueDate, Status) VALUES ('"+ action_date +"', '"+ Action +"', '"+ Owner +"', '"+ DueDate +"', '"+ Status +"')")
      return "Thanks for adding " + truck_class


   
if streamlit.button('Create new Action'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   back_from_function = insert_row_snowflake(action_date, Action, Owner, DueDate, Status)
   my_cnx.close()
   streamlit.text(back_from_function)
