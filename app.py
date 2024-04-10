import streamlit as st
import psycopg2
from contextlib import closing
from dotenv import load_dotenv
import os

load_dotenv()
# Database connection parameters
DB_HOST = os.environ.get("DB_HOST")
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")

# Add custom styles to make buttons wider
st.markdown(
    """
    <style>
    .stButton>button {
        min-width: 70px;  # Set the minimum width of buttons to prevent wrapping
    }
    </style>
    """,
    unsafe_allow_html=True
)



# Function to connect to the database
def get_db_connection():
    conn = psycopg2.connect(dbname=DB_NAME, user=DB_USER, host=DB_HOST, password=DB_PASS, sslmode='prefer')
    return conn

# Function to initialize the database
def init_db():
    with closing(get_db_connection()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    is_favorite BOOLEAN DEFAULT FALSE
                )
                """
            )
            conn.commit()

# Function to create a new task
def create_task(title, description, is_favorite):
    with closing(get_db_connection()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tasks (title, description, is_favorite) VALUES (%s, %s, %s)",
                (title, description, is_favorite)
            )
            conn.commit()

# Function to list all tasks or filtered/searched tasks
def list_tasks(search_query=None, favorite_filter=None):
    with closing(get_db_connection()) as conn:
        with conn.cursor() as cur:
            base_query = "SELECT id, title, description, is_favorite FROM tasks"
            conditions = []
            params = []
            
            if search_query:
                conditions.append("title ILIKE %s")
                params.append(f"%{search_query}%")
            
            if favorite_filter is not None:
                conditions.append("is_favorite = %s")
                params.append(favorite_filter)
            
            if conditions:
                base_query += " WHERE " + " AND ".join(conditions)
            
            cur.execute(base_query, tuple(params))
            tasks = cur.fetchall()
            return tasks

# Function to update a task's favorite status
def update_favorite_status(task_id, is_favorite):
    with closing(get_db_connection()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE tasks SET is_favorite = %s WHERE id = %s",
                (is_favorite, task_id)
            )
            conn.commit()

# Function to delete a task
def delete_task(task_id):
    with closing(get_db_connection()) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            conn.commit()

# Function to update a task
def update_task(task_id, title, description):
    with closing(get_db_connection()) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE tasks SET title = %s, description = %s WHERE id = %s",
                (title, description, task_id)
            )
            conn.commit()

# Function to delete all tasks
def delete_all_tasks():
    with closing(get_db_connection()) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tasks")
            conn.commit()


# Streamlit UI
def main():
    st.title("Prompt Manager")

    # Initialize the database (ensure the table exists)
    init_db()

    # Input form to create a new task
    with st.form("task_form"):
        title = st.text_input("Prompt Title")
        description = st.text_area("Prompt Description")
        is_favorite = st.checkbox("Favorite")
        submit_button = st.form_submit_button("Create Task")

        if submit_button:
            create_task(title, description, is_favorite)
            st.success("Task Created Successfully!")

    # Search functionality
    st.subheader("Search and Filter")
    search_query = st.text_input("Search by Title")
    favorite_filter = st.selectbox("Filter by Favorite", options=["All", "Favorite", "Not Favorite"], index=0)
    favorite_filter = True if favorite_filter == "Favorite" else False if favorite_filter == "Not Favorite" else None

    # Display existing tasks and a Clear button
    st.subheader("Existing Tasks")
    if st.button("Clear All Tasks"):
        # Set a session state variable to show the confirmation buttons
        st.session_state['confirm_clear'] = True
    
  # If the confirm_clear state is set, show the warning and confirmation options
    if st.session_state.get('confirm_clear', False):
        
        # Inject custom CSS with st.markdown
        with st.container():
            st.warning("Are you sure you want to delete all tasks?")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, delete all tasks"):
                    delete_all_tasks()
                    st.success("All tasks have been deleted.")
                    del st.session_state['confirm_clear']  # Remove the state variable
                    st.experimental_rerun()
            with col2:
                if st.button("Cancel"):
                    del st.session_state['confirm_clear']  # Remove the state variable
                    st.experimental_rerun()
            
    tasks = list_tasks(search_query=search_query, favorite_filter=favorite_filter)
    for task in tasks:
        task_id, task_title, task_description, task_is_favorite = task

        # Display each task title with an expander to show more details
        with st.expander(task_title):
            # Edit mode state for each task
            edit_mode = st.session_state.get(f'edit_mode_{task_id}', False)

            if edit_mode:
                new_title = st.text_input("Title", value=task_title, key=f"title_{task_id}")
                new_description = st.text_area("Description", value=task_description, key=f"desc_{task_id}")
                
                # Save button replaces Edit and Delete in edit mode
                if st.button("Save", key=f"save_{task_id}"):
                    update_task(task_id, new_title, new_description)
                    st.session_state[f'edit_mode_{task_id}'] = False  # Exit edit mode
                    st.experimental_rerun()
            else:
                st.write(f"Description: {task_description}")
                # Checkbox for favorite status, remains visible even outside edit mode
                fav_status = st.checkbox("Favorite", value=task_is_favorite, key=f"fav_{task_id}")
                if fav_status != task_is_favorite:
                    update_favorite_status(task_id, fav_status)
                    st.experimental_rerun()

                # Edit and Delete buttons are only visible when not in edit mode
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Edit", key=f"edit_{task_id}"):
                        st.session_state[f'edit_mode_{task_id}'] = True  # Enter edit mode
                        st.experimental_rerun()

                with col2:
                    if st.button("Delete", key=f"delete_{task_id}"):
                        delete_task(task_id)
                        st.experimental_rerun()



if __name__ == "__main__":
    main()
