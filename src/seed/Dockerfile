# ビルドステージ
FROM ghcr.io/astral-sh/uv:python3.10-bookworm as builder

RUN apt-get update && apt-get install -y git

WORKDIR /build

# LINEのSeedフォントリポジトリをクローン
ARG GIT_TAG=v20241007
RUN git clone --depth=1 https://github.com/line/seed . && \
    if [ -n "$GIT_TAG" ]; then \
        git fetch --depth=1 origin $GIT_TAG && \
        git checkout $GIT_TAG; \
    fi

# venvを作成し依存関係をインストール
RUN make venv

# 実行ステージ
FROM ghcr.io/astral-sh/uv:python3.10-bookworm

# ttfautohintは実行時のみ必要
RUN apt-get update && apt-get install -y ttfautohint

# ビルド済みのリポジトリとvenvをコピー
COPY --from=builder /build /build

WORKDIR /build

VOLUME /build/out

# ビルドとTTFファイルのコピー
CMD make build && cp -r LINESeedJP/fonts/ttf/* /build/out/
