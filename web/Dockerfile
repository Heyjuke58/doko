FROM python:3.12.0-bookworm

WORKDIR /usr/src/app

# prevent python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# prevent python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat-traditional
RUN apt install -y curl

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# debugging
RUN pip install debugpy

# # Download latest nodejs binary
# RUN curl https://nodejs.org/dist/v18.18.2/node-v18.18.2-linux-x64.tar.xz -O

# # Extract & install
# RUN tar -xf node-v18.18.2-linux-x64.tar.xz
# RUN ln -s /node-v18.18.2-linux-x64/bin/node /usr/local/bin/node
# RUN ln -s /node-v18.18.2-linux-x64/bin/npm /usr/local/bin/npm
# RUN ln -s /node-v18.18.2-linux-x64/bin/npx /usr/local/bin/npx

ENV NODE_VERSION=18.18.2
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.5/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"

COPY . /usr/src/app/

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]