# Admin Panel Setup Wizard

This is the setup wizard for the admin panel of the smart agricultural system. Follow these steps to get started:

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

## Installation

1. Create a virtual environment (recommended):

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

## Starting the Setup Wizard

1. Initialize the database:

   ```bash
   python init_db.py
   ```

2. Start the Flask application:

   ```bash
   flask run
   ```

3. Open your web browser and navigate to:

   ```
   http://localhost:5000/setup
   ```

## Setup Steps

The setup wizard will guide you through the following steps:

1. **Basic Information**
   - System name
   - Admin email
   - Admin password

2. **System Settings**
   - Default language
   - Timezone
   - Date format

3. **Security Settings**
   - Session timeout
   - Maximum login attempts
   - Password expiry
   - Two-factor authentication

4. **Review**
   - Review all settings before finalizing

## After Setup

Once the setup is completed:

1. You will be redirected to the login page
2. Use the admin email and password you set up to log in
3. The system will be ready to use

## Troubleshooting

If you encounter any issues:

1. Make sure all dependencies are installed correctly
2. Check that the database was initialized properly
3. Verify that no other application is using port 5000
4. Check the Flask application logs for any error messages

## Security Notes

- Change the default secret key in production
- Use a strong password for the admin account
- Enable two-factor authentication for additional security
- Regularly update the system and dependencies
