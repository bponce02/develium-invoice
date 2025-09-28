FROM python:3-slim

WORKDIR /user/src/app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["nanodjango", "run", "app.py"]
