#!/bin/bash
set -e

# リポジトリ URL は固定
REPO_URL="https://github.com/line/seed"

# 一時ディレクトリを作成してクローン
TMP_DIR=$(mktemp -d)
echo "==> Cloning repository from ${REPO_URL} into ${TMP_DIR}"
git clone "${REPO_URL}" "${TMP_DIR}" --depth=1

# GIT_TAG 環境変数が指定されている場合はチェックアウト
if [ -n "$GIT_TAG" ]; then
    echo "==> Checking out tag: $GIT_TAG"
    cd "${TMP_DIR}"
    git fetch --all
    git checkout "$GIT_TAG"
    cd -
fi

# 一時ディレクトリに移動してビルド実行
cd "${TMP_DIR}"
uv init

# もし requirements.txt があれば依存パッケージをインストール
if [ -f requirements.txt ]; then
    echo "==> Installing Python dependencies"
    uv add -r requirements.txt
fi

echo "==> Running: make build"
make build
echo "==> Build completed."

echo "==> Copying artifacts to /work"
if [ -d "LINESeedJP/fonts" ]; then
    cp -r LINESeedJP/fonts/ttf /work/
fi

echo "==> Artifacts have been copied to /work"

rm -rf "${TMP_DIR}"
