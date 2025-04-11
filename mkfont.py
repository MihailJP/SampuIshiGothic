#!/usr/bin/env fontforge

from sys import argv
from math import radians
import fontforge, psMat, re

def selectGlyphsWorthOutputting(font, f = lambda _: True):
	font.selection.none()
	for glyph in font:
		if font[glyph].isWorthOutputting() and f(font[glyph]):
			font.selection.select(("more",), glyph)

blockElements = {0x2429} \
	| set(range(0x2500, 0x25a0)) \
	| set(range(0x25e2, 0x25e6)) \
	| set(range(0xe0b0, 0xe0b4)) \
	| set(range(0x1cd00, 0x1ceb0)) \
	| set(range(0x1cc21, 0x1cc30)) \
	| set(range(0x1fb00, 0x1fbf0))

hiraganaToHentaigana = {
	# あ
	'uni3042': ('u1B002', 'u1B003', 'u1B004', 'u1B005',),
	'uni3044': ('u1B006', 'u1B007', 'u1B008', 'u1B009',),
	'uni3046': ('u1B00A', 'u1B00B', 'u1B00C', 'u1B00D', 'u1B00E',),
	'uni3048': ('u1B001', 'u1B00F', 'u1B010', 'u1B011', 'u1B012', 'u1B013',),
	'uni304A': ('u1B014', 'u1B015', 'u1B016',),

	# か
	'uni304B': ('u1B017', 'u1B018', 'u1B019', 'u1B01A', 'u1B01B', 'u1B01C', 'u1B01D', 'u1B01E', 'u1B01F', 'u1B020', 'u1B021', 'u1B022',),
	'uni304D': ('u1B023', 'u1B024', 'u1B025', 'u1B026', 'u1B027', 'u1B028', 'u1B029', 'u1B02A', 'u1B03B',),
	'uni304F': ('u1B02B', 'u1B02C', 'u1B02D', 'u1B02E', 'u1B02F', 'u1B030', 'u1B031',),
	'uni3051': ('u1B032', 'u1B033', 'u1B034', 'u1B035', 'u1B036', 'u1B037', 'u1B022',),
	'uni3053': ('u1B038', 'u1B039', 'u1B03A', 'u1B03B', 'u1B098',),

	# さ
	'uni3055': ('u1B03C', 'u1B03D', 'u1B03E', 'u1B03F', 'u1B040', 'u1B041', 'u1B042', 'u1B043',),
	'uni3057': ('u1B044', 'u1B045', 'u1B046', 'u1B047', 'u1B048', 'u1B049',),
	'uni3059': ('u1B04A', 'u1B04B', 'u1B04C', 'u1B04D', 'u1B04E', 'u1B04F', 'u1B050', 'u1B051',),
	'uni305B': ('u1B052', 'u1B053', 'u1B054', 'u1B055', 'u1B056',),
	'uni305D': ('u1B057', 'u1B058', 'u1B059', 'u1B05A', 'u1B05B', 'u1B05C', 'u1B05D',),

	# た
	'uni305F': ('u1B05E', 'u1B05F', 'u1B060', 'u1B061',),
	'uni3061': ('u1B062', 'u1B063', 'u1B064', 'u1B065', 'u1B066', 'u1B067', 'u1B068', ),
	'uni3064': ('u1B069', 'u1B06A', 'u1B06B', 'u1B06C', 'u1B06D',),
	'uni3066': ('u1B06E', 'u1B06F', 'u1B070', 'u1B071', 'u1B072', 'u1B073', 'u1B074', 'u1B075', 'u1B076', 'u1B08E',),
	'uni3068': ('u1B077', 'u1B078', 'u1B079', 'u1B07A', 'u1B07B', 'u1B07C', 'u1B07D', 'u1B06D',),

	# な
	'uni306A': ('u1B07E', 'u1B07F', 'u1B080', 'u1B081', 'u1B082', 'u1B083', 'u1B084', 'u1B085', 'u1B086',),
	'uni306B': ('u1B087', 'u1B088', 'u1B089', 'u1B08A', 'u1B08B', 'u1B08C', 'u1B08D', 'u1B08E',),
	'uni306C': ('u1B08F', 'u1B090', 'u1B091',),
	'uni306D': ('u1B092', 'u1B093', 'u1B094', 'u1B095', 'u1B096', 'u1B097', 'u1B098',),
	'uni306E': ('u1B099', 'u1B09A', 'u1B09B', 'u1B09C', 'u1B09D',),

	# は
	'uni306F': ('u1B09E', 'u1B09F', 'u1B0A0', 'u1B0A1', 'u1B0A2', 'u1B0A3', 'u1B0A4', 'u1B0A5', 'u1B0A6', 'u1B0A7', 'u1B0A8',),
	'uni3072': ('u1B0A9', 'u1B0AA', 'u1B0AB', 'u1B0AC', 'u1B0AD', 'u1B0AE', 'u1B0AF',),
	'uni3075': ('u1B0B0', 'u1B0B1', 'u1B0B2',),
	'uni3078': ('u1B0B3', 'u1B0B4', 'u1B0B5', 'u1B0B6', 'u1B0B7', 'u1B0B8', 'u1B0B9',),
	'uni307B': ('u1B0BA', 'u1B0BB', 'u1B0BC', 'u1B0BD', 'u1B0BE', 'u1B0BF', 'u1B0C0', 'u1B0C1',),

	# ま
	'uni307E': ('u1B0C2', 'u1B0C3', 'u1B0C4', 'u1B0C5', 'u1B0C6', 'u1B0C7', 'u1B0C8', 'u1B0D6',),
	'uni307F': ('u1B0C9', 'u1B0CA', 'u1B0CB', 'u1B0CC', 'u1B0CD', 'u1B0CE', 'u1B0CF',),
	'uni3080': ('u1B0D0', 'u1B0D1', 'u1B0D2', 'u1B0D3', 'u1B11D', 'u1B11E',),
	'uni3081': ('u1B0D4', 'u1B0D5', 'u1B0D6',),
	'uni3082': ('u1B0D7', 'u1B0D8', 'u1B0D9', 'u1B0DA', 'u1B0DB', 'u1B0DC', 'u1B11D', 'u1B11E',),

	# や
	'uni3084': ('u1B0DD', 'u1B0DE', 'u1B0DF', 'u1B0E0', 'u1B0E1', 'u1B0E2',),
	'uni3086': ('u1B0E3', 'u1B0E4', 'u1B0E5', 'u1B0E6',),
	'uni3088': ('u1B0E7', 'u1B0E8', 'u1B0E9', 'u1B0EA', 'u1B0EB', 'u1B0EC', 'u1B0E2',),

	# ら
	'uni3089': ('u1B0ED', 'u1B0EE', 'u1B0EF', 'u1B0F0', 'u1B07D',),
	'uni308A': ('u1B0F1', 'u1B0F2', 'u1B0F3', 'u1B0F4', 'u1B0F5', 'u1B0F6', 'u1B0F7',),
	'uni308B': ('u1B0F8', 'u1B0F9', 'u1B0FA', 'u1B0FB', 'u1B0FC', 'u1B0FD',),
	'uni308C': ('u1B0FE', 'u1B0FF', 'u1B100', 'u1B101',),
	'uni308D': ('u1B102', 'u1B103', 'u1B104', 'u1B105', 'u1B106', 'u1B107',),

	# わ
	'uni308F': ('u1B108', 'u1B109', 'u1B10A', 'u1B10B', 'u1B10C',),
	'uni3090': ('u1B10D', 'u1B10E', 'u1B10F', 'u1B110', 'u1B111',),
	'uni3091': ('u1B112', 'u1B113', 'u1B114', 'u1B115',),
	'uni3092': ('u1B116', 'u1B117', 'u1B118', 'u1B119', 'u1B11A', 'u1B11B', 'u1B11C', 'u1B005',),

	# ん
	'uni3093': ('u1B11D', 'u1B11E',),
}

