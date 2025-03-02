#!/usr/bin/env fontforge

from sys import argv
from math import radians
import fontforge, psMat, re

def selectGlyphsWorthOutputting(font, f = lambda _: True):
	font.selection.none()
	for glyph in font:
		if font[glyph].isWorthOutputting() and f(font[glyph]):
			font.selection.select(("more",), glyph)

blockElements = set(range(0x2500, 0x25a0)) \
	| set(range(0x25e2, 0x25e6)) \
	| set(range(0xe0b0, 0xe0b4)) \
	| set(range(0x1fb00, 0x1fbaf))

# Inconsolataの読み込み、サイズ調整、諸設定
font = fontforge.open(argv[2])
tmpname = font.fontname.replace("InconsolataLGC", "SampuIshiGothic")
font.fontname = tmpname
tmpname = font.fullname.replace("Inconsolata LGC", "Sampu Ishi Gothic")
font.fullname = tmpname
font.familyname = "Sampu Ishi Gothic"
font.em = 1000
font.ascent = 820
font.descent = 180
selectGlyphsWorthOutputting(font, lambda glyph: glyph.unicode not in blockElements)
font.transform(psMat.scale(634/735), ("round",))
font.transform(psMat.translate(-8, 0), ("round",))
selectGlyphsWorthOutputting(font, lambda glyph: glyph.unicode in blockElements)
font.transform(psMat.scale(500/599, 1), ("round",))
font.transform(psMat.translate(0, 60), ("round",))
selectGlyphsWorthOutputting(font)
for glyph in font.selection.byGlyphs:
	glyph.width = 500
font.copyright = """Copyright (c) 2006 Raph Levien
Copyright (c) 2010-2012 Dimosthenis Kaponis
Copyright (c) 2012-2024 MihailJP
Copyright 2014-2019 Adobe (http://www.adobe.com/), with Reserved Font Name 'Source'. Source is a trademark of Adobe in the United States and/or other countries."""
font.version = "2.1.1"
font.sfntRevision = None

# 日本語のフォント名
subFamily = [(x, y, z) for x, y, z in font.sfnt_names if x == "English (US)" and y == "SubFamily"][0][2]
font.appendSFNTName("Japanese", "Family", "算譜石ゴシック")
if subFamily == "Regular":
	font.appendSFNTName("Japanese", "SubFamily", "標準")
	font.appendSFNTName("Japanese", "Fullname", "算譜石ゴシック")
elif subFamily == "Italic":
	font.appendSFNTName("Japanese", "SubFamily", "斜体")
	font.appendSFNTName("Japanese", "Fullname", "算譜石ゴシック 斜体")
elif subFamily == "Bold":
	font.appendSFNTName("Japanese", "SubFamily", "太字")
	font.appendSFNTName("Japanese", "Fullname", "算譜石ゴシック 太字")
elif subFamily == "Bold Italic":
	font.appendSFNTName("Japanese", "SubFamily", "太字斜体")
	font.appendSFNTName("Japanese", "Fullname", "算譜石ゴシック 太字斜体")

# 丸数字と一部の記号を除去
rejected_glyphs = set()
for glyph in font:
	if re.search(r'[^v]+circle($|\.)', glyph):
		rejected_glyphs.add(glyph)
	elif re.search(r'\.smallnarrow', glyph):
		rejected_glyphs.add(glyph)
	elif 0x25a0 <= font[glyph].unicode <= 0x25af:
		rejected_glyphs.add(glyph)
	elif 0x25b2 <= font[glyph].unicode <= 0x25c9:
		rejected_glyphs.add(glyph)
	elif 0x25cb <= font[glyph].unicode <= 0x25cf:
		rejected_glyphs.add(glyph)
	elif 0x2605 <= font[glyph].unicode <= 0x2606:
		rejected_glyphs.add(glyph)
	elif 0x2640 <= font[glyph].unicode <= 0x266f:
		rejected_glyphs.add(glyph)
for glyph in rejected_glyphs:
	font.removeGlyph(glyph)

# 源石ゴシックを読み込み
genseki = fontforge.open(argv[3] + "(" + [x for x in fontforge.fontsInFile(argv[3]) if x.find("JP") != -1 and x.find("PJP") == -1][0] + ")")

# 文字コード修正
def fixUni(font, oldCode, newCode, oldCodeInAltUni):
	font["uni{:0>4X}".format(oldCode)].altuni = (oldCode,) if oldCodeInAltUni else None
	if oldCode != newCode:
		font["uni{:0>4X}".format(oldCode)].unicode = newCode
		font["uni{:0>4X}".format(oldCode)].glyphname = "uni{:0>4X}".format(newCode)
fixUni(genseki, 0x2215, 0xff0f, True)
fixUni(genseki, 0x2027, 0x30fb, True)
fixUni(genseki, 0x52fb, 0x5300, False)
fixUni(genseki, 0x5e21, 0x5e32, False)
fixUni(genseki, 0x5910, 0x5910, False)
fixUni(genseki, 0x7bb3, 0x7c08, False)
#fixUni(genseki, 0x670c, 0x80a6, True)
#fixUni(genseki, 0x6710, 0x80ca, True)
#fixUni(genseki, 0x3b35, 0x80f6, True)
fixUni(genseki, 0x6713, 0x6713, False)
fixUni(genseki, 0x8c5c, 0x8c63, False)
fixUni(genseki, 0x8eff, 0x8f27, False)
fixUni(genseki, 0x9203, 0x9292, False)
genseki.encoding = "UnicodeFull"

