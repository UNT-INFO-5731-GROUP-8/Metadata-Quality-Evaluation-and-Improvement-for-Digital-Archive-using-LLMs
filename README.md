# Metadata Project

A web application to generate and validate metadata from PDF files using Excel templates.

## Getting Started

### 1. Extract the Project

Unzip / Extract the `final_code.zip` file and navigate into the extracted folder:

```bash
cd final_code
```

### 2. Set Up a Virtual Environment

Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate
venv\Scripts\activate

### 3. Install Required Packages

Install all the necessary Python packages:

```bash
pip install -r requirements.txt
```

### 4. Get a Google API Key

- Go to [Google AI Studio](https://makersuite.google.com/app/apikey).
- Generate an API key.
- Update '.env' file with generated key like this:

```env
GOOGLE_API_KEY=your_api_key_here
```

### 5. Run the FastAPI App

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

### 6. Open in Browser

Once the server is running, open your browser and go to:

```
http://127.0.0.1:8000
```

From there, you can access the **Metadata Quality Suite** to generate and validate metadata.

---
