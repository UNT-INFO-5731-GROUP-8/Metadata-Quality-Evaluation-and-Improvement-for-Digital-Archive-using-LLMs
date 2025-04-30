# Metadata Project

A web application to generate and validate metadata from PDF files using Excel templates.

## 📦 Getting Started

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

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### 3. Install Required Packages

Install all the necessary Python packages:

```bash
pip install -r requirements.txt
```

### 4. Get a Google API Key

- Go to [Google AI Studio](https://makersuite.google.com/app/apikey).
- Generate an API key.
- Create a `.env` file in the project root and add the key like this:

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

## 📁 Project Structure

```
final_code/
│
├── main.py
├── requirements.txt
├── .env
├── static/
│   ├── style.css
│   └── app.js
├── templates/
│   └── index.html
├── generator.py
└── validator.py

```

---

## 🛠 Features

- Upload Excel templates and PDFs to generate metadata.
- Upload metadata files to validate data quality.
- Visualize scores with charts.
- Google AI integration for smart metadata extraction.

---
