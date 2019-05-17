FROM ubuntu:18.04

ENV DEBIAN_FRONTEND noninteractive
ENV DEBCONF_NONINTERACTIVE_SEEN true
ENV MAIN_PATH=/usr/local/bin/census_data
ENV LIBS_PATH=${MAIN_PATH}/libs
ENV CONFIG_PATH=${MAIN_PATH}/config
ENV NOTEBOOK_PATH=${MAIN_PATH}/notebooks

COPY ./.dotfiles /root/.dotfiles/

RUN apt-get update
RUN apt-get -y upgrade
RUN apt-get install -y build-essential  \
    checkinstall \
    sudo \
    curl \ 
    git-core \
    libreadline-gplv2-dev \
    libncursesw5-dev \
    libssl-dev \
    libsqlite3-dev \
    tk-dev \
    libgdbm-dev \
    libc6-dev \
    libbz2-dev \
    zlib1g-dev \
    openssl \
    libffi-dev \
    python3 \
    python3-dev \
    python3-setuptools \
    python3-pip \
    wget \
    zsh \
    vim \
    fonts-powerline \
    pandoc \
    texlive-xetex

RUN pip3 install --upgrade pip \
    requests \
    jupyter \
    jupyterlab \
    pycrypto \
    pandas

RUN apt-get install -y bash nodejs npm \
    && pip3 install bash_kernel \
    && python3 -m bash_kernel.install

# run the installation script  
RUN wget https://github.com/robbyrussell/oh-my-zsh/raw/master/tools/install.sh -O - | zsh || true

RUN cd ~/.dotfiles \
    && make install

EXPOSE 8888

CMD cd ${MAIN_PATH} && [ "zsh" ]
