FROM python:3.11
WORKDIR /disaster
COPY . /disaster
RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 5432
CMD ["python3", "manage.py", "runserver"]




