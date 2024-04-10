# technic510-lab3
# Prompt Manager

## Overview
Prompt Manager is a web application built with Streamlit and PostgreSQL, designed to manage and organize ChatGPT prompts. It allows users to create, view, edit, delete, and search for prompts, as well as mark them as favorites for quick access.

## How to Run
To run Prompt Manager on your local machine, follow these steps:

1. **Clone the repository:**

```python
git clone https://github.com/Jaclynjw/technic510-lab3.git
cd technic510-lab3
```

2. **Install dependencies:**
Make sure you have Python installed on your system. Then install the required Python packages using:
```python
pip install -r requirements.txt
```

3. **Set up the PostgreSQL database:**
- Set up a PostgreSQL database either locally or on a cloud service like AWS RDS or Azure Database for PostgreSQL.
- Create the necessary tables by running the SQL commands found in the `init_db()` function within the application code.

4. **Configure environment variables:**
- Create a `.env` file in the root directory of the project.
- Add your database configuration to the `.env` file as follows:
  ```
  DB_HOST=<your-database-host>
  DB_NAME=<your-database-name>
  DB_USER=<your-database-user>
  DB_PASS=<your-database-password>
  ```
- Make sure the `.env` file is listed in your `.gitignore` to prevent sensitive information from being uploaded to version control.

5. **Run the application:**
Execute the following command to run the application:
```
streamlit run app.py
```

6. **Access the application:**
Open your web browser and go to `http://localhost:8501` to start using Prompt Manager.

## Lessons Learned

While working on the Prompt Manager project, I gained valuable insights into full-stack development, particularly in integrating a Streamlit frontend with a PostgreSQL backend. Here are some key takeaways:

- **Streamlit's Power and Simplicity:**
  - Streamlit provided an incredibly rapid way to build and prototype a web application. Its simplicity for creating interactive UI elements without the need for callbacks was enlightening.
  - Learning how to effectively use Streamlit's caching mechanisms to optimize database calls improved the application's performance significantly.

- **Database Management:**
  - Establishing a secure connection to PostgreSQL and managing sessions properly was crucial for data integrity and application stability.
  - I learned the importance of designing a scalable database schema that can evolve with the application's requirements.

- **Environment Management:**
  - The necessity of environment variables for securing sensitive information like database credentials became apparent. It emphasized the importance of security best practices, even in smaller projects.

- **UI/UX Design Considerations:**
  - Even for data-centric applications, user experience is paramount. Implementing features like search and filter improved the usability of the application.
  - The challenge of presenting data in an accessible and understandable way led to experimenting with different UI elements and layouts.

## Questions/Future Improvements

- **Questions:**
  - How can I implement more advanced search capabilities, such as fuzzy search or search by date range, to enhance user experience?
  - What are the best practices for scaling the application to handle a larger number of users and more complex data sets?

- **Future Improvements:**
  - **User Authentication and Authorization:**
    - To accommodate multiple users, implementing a secure authentication system is essential. OAuth or JWT-based authentication could be explored.
  
  - **Advanced Search and Filtering:**
    - Enhancing the search functionality to include fuzzy search, tags, and categories would make it easier for users to organize and find prompts.
  
  - **Responsive Design:**
    - Improving the application's responsiveness to ensure it works seamlessly across different devices and screen sizes.
  
  - **Data Export/Import:**
    - Adding the ability for users to export and import their prompts as a backup or for data analysis purposes.
  
  - **Integration with AI Services:**
    - Exploring the integration of external AI services, like OpenAI's GPT-3, to generate prompts or analyze the stored prompts for insights.
  
  - **Feedback Loop:**
    - Creating a system for users to provide feedback on prompts, such as upvoting or commenting, could foster a community and help improve prompt quality.

