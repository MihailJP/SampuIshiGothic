#!/usr/bin/env fontforge

from sys import argv
import fontforge, re

patch = fontforge.open(argv[3])
hentaigana = fontforge.open(argv[2])
glyphsToAppend = []

for glyphname in hentaigana:
	if not re.search(R'\.vert', glyphname):
		if re.search(r'^uni30.*\.', glyphname):
			glyphsToAppend.append(glyphname)
		elif re.search(r'^u1B(0|1[0-6]).*', glyphname):
			glyphsToAppend.append(glyphname)

for glyphname in glyphsToAppend:
	if glyphname in patch:
		patch[glyphname].unicode = -1
		patch[glyphname].glyphname = glyphname + ".dele"
		patch.createChar(hentaigana[glyphname].unicode, glyphname)
		patch.selection.select(glyphname + ".dele")
		patch.copy()
		patch.selection.select(glyphname)
		patch.paste()
		patch[glyphname].color = patch[glyphname + ".dele"].color
		patch.removeGlyph(glyphname + ".dele")
	else:
		patch.createChar(hentaigana[glyphname].unicode, glyphname)
		hentaigana.selection.select(glyphname)
		hentaigana.copy()
		patch.selection.select(glyphname)
		patch.paste()
		patch[glyphname].color = hentaigana[glyphname].color

patch.encoding = "Original"
patch.save(argv[1])