# グリフの変更
def searchLookup(font, otTag, scriptCode):
	for lookup in font.gsub_lookups:
		for tag, scripts in font.getLookupInfo(lookup)[2]:
			for scr, _ in scripts:
				if tag == otTag and scr == scriptCode:
					return lookup
	return None
patchFont = fontforge.open(argv[4])
for glyph in patchFont:
	patchFont.selection.select(glyph)
	patchFont.copy()
	if glyph not in genseki:
		genseki.createChar(patchFont[glyph].unicode, patchFont[glyph].glyphname)
		# 拡張濁点・半濁点
		glyphPattern = re.search(r'^(uni30[0-9A-F]{2})_(uni309[9A])\.ccmp$', glyph, re.A)
		if glyphPattern:
			lookup = searchLookup(genseki, 'ccmp', 'kana')
			subtable = genseki.getLookupSubtables(lookup)[0]
			genseki[glyph].addPosSub(subtable, glyphPattern.group(1, 2))
	genseki.selection.select(glyph)
	genseki.paste()
patchFont.close(); patchFont = None

# 源石ゴシックVer2で仮名の幅が正しくなくなっているので直す
for glyph in genseki:
	if genseki[glyph].width == 940 and ((0x3040 <= genseki[glyph].unicode <= 0x30ff) or (0x31f0 <= genseki[glyph].unicode <= 0x31ff)):
		genseki[glyph].transform(psMat.translate(30, 0), ("round",))
		genseki[glyph].width = 1000
genseki.selection.select("uni309B")
genseki.copy()
genseki.selection.select("uni3099")
genseki.paste()

# 縦書き用など不要なグリフの削除
for glyph in genseki:
	if genseki[glyph].width != 1000 and genseki[glyph].width != 500:
		genseki.removeGlyph(glyph)
	elif genseki[glyph].glyphname.find(".fwid") != -1:
		genseki.removeGlyph(glyph)
	elif genseki[glyph].glyphname.find(".hwid") != -1:
		genseki.removeGlyph(glyph)
	elif genseki[glyph].glyphname.find(".vert") != -1:
		genseki.removeGlyph(glyph)
	elif genseki[glyph].glyphname.find(".aalt") != -1:
		genseki.removeGlyph(glyph)
	elif genseki[glyph].glyphname.find("glyph") != -1:
		genseki.removeGlyph(glyph)

# メトリックのコピー
font.upos = genseki.upos
font.uwidth = genseki.uwidth
font.os2_winascent_add = genseki.os2_winascent_add
font.os2_windescent_add = genseki.os2_windescent_add
font.os2_winascent = genseki.os2_winascent
font.os2_windescent = genseki.os2_windescent
font.os2_typoascent_add = genseki.os2_typoascent_add
font.os2_typodescent_add = genseki.os2_typodescent_add
font.os2_typoascent = genseki.os2_typoascent
font.os2_typodescent = genseki.os2_typodescent
font.os2_typolinegap = genseki.os2_typolinegap
font.hhea_ascent_add = genseki.hhea_ascent_add
font.hhea_descent_add = genseki.hhea_descent_add
font.hhea_ascent = genseki.hhea_ascent
font.hhea_descent = genseki.hhea_descent
font.hhea_linegap = genseki.hhea_linegap
font.os2_family_class = genseki.os2_family_class
#font.os2_stylemap = genseki.os2_stylemap
font.os2_panose = genseki.os2_panose
font.os2_version = genseki.os2_version
font.os2_strikeypos = genseki.os2_strikeypos
font.os2_strikeysize = genseki.os2_strikeysize
font.os2_subxoff = genseki.os2_subxoff
font.os2_subxsize = genseki.os2_subxsize
font.os2_subyoff = genseki.os2_subyoff
font.os2_subysize = genseki.os2_subysize
font.os2_supxoff = genseki.os2_supxoff
font.os2_supxsize = genseki.os2_supxsize
font.os2_supyoff = genseki.os2_supyoff
font.os2_supysize = genseki.os2_supysize

# 全角スペース
genseki.selection.select("H22073")
genseki.copy()
genseki.selection.select("uni2003")
genseki.paste()
genseki.selection.select("uni271A")
genseki.copy()
genseki.selection.select("uni2003")
genseki.pasteInto()
genseki.intersect()

# サイズ調整
for w in (500, 1000):
	selectGlyphsWorthOutputting(genseki, lambda glyph: glyph.width == w)
	genseki.transform(psMat.scale(font.ascent / genseki.ascent), ("round", "noWidth"))
	genseki.transform(psMat.translate(w * (1 - font.ascent / genseki.ascent) / 2), ("round", "noWidth"))

# 斜体
if font.italicangle != 0:
	selectGlyphsWorthOutputting(genseki)
	genseki.transform(psMat.skew(radians(-font.italicangle)), ("round",))

# OpenType機能を整理
for lookup in genseki.gpos_lookups:
	genseki.removeLookup(lookup)
for lookup in genseki.gsub_lookups:
	if lookup.find("jp78") == lookup.find("jp83") == lookup.find("jp90") == lookup.find("nlck") == lookup.find("ccmp") == -1:
		genseki.removeLookup(lookup)

# OTFグリフクラス（ワークアラウンド）
for glyph in genseki:
	if genseki[glyph].isWorthOutputting():
		genseki[glyph].glyphclass = "baseglyph"

# サイズ調整（Ricty Diminishedと同様）
selectGlyphsWorthOutputting(genseki)
genseki.transform(psMat.compose(psMat.scale(0.95), psMat.translate(10, 0)), ('noWidth', 'round'))

# 統合
font.mergeFonts(genseki)
font.encoding = "UnicodeFull"

# 出力
font.generate(argv[1])
