# Import statements
import streamlit
import pandas
from datetime import datetime
import requests
import snowflake.connector
#use this for Control of Flow changes - error message handling
from urllib.error import URLError

[theme]
primaryColor="#F63366"
backgroundColor="#FFFFFF"
secondaryBackgroundColor="#F0F2F6"
textColor="#262730"
font="sans serif"

streamlit.title('Actions and Issues Tracker')

#test snowflake connection
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# ---- test my connection----------------------------------------------------
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_row = my_cur.fetchone()
#streamlit.text(my_data_row)
# ---------------------------------------------------------------------------

my_cur.execute("SELECT * FROM tbl_OperationalActionsRegister")
my_cnx.close()

# don't run anything past here while I troubleshoot
#streamlit.stop()

my_data_rows = my_cur.fetchall()

streamlit.header(':blue[Action/ Issue Register] :runner:')
#streamlit.dataframe(my_data_row)

df = pandas.DataFrame(
   my_data_rows,
   columns=("Action ID", "Entry Date", "Action", "Owner", "Due Date", "Status"))

streamlit.dataframe(df,width=1200)
#streamlit.table(df)

# new action variables
with streamlit.sidebar:
   streamlit.header(':lower_left_ballpoint_pen: :blue[Enter New Action]')
   #action_date = streamlit.text_input('Action date:') # Date picker
   date_select1 = streamlit.date_input('Action date:')
   action_date = date_select1.strftime("%m/%d/%Y")
   action = streamlit.text_input('Action details:')
   owner = streamlit.text_input('Action Owner:')
   #due_date = streamlit.text_input('Action Due Date:') # Date picker
   date_select2 = streamlit.date_input('Action Due Date:')
   due_date = date_select2.strftime("%m/%d/%Y")
   #status = streamlit.text_input('Current Status:') # Status dropdown box
   status = streamlit.selectbox('Current Status:', ('New', 'In Progress', 'Delayed','Complete'))

# Use a Function and Button to Add new record
# Allow the end user to add a new record to the action list
def insert_row_snowflake(action_date, action, owner, due_date, status):
   with my_cnx.cursor() as my_cur:
      #my_cur.execute("INSERT INTO tbl_OperationalActionsRegister (EntryDate, Action, Owner, DueDate, Status) VALUES (to_date('"+ action_date2 +"','DD/MM/YYYY'), '"+ action +"', '"+ owner +"', to_date('"+ due_date +"','DD/MM/YYYY'), '"+ status +"')")
      my_cur.execute("INSERT INTO tbl_OperationalActionsRegister (EntryDate, Action, Owner, DueDate, Status) VALUES ('"+ action_date +"', '"+ action +"', '"+ owner +"', '"+ due_date +"', '"+ status +"')")
      return "New action added " #+ Action


with streamlit.sidebar:   
   if streamlit.button('Create new Action'):
      my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
      back_from_function = insert_row_snowflake(action_date, action, owner, due_date, status)
      my_cnx.close()
      streamlit.text(back_from_function)
