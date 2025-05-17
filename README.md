# Django Project

This is a Django project with a clean setup.

## Setup Instructions

1. Create a virtual environment:
```bash
python3 -m venv venv
```

2. Activate the virtual environment:
```bash
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

The server will start at http://127.0.0.1:8000/

## Project Structure

- `core/` - Main project directory
  - `settings.py` - Project settings
  - `urls.py` - Main URL configuration
  - `wsgi.py` - WSGI configuration
  - `asgi.py` - ASGI configuration
- `manage.py` - Django's command-line utility
- `requirements.txt` - Project dependencies 