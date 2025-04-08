# OctoFit Tracker

## Overview

OctoFit Tracker is a fitness tracking application designed for Mergington High School. The application aims to make fitness tracking fun and engaging for students while allowing teachers to monitor their progress remotely. The project is built using a modern web application stack, including a Django backend and a React frontend.

## Project Structure

The project is organized into two main directories: `backend` and `frontend`.

```
octofit-tracker
├── backend          # Contains the Django backend application
│   ├── app         # Main application package
│   ├── manage.py    # Command-line utility for managing the Django project
│   ├── requirements.txt  # Required Python packages
│   └── settings.py  # Configuration settings for the Django application
├── frontend         # Contains the React frontend application
│   ├── public       # Public assets for the frontend
│   └── src         # Source code for the React application
└── .gitignore       # Files and directories to ignore by Git
```

## Setup Instructions

### Backend Setup

1. Navigate to the `backend` directory:
   ```
   cd backend
   ```

2. Create a Python virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

5. Run the Django server:
   ```
   python manage.py runserver
   ```

### Frontend Setup

1. Navigate to the `frontend` directory:
   ```
   cd frontend
   ```

2. Install the necessary dependencies (assuming you have Node.js and npm installed):
   ```
   npm install
   ```

3. Start the React application:
   ```
   npm start
   ```

## Usage

Once both the backend and frontend are running, you can access the OctoFit Tracker application in your web browser at `http://localhost:3000`.

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.