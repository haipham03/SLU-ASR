FROM nvidia/cuda:11.7.1-devel-ubuntu20.04

WORKDIR /SLU

# install dependencies
RUN --mount=type=cache,target=/root/.cache \
    apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
    ca-certificates \
    libjpeg-dev \
    libpng-dev \
    libboost-all-dev \
    zlib1g-dev \
    libbz2-dev \
    liblzma-dev \
    libgl1 \
    ccache \
    cmake \
    curl \
    default-jdk \
    wget \
    gcc \
    build-essential \
    software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa -y

RUN --mount=type=cache,target=/root/.cache \
    apt-get update -y \
    && apt-get install -y python3.9 python3.9-dev \
    && update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1 

RUN --mount=type=cache,target=/root/.cache \
    apt-get update -y \
    && apt-get install -y python3-pip \
    && pip3 install --upgrade pip \
    && pip3 install pyem empy pyyaml

COPY . /SLU

# install requirements
RUN --mount=type=cache,target=/root/.cache \
    pip install -r requirements.txt 

ARG INSTALL_TORCH="pip install torch==1.7.1+cu110 torchvision==0.8.2+cu110 torchaudio==0.7.2 -f https://download.pytorch.org/whl/torch_stable.html"

RUN --mount=type=cache,target=/root/.cache \
    bash -c "${INSTALL_TORCH}"

RUN --mount=type=cache,target=/root/.cache \
    pip3 install protobuf==3.20.* \
    && pip3 install https://github.com/kpu/kenlm/archive/master.zip

RUN --mount=type=cache,target=/root/.cache \
    pip3 install gdown && \
    cd /SLU && \
    gdown --folder 1CK__VZzxKA9ZZFbl0frFYyL3dFxEm83_ && \
    gdown --folder 1HVt09CDAyoSaEdzC7J38VH_ksE4SgO_J

