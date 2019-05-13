FROM python:3.7

RUN pip install selenium, sanic

COPY . .

CMD [ "python", "notice.py" ]