#!/usr/bin/env fontforge

from sys import argv
from math import radians
import fontforge, psMat, re

font = fontforge.open(argv[2])
tmpname = font.fontname.replace("InconsolataLGC", "SampuIshiGothic")
font.fontname = tmpname
tmpname = font.fullname.replace("Inconsolata LGC", "Sampu Ishi Gothic")
font.fullname = tmpname
font.familyname = "Sampu Ishi Gothic"
font.em = 1000
font.ascent = 860
font.descent = 140
font.selection.none()
for glyph in font:
	if font[glyph].isWorthOutputting():
		font.selection.select(("more",), glyph)
font.transform(psMat.scale(634/735), ("round",))
font.transform(psMat.translate(-8, 0), ("round",))
for glyph in font.selection.byGlyphs:
	glyph.width = 500
font.copyright = """
Copyright (c) 2006 Raph Levien
Copyright (c) 2010-2012 Dimosthenis Kaponis
Copyright (c) 2012-2024 MihailJP
Copyright 2014-2019 Adobe (http://www.adobe.com/), with Reserved Font Name 'Source'. Source is a trademark of Adobe in the United States and/or other countries."""
font.version = "0.1"
font.sfntRevision = None

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

genseki = fontforge.open(argv[3] + "(" + [x for x in fontforge.fontsInFile(argv[3]) if x.find("JP") != -1][0] + ")")

for glyph in genseki:
	if genseki[glyph].glyphname.find(".fwid") != -1:
		genseki.selection.select(glyph)
		genseki.copy()
		genseki.selection.select(genseki[glyph].glyphname.replace(".fwid", ""))
		genseki.paste()

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

genseki.selection.select("H22073")
genseki.copy()
genseki.selection.select("uni2003")
genseki.paste()
genseki.selection.select("uni271A")
genseki.copy()
genseki.selection.select("uni2003")
genseki.pasteInto()
genseki.intersect()

if font.italicangle != 0:
	genseki.selection.none()
	for glyph in genseki:
		if genseki[glyph].isWorthOutputting():
			genseki.selection.select(("more",), glyph)
	genseki.transform(psMat.skew(radians(-font.italicangle)), ("round",))

for lookup in genseki.gpos_lookups:
	genseki.removeLookup(lookup)
for lookup in genseki.gsub_lookups:
	if lookup.find("jp78") == lookup.find("jp83") == lookup.find("jp90") == lookup.find("nlck") == -1:
		genseki.removeLookup(lookup)

font.mergeFonts(genseki)
font.encoding = "UnicodeFull"

font.generate(argv[1])
