FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

# GROQ_API_KEY must be passed in at runtime, e.g.:
#   docker run -p 8501:8501 -e GROQ_API_KEY=your_key financial-analyzer
CMD ["streamlit", "run", "app/app.py", "--server.address=0.0.0.0"]
