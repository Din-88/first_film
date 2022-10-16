# Flask_UWSGI

FROM ubuntu:22.04

RUN apt update
RUN	apt install --no-install-recommends \
	python3 \
	python3-pip \
	uwsgi \
	python3.10-venv \
	uwsgi-plugin-python3 -y
#	libpq-dev \
#	python3-dev \
#	build-essential -y

RUN useradd --no-create-home uwsgi

WORKDIR /src

COPY ./requirements.txt /src

RUN pip install --no-cache-dir -r requirements.txt

# RUN pip install --no-cache-dir flask
# RUN pip install -r requirements.txt # --no-cache-dir
# RUN pip install --no-cache-dir tk

RUN apt purge python3-pip libpq-dev python3-dev build-essential -y \
	&& apt clean -y \
	&& apt autoclean -y \
	&& apt autoremove -y

# ADD . .
# RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 7000
EXPOSE 7001

# CMD ["/bin/bash"]
# CMD ["python", "/usr/src/app/app.py" ]
CMD ["uwsgi", "--ini", "/src/uwsgi.ini"]