import dataclasses
import math
import os

import fontforge
import psMat

FAMILY_NAME = "LINosevkaNF"
VERSION = "1.0.1"


def JP_FONT_PATH(weight: str):
    return f"/fonts/seed/LINESeedJP-{weight}.ttf"


def EN_FONT_PATH(style: str):
    return f"/fonts/iosevka/IosevkaNerdFont-{style}.ttf"


def OUTPUT_FONT_PATH(style: str):
    return f"/fonts/out/{FAMILY_NAME}-{style}.ttf"


@dataclasses.dataclass
class Style:
    name: str
    jp_weight: str
    en_weight: str
    is_oblique: bool


OUTPUT_STYLE = [
    Style("Thin", "Thin", "ExtraLight", False),
    Style("ThinOblique", "Thin", "ExtraLightOblique", True),
    Style("Regular", "Regular", "Regular", False),
    Style("RegularOblique", "Regular", "Oblique", True),
    Style("Bold", "Bold", "ExtraBold", False),
    Style("BoldOblique", "Bold", "ExtraBoldOblique", True),
]

OBLIQUE_ANGLE = 9.4

COPYRIGHT = """
[LINE Seed]
(c) LY Corporation https://github.com/line/seed

[Iosevka]
Copyright 2015-2025, Renzhi Li (aka. Belleve Invis, belleve@typeof.net). https://github.com/be5invis/Iosevka

[Nerd Fonts]
Copyright (c) 2014, Ryan L McIntyre https://github.com/ryanoasis/nerd-fonts

[LINosevka NF]
Copyright 2025 chik4ge
"""

# Iosevkaフォントのメトリクス
IOSEVKA_METRICS = {
    "ascent": 800,
    "descent": 200,
    "em_size": 1000,
    "underline_position": -75,
    "underline_height": 50
}

# LINE Seed JPフォントのメトリクス
LINESEED_METRICS = {
    "ascent": 880,
    "descent": 120,
    "em_size": 1000,
    "underline_position": -224,
    "underline_height": 76
}

# 横幅比の設定 (英語:日本語 = 3:5)
WIDTH_RATIO = 3/5  # 元の設定に戻す

def build():
    """すべてのフォントスタイルをビルドする"""
    os.makedirs(os.path.dirname(OUTPUT_FONT_PATH("Regular")), exist_ok=True)
    
    for style in OUTPUT_STYLE:
        print(f"Building {style.name}...")
        merge_fonts(style)
        print(f"✓ {style.name} done")


def merge_fonts(style: Style):
    """
    IosevkaとLINE Seed JPフォントを合成する
    
    Args:
        style: 出力するフォントスタイル情報
    """
    # 英語フォントをベースにする
    en_font = fontforge.open(EN_FONT_PATH(style.en_weight))
    jp_font = fontforge.open(JP_FONT_PATH(style.jp_weight))
    
    # フォント情報を設定
    en_font.familyname = FAMILY_NAME
    en_font.fontname = f"{FAMILY_NAME}-{style.name}"
    en_font.fullname = f"{FAMILY_NAME} {style.name}"
    en_font.version = VERSION
    en_font.copyright = COPYRIGHT
    
    # Iosevkaのメトリクスを採用
    en_font.ascent = IOSEVKA_METRICS["ascent"]
    en_font.descent = IOSEVKA_METRICS["descent"]
    en_font.upos = IOSEVKA_METRICS["underline_position"]
    en_font.uwidth = IOSEVKA_METRICS["underline_height"]
    
    # LINE Seed JPのグリフをスケーリングしてIosevkaに合わせる
    # アセント比率に基づくスケーリング係数
    scale_factor = IOSEVKA_METRICS["ascent"] / LINESEED_METRICS["ascent"]
    
    # 日本語グリフを追加
    for glyph in jp_font.glyphs():
        unicode_value = glyph.unicode
        
        # グリフがベースフォントに存在しない場合のみ追加
        if unicode_value != -1 and unicode_value not in en_font:
            # グリフをコピー
            jp_font.selection.select(unicode_value)
            jp_font.copy()
            en_font.selection.select(unicode_value)
            en_font.paste()
            
            # グリフのメトリクス調整
            if unicode_value in en_font:
                # スケーリングと位置調整
                en_glyph = en_font[unicode_value]
                
                # 変換行列を作成（高さ方向のみスケール）
                matrix = psMat.scale(1.0, scale_factor)
                
                # 斜体の場合は傾斜を適用
                if style.is_oblique:
                    slant_matrix = psMat.skew(math.radians(OBLIQUE_ANGLE))
                    matrix = psMat.compose(matrix, slant_matrix)
                
                # 変換を適用
                en_glyph.transform(matrix)
                
                # ベースラインに合わせて配置調整
                baseline_adjust = (IOSEVKA_METRICS["descent"] - LINESEED_METRICS["descent"] * scale_factor)
                en_glyph.transform(psMat.translate(0, baseline_adjust))
    
    # フォントの生成
    output_path = OUTPUT_FONT_PATH(style.name)
    # SFDファイルも保存（デバッグ用）
    sfd_path = output_path.replace(".ttf", ".sfd")
    en_font.generate(output_path)
    en_font.save(sfd_path)
    en_font.close()
    jp_font.close()


if __name__ == "__main__":
    build()
