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
   uvicorn app.main:app --reload
   ```

2. Open your web browser and navigate to `http://localhost:8000` to access the application.

## Unit Tests

1. Run the tests

   ```bash
   pytest
   ```
