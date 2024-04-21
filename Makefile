TARGETS=SampuIshiGothic.ttf SampuIshiGothic-Bold.ttf \
SampuIshiGothic-Italic.ttf SampuIshiGothic-BoldItalic.ttf
DOCUMENTS=README.md ChangeLog LICENSE
PACKAGES=SampuIshiGothic.tar.xz

.SUFFIXES: .tar.xz

.PHONY: all
all: ${TARGETS}

.INTERMEDIATE: ${TARGETS:.ttf=.ttx} ${TARGETS:.ttf=.raw.ttf} ${TARGETS:.ttf=.raw.ttx}

SampuIshiGothic.raw.ttf: Inconsolata-LGC/Inconsolata-LGC.sfd genseki-font/ttc/GenSekiGothic-R.ttc PatchGlyph-Regular.sfd
	./mkfont.py $@ $^

SampuIshiGothic-Bold.raw.ttf: Inconsolata-LGC/Inconsolata-LGC-Bold.sfd genseki-font/ttc/GenSekiGothic-B.ttc PatchGlyph-Bold.sfd
	./mkfont.py $@ $^

SampuIshiGothic-Italic.raw.ttf: Inconsolata-LGC/Inconsolata-LGC-Italic.sfd genseki-font/ttc/GenSekiGothic-R.ttc PatchGlyph-Regular.sfd
	./mkfont.py $@ $^

SampuIshiGothic-BoldItalic.raw.ttf: Inconsolata-LGC/Inconsolata-LGC-BoldItalic.sfd genseki-font/ttc/GenSekiGothic-B.ttc PatchGlyph-Bold.sfd
	./mkfont.py $@ $^

%.raw.ttx: %.raw.ttf
	ttx -o $@ $<
%.ttx: %.raw.ttx
	cat $< | sed -e '/isFixedPitch/s/value=".*"/value="1"/' -e '/bProportion/s/value=".*"/value="9"/' -e '/xAvgCharWidth/s/value=".*"/value="500"/' > $@
%.ttf: %.ttx
	ttx -o $@ $<

.PHONY: dist
dist: ${PACKAGES}

ChangeLog: .git
	Inconsolata-LGC/mkchglog.rb > $@ # GIT

SampuIshiGothic.tar.xz: ${TARGETS} ${DOCUMENTS}
	rm -rf $*; mkdir $*; cp ${TARGETS} ${DOCUMENTS} $*; tar cfvJ $@ $*

.PHONY: clean
clean:
	-rm -f ${TARGETS} ${PACKAGES}
	-rm -f ${TARGETS:.ttf=.ttx} ${TARGETS:.ttf=.raw.ttf} ${TARGETS:.ttf=.raw.ttx}
	-rm -rf ${PACKAGES:.tar.xz=}
