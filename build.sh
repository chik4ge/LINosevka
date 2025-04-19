#!/usr/bin/bash
REPO_DIR=$(dirname "$0")
BUILD_DIR=$REPO_DIR/build
CACHE_DIR=$REPO_DIR/cache

BUILD_CONCURRENCY=4

IOSEVKA_VERSION="v33.1.0"
LINE_SEED_VERSION="v20241007"

# setup build environment
if [ ! -d $BUILD_DIR ]; then
    mkdir -p $BUILD_DIR
fi
if [ ! -d $CACHE_DIR ]; then
    mkdir -p $CACHE_DIR
fi

# build Iosevka
# (https://github.com/be5invis/Iosevka/tree/main/docker#readme)
if ! docker image inspect fontcc:$IOSEVKA_VERSION >/dev/null 2>&1; then
    git clone --depth=1 --branch $IOSEVKA_VERSION https://github.com/be5invis/Iosevka.git $BUILD_DIR/Iosevka
    cd $BUILD_DIR/Iosevka/docker

    docker build -t=fontcc:$IOSEVKA_VERSION .

    cd $BUILD_DIR
    rm -rf $BUILD_DIR/Iosevka
else
    echo "Docker image fontcc:$IOSEVKA_VERSION already exists. Skipping clone and build."
fi

IOSEVKA_BUILD_DIR=$BUILD_DIR/IosevkaCustom
if [ ! -d $IOSEVKA_BUILD_DIR ]; then
    mkdir -p $IOSEVKA_BUILD_DIR
fi
cp $REPO_DIR/private-build-plans.toml $IOSEVKA_BUILD_DIR
# docker run -it --rm -v $IOSEVKA_BUILD_DIR:/work -e "VERSION_TAG=$IOSEVKA_VERSION" fontcc:$IOSEVKA_VERSION --jCmd=$BUILD_CONCURRENCY ttf::LInosevkaBase

IOSEVKA_DIR=$IOSEVKA_BUILD_DIR/dist/LInosevkaBase/TTF

# merge Iosevka & Nerd fonts
IOSEVKA_NERD_DIR=$BUILD_DIR/IosevkaCustomNerdFonts
if [ ! -d $IOSEVKA_NERD_DIR ]; then
    mkdir -p $IOSEVKA_NERD_DIR
fi
# docker run --rm -v $IOSEVKA_DIR:/in:Z -v $IOSEVKA_NERD_DIR:/out:Z nerdfonts/patcher -c -s --makegroups 4

# build LINE Seed
LINE_SEED_BUILDER_CONTEXT_DIR=$REPO_DIR/src/seed
docker build -t line-seed-builder -f $LINE_SEED_BUILDER_CONTEXT_DIR/Dockerfile $LINE_SEED_BUILDER_CONTEXT_DIR

LINE_SEED_DIR=$BUILD_DIR/LINESeedJP
# docker run --rm -v $LINE_SEED_DIR:/work -e GIT_TAG=$LINE_SEED_VERSION line-seed-builder

# run merge script
docker build -t linosevka-builder .
docker run --rm -it -v ./src/builder:/work -v ./build/IosevkaCustomNerdFonts:/fonts/iosevka -v ./build/LINESeedJP/ttf:/fonts/seed -v ./out:/fonts/out linosevka-builder
