# TODO: Shrink this image size
FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY app .
COPY indeed /indeed

EXPOSE 8502

CMD ["streamlit", "run", "money_gun.py"]
