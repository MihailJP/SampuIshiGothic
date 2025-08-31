TARGETS=SampuIshiGothic.ttf SampuIshiGothic-Bold.ttf \
SampuIshiGothic-Italic.ttf SampuIshiGothic-BoldItalic.ttf
TARGETS2=SampuIwaGothic.ttf SampuIwaGothic-Bold.ttf \
SampuIwaGothic-Italic.ttf SampuIwaGothic-BoldItalic.ttf
DOCUMENTS=README.md ChangeLog LICENSE
PACKAGES=SampuIshiGothic.tar.xz SampuIwaGothic.tar.xz

.SUFFIXES: .tar.xz

.PHONY: all
all: ${TARGETS} ${TARGETS2}

.INTERMEDIATE: ${TARGETS:.ttf=.ttx} ${TARGETS:.ttf=.raw.ttf} ${TARGETS:.ttf=.raw.ttx}
.INTERMEDIATE: ${TARGETS2:.ttf=.ttx} ${TARGETS2:.ttf=.raw.ttf} ${TARGETS2:.ttf=.raw.ttx}
.INTERMEDIATE: PatchGlyph2-Regular.sfd PatchGlyph2-Bold.sfd

PatchGlyph2-Regular.sfd: GenSekiHentaiganaGothic/GenSekiHentaiganaGothic.sfd PatchGlyph-Regular.sfd
	./mkpatch.py $@ $^

PatchGlyph2-Bold.sfd: GenSekiHentaiganaGothic/GenSekiHentaiganaGothic-Bold.sfd PatchGlyph-Bold.sfd
	./mkpatch.py $@ $^

SampuIshiGothic.raw.ttf SampuIwaGothic.raw.ttf: Inconsolata-LGC/Inconsolata-LGC.sfd genseki-font/ttc/GenSekiGothic2-R.ttc PatchGlyph2-Regular.sfd
	./mkfont.py $@ $^

SampuIshiGothic-Bold.raw.ttf SampuIwaGothic-Bold.raw.ttf: Inconsolata-LGC/Inconsolata-LGC-Bold.sfd genseki-font/ttc/GenSekiGothic2-B.ttc PatchGlyph2-Bold.sfd
	./mkfont.py $@ $^

SampuIshiGothic-Italic.raw.ttf SampuIwaGothic-Italic.raw.ttf: Inconsolata-LGC/Inconsolata-LGC-Italic.sfd genseki-font/ttc/GenSekiGothic2-R.ttc PatchGlyph2-Regular.sfd
	./mkfont.py $@ $^

SampuIshiGothic-BoldItalic.raw.ttf SampuIwaGothic-BoldItalic.raw.ttf: Inconsolata-LGC/Inconsolata-LGC-BoldItalic.sfd genseki-font/ttc/GenSekiGothic2-B.ttc PatchGlyph2-Bold.sfd
	./mkfont.py $@ $^

%.raw.ttx: %.raw.ttf
	ttx -t post -t "OS/2" -o $@ $<
%.ttx: %.raw.ttx
	cat $< | sed -e '/isFixedPitch/s/value=".*"/value="1"/' -e '/bProportion/s/value=".*"/value="9"/' -e '/xAvgCharWidth/s/value=".*"/value="500"/' > $@
%.ttf: %.raw.ttf %.ttx
	ttx -o $@ -m $^

.PHONY: dist
dist: ${PACKAGES}

ChangeLog: .git
	Inconsolata-LGC/mkchglog.rb > $@ # GIT

SampuIshiGothic.tar.xz: ${TARGETS} ${DOCUMENTS}
	rm -rf $*; mkdir $*; cp ${TARGETS} ${DOCUMENTS} $*; tar cfvJ $@ $*
SampuIwaGothic.tar.xz: ${TARGETS2} ${DOCUMENTS}
	rm -rf $*; mkdir $*; cp ${TARGETS2} ${DOCUMENTS} $*; tar cfvJ $@ $*

.PHONY: clean
clean:
	-rm -f ${TARGETS} ${TARGETS2} ${PACKAGES}
	-rm -f ${TARGETS:.ttf=.ttx} ${TARGETS:.ttf=.raw.ttf} ${TARGETS:.ttf=.raw.ttx}
	-rm -f ${TARGETS2:.ttf=.ttx} ${TARGETS2:.ttf=.raw.ttf} ${TARGETS2:.ttf=.raw.ttx}
	-rm -f PatchGlyph2-Regular.sfd PatchGlyph2-Bold.sfd
	-rm -rf ${PACKAGES:.tar.xz=}
