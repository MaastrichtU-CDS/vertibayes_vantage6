FROM maven:3.8-eclipse-temurin-17-alpine as builder
ARG VERTIBAYES_PATH
ARG N_SCALAR_PRODUCT_PATH
ARG SSH_PRIVATE_KEY
ARG SSH_PUBLIC_KEY

RUN apk update && apk add openssh git

RUN mkdir /build
RUN mkdir /root/.ssh
RUN echo "$SSH_PRIVATE_KEY" > /root/.ssh/id_rsa && \
    echo "$SSH_PUBLIC_KEY" > /root/.ssh/id_rsa.pub && \
    chmod 600 /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa.pub

# make sure your domain is accepted
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan gitlab.com >> /root/.ssh/known_hosts

# Build n-scalar-product protocol
WORKDIR /build
RUN git clone git@gitlab.com:fvandaalen/n-scalar-product-protocol.git

WORKDIR /build/n-scalar-product-protocol/java
RUN mvn install

# Build vertibayes java
WORKDIR /build
RUN git clone git@gitlab.com:fvandaalen/vertibayes.git

WORKDIR /build/vertibayes
RUN mvn package -Dmaven.test.skip

FROM openjdk:17-slim as runner

# This is a placeholder that should be overloaded by invoking
# docker build with '--build-arg PKG_NAME=...'
ARG PKG_NAME="com.florian.vertibayes"
ENV JAR_PATH="/app/vertibayes.jar"
ENV SERVER_PORT=8888

RUN apt update && apt install -y python3 python3-pip python3-dev g++ musl-dev libffi-dev libssl-dev
RUN ln -sf python3 /usr/bin/python
RUN pip3 install --no-cache setuptools wheel poetry

COPY --from=builder /build/vertibayes/target/vertibayes-1.0-SNAPSHOT.jar $JAR_PATH

# install federated algorithm
COPY . /app


WORKDIR /app
RUN poetry install && poetry cache clear -n --all pypi

# Installing torch with pip to be able to install it cpu-only because it is significantly smaller
RUN poetry run pip install torch==1.10.1+cpu -f https://download.pytorch.org/whl/cpu/torch_stable.html
RUN poetry run pip install pgmpy

ENV PKG_NAME=${PKG_NAME}

# Tell docker to execute `docker_wrapper()` when the image is run.
CMD poetry run python -c "from vantage6.tools.docker_wrapper import docker_wrapper; docker_wrapper('${PKG_NAME}')"