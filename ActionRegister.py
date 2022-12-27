# Import statements
import streamlit
import pandas
from datetime import datetime
import requests
import snowflake.connector
#use this for Control of Flow changes - error message handling
from urllib.error import URLError

   #Set page title
streamlit.title('Actions and Issues Tracker')

   #Connect to Snowflake and instantiate cursor object
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_dataframe_cur = my_cnx.cursor()

   #Populate the cursor with the data in the tbl_OperationalActionsRegister table using execute and close cursor
my_dataframe_cur.execute("SELECT * FROM tbl_OperationalActionsRegister")
my_cnx.close()

   #Populate my_data_rows variable with cursor results
my_data_rows = my_dataframe_cur.fetchall()

   #Create action table header
streamlit.header(':blue[Action/ Issue Register] :runner:')

   #Populate dataframe
df = pandas.DataFrame(
   my_data_rows,
   columns=("Action ID", "Entry Date", "Action", "Owner", "Due Date", "Status"))

streamlit.dataframe(df)#,width=3000,height=245)


   #create new action variables and objects in sidebar object
with streamlit.sidebar:
   streamlit.header(':lower_left_ballpoint_pen: :blue[Enter New Action]')
   date_select1 = streamlit.date_input('Action date:')
      #convert the date to the required string format
   action_date = date_select1.strftime("%m/%d/%Y")
   action = streamlit.text_input('Action details:')
   owner = streamlit.text_input('Action Owner:')
   date_select2 = streamlit.date_input('Action Due Date:')
      #convert the date to the required string format
   due_date = date_select2.strftime("%m/%d/%Y")
   status = streamlit.selectbox('Current Status:', ('New', 'In Progress', 'Delayed','Complete'))

# -------------------------------------FUNCTIONS--------------------------------------
   #Use a Function and Button to Add new record
   #Allow the end user to add a new record to the action list
def insert_row_snowflake(action_date, action, owner, due_date, status):
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   with my_cnx.cursor() as my_cur:
      my_cur.execute("INSERT INTO tbl_OperationalActionsRegister (EntryDate, Action, Owner, DueDate, Status) VALUES ('"+ action_date +"', '"+ action +"', '"+ owner +"', '"+ due_date +"', '"+ status +"')")
      my_cnx.close()
      return "New action added " #+ Action
     
   #Function to update record based on select box selected id
   #Allow the end user to add a new record to the action list
def update_selected_action(ud_action, ud_owner, ud_due_date, ud_status): 
   my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
   with my_cnx.cursor() as my_cur:
      my_cur.execute("UPDATE tbl_OperationalActionsRegister SET Action = '"+ ud_action +"', Owner = '"+ ud_owner +"', DueDate = '"+ ud_due_date +"', Status = '"+ ud_status +"' WHERE Action_ID = "+ str(select_id) +"")
      my_cnx.close()
   return str(select_id)
# ---------------------------------------------------------------------------------

   #Insert new action record based on sliderbar objects
with streamlit.sidebar:   
   if streamlit.button('Create new Action'):
      back_from_function = insert_row_snowflake(action_date, action, owner, due_date, status)
      streamlit.success(back_from_function)

      #Create update action header
streamlit.subheader(':orange[Update existing Active Action - Select Action ID]')      

   #Retrieve list of active action ID's
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_id_cur = my_cnx.cursor()
my_id_cur.execute("SELECT Action_ID FROM tbl_OperationalActionsRegister WHERE Status <> 'Complete'")
my_cnx.close()

   #format the results in the cursor and populate the select box object
action_ids = my_id_cur.fetchall() 
final_result = [i[0] for i in action_ids]
select_id = streamlit.selectbox('Select Action ID:',final_result, label_visibility="collapsed")
#select_id = streamlit.selectbox(:blue[Select Action ID:],('Email', 'Home phone', 'Mobile phone')) -- does not work

   #Retrieve Action based on selected action ID
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
action_to_update_cur = my_cnx.cursor()
action_to_update_cur.execute("SELECT * FROM tbl_OperationalActionsRegister WHERE Action_ID = "+ str(select_id) +"")
my_cnx.close()


updateAction = action_to_update_cur.fetchmany()
for row in updateAction:
   ud_action = streamlit.text_input('Action details:',f"{row[2]}")
   ud_owner = streamlit.text_input('Owner:',f"{row[3]}")
   ud_due_date = streamlit.text_input('Due Date:',f"{row[4]}")
   ud_status = streamlit.text_input('Status:',f"{row[5]}")

#col1,col2 = streamlit.columns(2)
#with col1:
#   for row in updateAction:
#       Up_action = streamlit.text_input('Action details:',f"{row[2]}")
      
#with col2:
#   for row in updateAction:
#       Up_action = streamlit.text_input('Action details:',f"{row[3]}") 
   
   


     
      
   #Update record for action ID selected in the selected_id selectbox
if streamlit.button('Update Action'):
   back_from_function = update_selected_action(action, owner, due_date, status)
   streamlit.success('Action ID: ' + str(back_from_function) + ' Update Succeded')
 

#TROUBLESHOOTING CODE
# ---- test my connection----------------------------------------------------
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
#my_data_row = my_cur.fetchone()
#streamlit.text(my_data_row)
# ---------------------------------------------------------------------------


# don't run anything past here while I troubleshoot
#streamlit.stop()
