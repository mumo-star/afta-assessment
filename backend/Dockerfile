FROM python:3.11-slim

#Set the working directory
WORKDIR /app

#Copy necessary files
COPY requirements.txt .
COPY loan.py .

#Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Expose the port for fastapi
EXPOSE 8000

#Run the application
CMD ["uvicorn", "loan:app", "--host", "0.0.0.0", "--port", "8000"]