FROM python:3.7

RUN apt-get update
RUN apt-get install -y gconf-service libasound2 libatk1.0-0 libcairo2 libcups2 libfontconfig1 libgdk-pixbuf2.0-0 libgtk-3-0 libnspr4 libpango-1.0-0 libxss1 fonts-liberation libappindicator1 libnss3 lsb-release xdg-utils libappindicator3-1
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install

#RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
RUN curl https://chromedriver.storage.googleapis.com/80.0.3987.106/chromedriver_linux64.zip --output chromedriver.zip && unzip chromedriver.zip -d /usr/bin

WORKDIR /app

RUN pip install --upgrade pip && pip install poetry==1.0.3

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . ./

EXPOSE 8000

# CMD ["/usr/bin/env", "python", "manage.py", "runserver", "0.0.0.0:8000"]
CMD ["/usr/bin/env", "gunicorn", "smart_bookmarks.wsgi:application", "--bind", "0.0.0.0:8000", "--log-file", "-", "--access-logfile", "-", "--reload"]
