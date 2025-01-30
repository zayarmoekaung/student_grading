# Student Grading System

This is a web-based Student Grading System built with Flask (backend) and Svelte (frontend).

## Prerequisites
Ensure you have the following installed:
- Python (>=3.8)
- Node.js (>=16)
- npm or yarn

## Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/zayarmoekaung/student_grading.git
   cd student_grading
   ```

### Backend Setup (Flask)
2. Create a virtual environment:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate  # On Windows
   ```
3. Navigate to the source directory:
   ```sh
   cd source
   ```
4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. Run migrations and seed the database:
   ```sh
   flask db migrate
   flask db upgrade
   flask db seed  # If a seed command is available
   ```

### Frontend Setup (Svelte)
6. Install dependencies and build the frontend:
   ```sh
   npm install
   npm run build
   ```

## Running the Application
After building the frontend, only the Flask server needs to run:
```sh
setx FLASKAPP app.py
flask run
```

## API Documentation
The API documentation is available on Postman:  
[Student Grading System API](https://documenter.getpostman.com/view/13224271/2sAYX2LiZj)

## License
This project is open-source and available under the [MIT License](LICENSE).
