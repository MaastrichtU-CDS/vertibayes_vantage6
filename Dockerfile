FROM maven:3.8-eclipse-temurin-17-alpine as builder

ARG VERTIBAYES_PATH
ARG N_SCALAR_PRODUCT_PATH
ARG SSH_PRIVATE_KEY
ARG SSH_PUBLIC_KEY

RUN apk update && apk add openssh git
RUN apk add --no-cache gcompat

RUN mkdir /build
RUN mkdir /root/.ssh
RUN echo "$SSH_PRIVATE_KEY" > /root/.ssh/id_rsa && \
    echo "$SSH_PUBLIC_KEY" > /root/.ssh/id_rsa.pub && \
    chmod 600 /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa.pub

# make sure your domain is accepted
RUN touch /root/.ssh/known_hosts
RUN ssh-keyscan github.com >> /root/.ssh/known_hosts

# Build n-scalar-product protocol
WORKDIR /build
RUN git clone --branch 3.0-stable git@github.com:MaastrichtU-CDS/n-scalar-product-protocol.git

WORKDIR /build/n-scalar-product-protocol/java
RUN mvn install

# Build vertibayes java
WORKDIR /build
RUN git clone --branch main git@github.com:MaastrichtU-CDS/vertibayes.git

WORKDIR /build/vertibayes
RUN mvn package -Dmaven.test.skip

FROM eclipse-temurin:17.0.7_7-jdk as runner

# This is a placeholder that should be overloaded by invoking
# docker build with '--build-arg PKG_NAME=...'
ARG PKG_NAME="com.florian.vertibayes"
ENV JAR_PATH="/app/vertibayes.jar"
ENV SERVER_PORT=8888

RUN apt update && apt install -y python3 python3-pip python3-dev g++ musl-dev libffi-dev libssl-dev
RUN ln -sf python3 /usr/bin/python
RUN pip3 install --no-cache setuptools wheel poetry

COPY --from=builder /build/vertibayes/target/vertibayes*.jar $JAR_PATH

# install federated algorithm
COPY /src/. /app/src
COPY ./pyproject.toml /app/pyproject.toml

WORKDIR /app
RUN poetry install && poetry cache clear -n --all pypi

ENV PKG_NAME=${PKG_NAME}

# Tell docker to execute `docker_wrapper()` when the image is run.
CMD poetry run python -c "from vantage6.algorithm.tools.wrap import wrap_algorithm; wrap_algorithm()"