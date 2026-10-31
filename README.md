Home Nursing Management System Expert Domiciliar
This is a production-level system specialized for the control, triage, and management of home nursing care. The application was developed focusing on precision, agility in patient monitoring, and the integrity of clinical data.

🚀 Access the System Online
The application is deployed and ready for production use via the link below:
🔗 Access the application in real-time

🛠️ Architecture and Technologies Used
The application was structured following software development best practices, clearly separating the presentation, business logic, and data persistence layers.

Python (System Core): Main language used to implement complex business rules, triage workflows, and secure manipulation of health data.

Streamlit (Front-end & Dashboard): A reactive user interface optimized for the workflow of healthcare professionals, enabling rapid decision-making through clean visualizations.

Pandas (Data Engineering): Used for the efficient manipulation, modeling, filtering, and organization of structured patient data structures.

SQLite (Persistence & Database): A robust relational database configured to ensure secure storage, reliable transactions, and referential integrity of confidential medical information.

🏗️ Engineering Patterns and Solved Challenges
1. Data Modeling and Relational Consistency
The Python backend was integrated with SQLite using data modeling best practices (such as primary keys, foreign keys, and integrity constraints). This ensures that clinical histories, medical records, and progress notes remain permanently linked to the correct patient, preventing overlapping data errors for sensitive information.

2. State Management and Reactivity
Through Streamlit, an architecture was implemented to handle session state management efficiently. The system updates care dashboards and triage reports in real-time as new nursing records are entered, without requiring heavy full-page reloads.

3. Input Security and Validation
The application features data validation layers using Python to ensure that critical fields (such as vital signs, dosages, and identification data) are entered in the correct format before reaching the database layer, mitigating human operational errors.

📦 How to Run the Project Locally
Clone the repository:

Bash
git clone https://github.com
Enter the project directory:

Bash
cd AcolhimentoEnfermagemExpertDomiciliar
Install the dependencies listed in requirements.txt:

Bash
pip install -r requirements.txt
Run the application:

Bash
streamlit run app.py