iwaFont = bool(re.search("SampuIwaGothic", argv[1]))

def isToBeConvertedToFullwidth(font, glyph):
	if 0x0391 <= font[glyph].unicode <= 0x03a9: # ギリシャ大文字
		return True
	elif 0x03b1 <= font[glyph].unicode <= 0x03c9: # ギリシャ小文字
		return True
	elif font[glyph].unicode == 0x0401: # 大文字Ё
		return True
	elif 0x0410 <= font[glyph].unicode <= 0x044f: # キリル文字（ロシア語）
		return True
	elif font[glyph].unicode == 0x0451: # 小文字ё
		return True
	elif 0x00a2 <= font[glyph].unicode <= 0x00a3:
		return True
	elif 0x00a7 <= font[glyph].unicode <= 0x00a8:
		return True
	elif font[glyph].unicode == 0x00ac:
		return True
	elif font[glyph].unicode == 0x00b1:
		return True
	elif font[glyph].unicode == 0x00b4:
		return True
	elif font[glyph].unicode == 0x00b6:
		return True
	elif font[glyph].unicode == 0x00d7:
		return True
	elif font[glyph].unicode == 0x00f7:
		return True
	elif font[glyph].unicode == 0x2010:
		return True
	elif 0x2014 <= font[glyph].unicode <= 0x2016:
		return True
	elif 0x2020 <= font[glyph].unicode <= 0x2021:
		return True
	elif 0x2025 <= font[glyph].unicode <= 0x2026:
		return True
	elif font[glyph].unicode == 0x2030:
		return True
	elif font[glyph].unicode == 0x2103:
		return True
	elif font[glyph].unicode == 0x212b:
		return True
	elif 0x2160 <= font[glyph].unicode <= 0x216b:
		return True
	elif 0x2170 <= font[glyph].unicode <= 0x217b:
		return True
	elif 0x2190 <= font[glyph].unicode <= 0x2193:
		return True
	elif 0x21d2 <= font[glyph].unicode <= 0x21d4:
		return True
	elif 0x2200 <= font[glyph].unicode <= 0x2208:
		return True
	elif font[glyph].unicode == 0x220b:
		return True
	elif 0x220f <= font[glyph].unicode <= 0x2212:
		return True
	elif 0x221a <= font[glyph].unicode <= 0x2237:
		return True
	elif 0x223d <= font[glyph].unicode <= 0x22a0:
		return True
	elif font[glyph].unicode == 0x22a5:
		return True
	elif 0x2312 <= font[glyph].unicode <= 0x2318:
		return True
	elif font[glyph].unicode == 0x23ce:
		return True
	elif font[glyph].unicode == 0x2423:
		return True
	else:
		return False
