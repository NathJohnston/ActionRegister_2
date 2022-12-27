# Import statements
import streamlit
import pandas
from datetime import datetime
import requests
import snowflake.connector
#use this for Control of Flow changes - error message handling
from urllib.error import URLError


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
      streamlit.success(back_from_function)

#Retrieve list of active action ID's
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_id_cur = my_cnx.cursor()

my_id_cur.execute("SELECT Action_ID FROM tbl_OperationalActionsRegister WHERE Status <> 'Complete'")
my_cnx.close()

#initial effort, presents data in following format (1),
#action_ids = my_id_cur.fetchall()
#select_id = streamlit.selectbox('Select Action ID to Update:',action_ids)

#action_ids = list(my_id_cur.fetchall())
#select_id = streamlit.selectbox('Select Action ID to Update:',action_ids)

streamlit.subheader(':orange[Update existing Active Action]')

# don't run anything past here while I troubleshoot
#streamlit.stop()

action_ids = my_id_cur.fetchall() 
final_result = [i[0] for i in action_ids]
select_id = streamlit.selectbox('Select Action ID:',final_result)

if streamlit.button('Update Action'):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   my_cur = my_cnx.cursor()
   #update_response = update_selected_action(action, owner, due_date, status)
   my_cur.execute("UPDATE tbl_OperationalActionsRegister SET Action = '"+ action +"', Owner = '"+ owner +"', DueDate = '"+ due_date +"', Status = '"+ status +"' WHERE Action_ID = "+ str(select_id) +"")
   my_cnx.close()
   streamlit.success('Action ID: ' + str(select_id) + ' Update Succeded')
 


def update_selected_action(ud_action, ud_owner, ud_due_date, ud_status):   
   with my_cnx.cursor() as my_cur:
      my_cur.execute("UPDATE tbl_OperationalActionsRegister SET Action = '"+ ud_action +"', Owner = '"+ ud_owner +"', DueDate = '"+ ud_due_date +"', Status = '"+ ud_status +"' WHERE Action_ID = 3")
      #my_cnx.close()
   return "Action ID ... Updated " #+ Action
