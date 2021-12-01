FROM python:3

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

COPY requirements.txt .
COPY entrypoint.sh .

RUN pip install -r requirements.txt
RUN chmod +x entrypoint.sh

COPY . .

ENTRYPOINT [ "/usr/src/app/entrypoint.sh" ]