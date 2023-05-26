FROM alpine:3.14

ENV VAULT_VERSION 1.8.2

RUN apk --no-cache add \
      bash \
      ca-certificates \
      wget \
      curl

RUN wget --quiet --output-document=/tmp/vault.zip https://releases.hashicorp.com/vault/${VAULT_VERSION}/vault_${VAULT_VERSION}_linux_amd64.zip && \
    unzip /tmp/vault.zip -d /vault && \
    rm -f /tmp/vault.zip && \
    chmod +x /vault

ENV PATH="PATH=$PATH:$PWD/vault"
ENV VAULT_ADDR="http://nextgenbts_vault:8200"
ENV VAULT_TOKEN="myroot"

WORKDIR /config

COPY ./config.sh /config/config.sh

ENTRYPOINT ["/config/config.sh"]