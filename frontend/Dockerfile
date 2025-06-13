FROM python:3.11-slim

#Set the working directory
WORKDIR /app

#Copy necessary files
COPY requirements.txt .
COPY main.py . 

#Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

#Expose the port for streamlit
EXPOSE 8501

#Run the application
CMD ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]