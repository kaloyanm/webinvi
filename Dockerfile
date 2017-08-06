FROM python:3
ENV PYTHONUNBUFFERED 1
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash -
RUN apt-get install nodejs
RUN npm install -g yarn webpack
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
ADD . /code/
RUN yarn install
RUN webpack
RUN python src/manage.py collectstatic --noinput --verbosity=3