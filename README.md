
# Data Drive Django Project

## About
This is a Django web application that allows users to manage and interact with files and folders in their personal drive. The app provides functionality to upload, create, delete, and manage files and folders.

## Features
- User authentication (register, login, logout)
- File and folder management (upload, create, delete)
- User access control (file ownership)

## Installation

To set up the project locally, follow the steps below:

### 1. Clone the repository:
```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

### 2. Create a virtual environment:
```bash
python3 -m venv env
env\Scripts\activate
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

### 4. Apply migrations:
```bash
python manage.py migrate
```

### 5. Create a superuser (optional, for accessing the admin panel):
```bash
python manage.py createsuperuser
```

### 6. Run the development server:
```bash
python manage.py runserver
```

Your project will be available at `http://127.0.0.1:8000/`.

## Usage
- Register or log in as a user.
- You can upload files, create folders, and manage them through the UI.

## Endpoints

### Authentication URLs

- **Register**
  - URL: `/register/`
  - Method: `GET`, `POST`
  - Description: Register a new user.

- **Login**
  - URL: `/login/`
  - Method: `GET`, `POST`
  - Description: Login to your account.

- **Logout**
  - URL: `/logout/`
  - Method: `GET`
  - Description: Logout from your current session.

### Home

- **Home**
  - URL: `/`
  - Method: `GET`
  - Description: Home page of the application, shows file and folder listings.

### Folder Management

- **Create Folder**
  - URL: `/create_folder/`
  - Method: `POST`
  - Description: Create a new folder.

- **Delete Folder**
  - URL: `/delete_folder/<int:folder_id>/`
  - Method: `POST`
  - Description: Delete a specific folder by its ID.

- **Update Folder Name**
  - URL: `/update_folder_name/`
  - Method: `POST`
  - Description: Update the name of a specific folder.

### File Management

- **Upload File**
  - URL: `/upload/`
  - Method: `POST`
  - Description: Upload a new file.

- **Delete File**
  - URL: `/delete_file/<int:file_id>/`
  - Method: `POST`
  - Description: Delete a specific file by its ID.

- **Update File Name**
  - URL: `/update_file_name/`
  - Method: `POST`
  - Description: Update the name of a specific file.



---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