def isToBeConvertedToFullwidthLeft(font, glyph):
	if font[glyph].unicode == 0x00b0:
		return True
	elif font[glyph].unicode == 0x2019:
		return True
	elif font[glyph].unicode == 0x201d:
		return True
	elif 0x2032 <= font[glyph].unicode <= 0x2033:
		return True
	else:
		return False
def isToBeConvertedToFullwidthRight(font, glyph):
	if font[glyph].unicode == 0x2018:
		return True
	elif font[glyph].unicode == 0x201c:
		return True
	else:
		return False

# Inconsolataの読み込み、サイズ調整、諸設定
font = fontforge.open(argv[2])
tmpname = font.fontname.replace("InconsolataLGC", "SampuIwaGothic" if iwaFont else "SampuIshiGothic")
font.fontname = tmpname
tmpname = font.fullname.replace("Inconsolata LGC", "Sampu Iwa Gothic" if iwaFont else "Sampu Ishi Gothic")
font.fullname = tmpname
font.familyname = "Sampu Iwa Gothic" if iwaFont else "Sampu Ishi Gothic"
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
Copyright 2014-2021 Adobe (http://www.adobe.com/), with Reserved Font Name 'Source'. Source is a trademark of Adobe in the United States and/or other countries."""
font.version = "2.3"
font.sfntRevision = None

# 日本語のフォント名
subFamily = [(x, y, z) for x, y, z in font.sfnt_names if x == "English (US)" and y == "SubFamily"][0][2]
font.appendSFNTName("Japanese", "Family", "算譜岩ゴシック" if iwaFont else "算譜石ゴシック")
if subFamily == "Regular":
	font.appendSFNTName("Japanese", "SubFamily", "標準")
	font.appendSFNTName("Japanese", "Fullname", "算譜岩ゴシック" if iwaFont else "算譜石ゴシック")
elif subFamily == "Italic":
	font.appendSFNTName("Japanese", "SubFamily", "斜体")
	font.appendSFNTName("Japanese", "Fullname", "算譜岩ゴシック 斜体" if iwaFont else "算譜石ゴシック 斜体")
elif subFamily == "Bold":
	font.appendSFNTName("Japanese", "SubFamily", "太字")
	font.appendSFNTName("Japanese", "Fullname", "算譜岩ゴシック 太字" if iwaFont else "算譜石ゴシック 太字")
elif subFamily == "Bold Italic":
	font.appendSFNTName("Japanese", "SubFamily", "太字斜体")
	font.appendSFNTName("Japanese", "Fullname", "算譜岩ゴシック 太字斜体" if iwaFont else "算譜石ゴシック 太字斜体")

# 丸数字と一部の記号を除去
rejected_glyphs = set()
for glyph in font:
	if re.search(r'[^v]+circle($|\.)', glyph):
		rejected_glyphs.add(glyph)
	elif re.search(r'\.smallnarrow', glyph):
		rejected_glyphs.add(glyph)
	elif iwaFont:
		if isToBeConvertedToFullwidth(font, glyph):
			rejected_glyphs.add(glyph)
		elif isToBeConvertedToFullwidthLeft(font, glyph):
			rejected_glyphs.add(glyph)
		elif isToBeConvertedToFullwidthRight(font, glyph):
			rejected_glyphs.add(glyph)
		elif 0x2500 <= font[glyph].unicode <= 0x257f: # 罫線素片
			rejected_glyphs.add(glyph)
		elif 0x25a0 <= font[glyph].unicode <= 0x25ab: # 幾何学模様
			rejected_glyphs.add(glyph)
		elif 0x25b2 <= font[glyph].unicode <= 0x25b9: # 幾何学模様
			rejected_glyphs.add(glyph)
		elif 0x25bb <= font[glyph].unicode <= 0x25c3: # 幾何学模様
			rejected_glyphs.add(glyph)
		elif 0x25c5 <= font[glyph].unicode <= 0x25c9: # 幾何学模様
			rejected_glyphs.add(glyph)
		elif 0x25cb <= font[glyph].unicode <= 0x25cf: # 幾何学模様
			rejected_glyphs.add(glyph)
		elif 0x2605 <= font[glyph].unicode <= 0x2606: # 星印
			rejected_glyphs.add(glyph)
		elif 0x2640 <= font[glyph].unicode <= 0x2642: # 雌雄記号
			rejected_glyphs.add(glyph)
		elif 0x2660 <= font[glyph].unicode <= 0x266f: # トランプのスート
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
fixUni(genseki, 0x02bb, 0x2018, False)
genseki.encoding = "UnicodeFull"

# Lookupを検索
def searchLookup(font, otTag, scriptCode):
	for lookup in font.gsub_lookups:
		for tag, scripts in font.getLookupInfo(lookup)[2]:
			for scr, _ in scripts:
				if tag == otTag and scr == scriptCode:
					return lookup
	return None

# Lookupの追加
lookupForDakuten = searchLookup(genseki, 'ccmp', 'kana')
subtableForDakuten = genseki.getLookupSubtables(lookupForDakuten)[0]
genseki.addLookupSubtable(lookupForDakuten, "Hentaigana with dakuten")
genseki.addLookup("Stylistic Kana alternates", 'gsub_single', None, (('salt', (('kana', ('dflt',)),)),))
genseki.addLookupSubtable("Stylistic Kana alternates", "Stylistic Hiragana alternates")
genseki.addLookup("Historical Kana", 'gsub_alternate', None, (('hist', (('kana', ('dflt',)),)),))
genseki.addLookupSubtable("Historical Kana", "Historical Katakana")
genseki.addLookupSubtable("Historical Kana", "Hiragana to Hentaigana")

# グリフの変更
patchFont = fontforge.open(argv[4])
for glyph in patchFont:
	patchFont.selection.select(glyph)
	patchFont.copy()
	if glyph not in genseki:
		genseki.createChar(patchFont[glyph].unicode, patchFont[glyph].glyphname)
		# 拡張濁点・半濁点
		glyphPattern = re.search(r'^(uni30[0-9A-F]{2})_(uni309[9A])\.ccmp$', glyph, re.A)
		if glyphPattern:
			genseki[glyph].addPosSub(subtableForDakuten, glyphPattern.group(1, 2))
		glyphPattern = re.search(r'^(u1B0[0-9A-F]{2})_(uni309[9A])\.ccmp$', glyph, re.A)
		if glyphPattern:
			genseki[glyph].addPosSub("Hentaigana with dakuten", glyphPattern.group(1, 2))
		# 「し」「そ」の異体字
		glyphPattern = re.search(r'^(uni30[0-9A-F]{2})\.salt$', glyph, re.A)
		if glyphPattern:
			genseki[glyphPattern.group(1)].addPosSub("Stylistic Hiragana alternates", glyph)
		# 「ネ」「ヰ」の異体字
		glyphPattern = re.search(r'^(uni30[0-9A-F]{2})\.hist$', glyph, re.A)
		if glyphPattern:
			genseki[glyphPattern.group(1)].addPosSub("Historical Katakana", glyph)
		glyphPattern = re.search(r'^(u1B1[0-9A-F]{2})\.hist$', glyph, re.A)
		if glyphPattern:
			genseki[glyphPattern.group(1)].addPosSub("Historical Katakana", glyph)
	genseki.selection.select(glyph)
	genseki.paste()
patchFont.close(); patchFont = None

# 変体仮名検索用
addDakuten = lambda x: x + '_uni3099.ccmp'
addHandakuten = lambda x: x + '_uni309A.ccmp'
checkExistence = lambda x: x in genseki
hiraganaToHentaigana.update({
	# が
	'uni304C': tuple(filter(checkExistence, map(addDakuten, hiraganaToHentaigana['uni304B']))),
	'uni304E': tuple(filter(checkExistence, map(addDakuten, hiraganaToHentaigana['uni304D']))),
	'uni3050': tuple(filter(checkExistence, map(addDakuten, hiraganaToHentaigana['uni304F']))),
	'uni3052': tuple(filter(checkExistence, map(addDakuten, hiraganaToHentaigana['uni3051']))),
	'uni3054': tuple(filter(checkExistence, map(addDakuten, hiraganaToHentaigana['uni3053']))),

	# ざ
	'uni3056': tuple(filter(checkExistence, map(addDakuten, hiraganaToHentaigana['uni3055']))),
	'uni3058': tuple(filter(checkExistence, map(addDakuten, hiraganaToHentaigana['uni3057']))),
	'uni305A': tuple(filter(checkExistence, map(addDakuten, hiraganaToHentaigana['uni3059']))),
	'uni305C': tuple(filter(checkExistence, map(addDakuten, hiraganaToHentaigana['uni305B']))),
	'uni305E': tuple(filter(checkExistence, map(addDakuten, hiraganaToHentaigana['uni305D']))),

	# だ
	'uni3060': tuple(filter(checkExistence, map(addDakuten, hiraganaToHentaigana['uni305F']))),
	'uni3062': tuple(filter(checkExistence, map(addDakuten, hiraganaToHentaigana['uni3061']))),
	'uni3065': tuple(filter(checkExistence, map(addDakuten, hiraganaToHentaigana['uni3064']))),
	'uni3067': tuple(filter(checkExistence, map(addDakuten, hiraganaToHentaigana['uni3066']))),
	'uni3069': tuple(filter(checkExistence, map(addDakuten, hiraganaToHentaigana['uni3068']))),

	# ば
	'uni3070': tuple(filter(checkExistence, map(addDakuten, hiraganaToHentaigana['uni306F']))),
	'uni3073': tuple(filter(checkExistence, map(addDakuten, hiraganaToHentaigana['uni3072']))),
	'uni3076': tuple(filter(checkExistence, map(addDakuten, hiraganaToHentaigana['uni3075']))),
	'uni3079': tuple(filter(checkExistence, map(addDakuten, hiraganaToHentaigana['uni3078']))),
	'uni307C': tuple(filter(checkExistence, map(addDakuten, hiraganaToHentaigana['uni307B']))),

	# ぱ
	'uni3071': tuple(filter(checkExistence, map(addHandakuten, hiraganaToHentaigana['uni306F']))),
	'uni3074': tuple(filter(checkExistence, map(addHandakuten, hiraganaToHentaigana['uni3072']))),
	'uni3077': tuple(filter(checkExistence, map(addHandakuten, hiraganaToHentaigana['uni3075']))),
	'uni307A': tuple(filter(checkExistence, map(addHandakuten, hiraganaToHentaigana['uni3078']))),
	'uni307D': tuple(filter(checkExistence, map(addHandakuten, hiraganaToHentaigana['uni307B']))),
})
for glyph in hiraganaToHentaigana.items():
	if len(glyph[1]) > 0:
		genseki[glyph[0]].addPosSub("Hiragana to Hentaigana", glyph[1])

# ギリシア・ロシア・一部の記号
for glyph in genseki:
	paddingWidth = 1000 - genseki[glyph].width
	if isToBeConvertedToFullwidth(genseki, glyph):
		genseki[glyph].left_side_bearing = genseki[glyph].left_side_bearing + (paddingWidth // 2)
		genseki[glyph].width = 1000
	elif isToBeConvertedToFullwidthLeft(genseki, glyph):
		genseki[glyph].width = 1000
	elif isToBeConvertedToFullwidthRight(genseki, glyph):
		genseki[glyph].left_side_bearing = genseki[glyph].left_side_bearing + paddingWidth
		genseki[glyph].width = 1000

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
	selectGlyphsWorthOutputting(genseki, lambda glyph: glyph.width == w and glyph.unicode not in range(0x2500, 0x2580))
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
	if lookup.find("jp78") == lookup.find("jp83") == lookup.find("jp90") == lookup.find("nlck") == lookup.find("ccmp") == -1 \
	and lookup != "Stylistic Kana alternates" and lookup != "Historical Kana":
		genseki.removeLookup(lookup)

# OTFグリフクラス（ワークアラウンド）
for glyph in genseki:
	if genseki[glyph].isWorthOutputting():
		genseki[glyph].glyphclass = "baseglyph"

# サイズ調整（Ricty Diminishedと同様）
selectGlyphsWorthOutputting(genseki, lambda glyph: glyph.unicode not in range(0x2500, 0x2580))
genseki.transform(psMat.compose(psMat.scale(0.95), psMat.translate(10, 0)), ('noWidth', 'round'))

# 統合
font.mergeFonts(genseki)
font.encoding = "UnicodeFull"

# `aalt`機能を更新
font.buildOrReplaceAALTFeatures()

# 出力
font.generate(argv[1])
