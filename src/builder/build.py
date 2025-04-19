import dataclasses
import math

import fontforge
import psMat

FAMILY_NAME = "LINosevkaNF"
VERSION = "1.0.0"


def JP_FONT_PATH(weight: str):
    return f"/fonts/seed/LINESeedJP-{weight}.ttf"


def EN_FONT_PATH(style: str):
    return f"/fonts/iosevka/LInosevkaBaseNerdFontMono-{style}.ttf"


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


EM_ASCENT = 880
EM_DESCENT = 120
OS2_ASCENT = 950
OS2_DESCENT = 250

HALF_WIDTH = 600
FULL_WIDTH = 1000

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


def build(style: Style):
    print(f"Building {style.name}...")
    jp_font, en_font = open_fonts(style)

    # Set font em to 1000
    jp_font.em = EM_ASCENT + EM_DESCENT
    en_font.em = EM_ASCENT + EM_DESCENT

    # remove jp glyphs that are in en font
    distinct_glyphs(jp_font, en_font)

    # oblique jp font
    if style.is_oblique:
        for glyph in jp_font.glyphs():
            glyph.transform(psMat.skew(-OBLIQUE_ANGLE * math.pi / 180))

    # merge jp and en font
    font = new_font(style)

    font.mergeFonts(jp_font)
    font.mergeFonts(en_font)

    font.generate(OUTPUT_FONT_PATH(style.name))

    jp_font.close()
    en_font.close()


def open_fonts(style: Style):
    jp_path = JP_FONT_PATH(style.jp_weight)
    en_path = EN_FONT_PATH(style.en_weight)

    jp_font = fontforge.open(jp_path)
    en_font = fontforge.open(en_path)

    for glyph in jp_font.glyphs():
        if glyph.isWorthOutputting():
            jp_font.selection.select(("more", None), glyph)
    jp_font.unlinkReferences()

    for glyph in en_font.glyphs():
        if glyph.isWorthOutputting():
            en_font.selection.select(("more", None), glyph)
    en_font.unlinkReferences()

    return jp_font, en_font


def new_font(style: Style):
    font = fontforge.font()

    font.fontname = f"{FAMILY_NAME}-{style.name}"
    font.fullname = f"{FAMILY_NAME} {style.name}"
    font.familyname = FAMILY_NAME
    font.copyright = COPYRIGHT
    font.version = VERSION

    font.weight = style.name

    font.ascent = EM_ASCENT
    font.descent = EM_DESCENT

    font.italicangle = -OBLIQUE_ANGLE if style.is_oblique else 0

    # font.upos = P.UNDERLINE_POS
    # font.uwidth = P.UNDERLINE_HEIGHT

    return font


def distinct_glyphs(jp_font, en_font):
    jp_font.selection.none()
    en_font.selection.none()

    for glyph in jp_font.glyphs("encoding"):
        try:
            if glyph.isWorthOutputting() and glyph.unicode > 0:
                en_font.selection.select(("more", "unicode"), glyph.unicode)
        except ValueError:
            # Encoding is out of range のときは継続する
            continue
    for glyph in en_font.selection.byGlyphs:
        jp_font.selection.select(("more", "unicode"), glyph.unicode)
    for glyph in jp_font.selection.byGlyphs:
        glyph.clear()

    jp_font.selection.none()
    en_font.selection.none()


if __name__ == "__main__":
    for style in OUTPUT_STYLE:
        build(style)
