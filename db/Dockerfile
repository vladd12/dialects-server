# Pull official alpine based image
FROM postgres:13-alpine

# Set Russian locale in alpine based image
RUN rm glibc-2.35-r0.apk && rm glibc-bin-2.35-r0.apk && rm glibc-i18n-2.35-r0.apk && \
    wget -q -O /etc/apk/keys/sgerrand.rsa.pub https://alpine-pkgs.sgerrand.com/sgerrand.rsa.pub && \
    wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.35-r0/glibc-2.35-r0.apk && \
    wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.35-r0/glibc-bin-2.35-r0.apk && \
    wget https://github.com/sgerrand/alpine-pkg-glibc/releases/download/2.35-r0/glibc-i18n-2.35-r0.apk && \
    apk --no-cache add glibc-2.35-r0.apk glibc-bin-2.35-r0.apk glibc-i18n-2.35-r0.apk && \
    /usr/glibc-compat/bin/localedef -i ru_RU -f UTF-8 ru_RU.UTF-8

ENV LANG ru_RU.utf8
