# Arosa'je BACKEND

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Ximawa/Arosa-je_Back.git
   ```

2. Create a virtual environment:

   ```bash
   python -m venv venv
   ```

3. Activate the virtual environment:

   - For Windows:

     ```bash
     venv\Scripts\activate
     ```

   - For macOS/Linux:

     ```bash
     source venv/bin/activate
     ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:

   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

2. Depending on your webserver configuration the URL for db connection in database.py might need to be change