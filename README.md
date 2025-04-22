# merged fonts

|  Iosevka   | LINE Seed |
| :--------: | :-------: |
| ExtraLight |   Thin    |
|  Regular   |  Regular  |
| ExtraBold  |   Bold    |

# Build

## requirements:

- git
- docker

> [!CAUTION]
> ビルド用に使用できるメモリが 12GB 程度必要です

```bash
docker compose up
```

# Debug
fontforge を起動します
```bash
docker compose --profile debug up
```
