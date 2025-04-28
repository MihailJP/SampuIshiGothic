プログラミング用フォント 算譜石ゴシック
=======================================

プログラミング用フォント [Inconsolata LGC](https://github.com/MihailJP/Inconsolata-LGC) に、
[源石ゴシック](https://github.com/ButTaiwan/genseki-font) を元にした日本語グリフを追加したものです。

変体仮名のグリフは、一部を除き[しょかき変体仮名ゴチック](https://booth.pm/ja/items/5633978)または
[すきまゴシック](https://booth.pm/ja/items/2117070)に由来します。

日本語グリフの特徴 (源石ゴシックからの変更点)
---------------------------------------------
- プログラマーの天敵「全角スペース」を可視化しています。
- 半濁点を大きくしました。
- 平仮名の「へ」と片仮名の「ヘ」の区別がつきやすいよう、前者を丸くし、後者を尖らせてあります。
- 区別がつきやすいよう、「ー」（長音）の字形に手を加えました。
- 片仮名と字形が類似した漢字の「一」、「二」、「力」、「口」、「工」、「卜」にセリフを付けました。
- 一部の濁点付き・半濁点付きグリフを追加しました。
- 小書き仮名拡張 (Small Kana Extension) のグリフ (Unicode 15.0 で登録されている 9 文字) を追加しました。
- 平安時代の片仮名ア行エ・平仮名や行え（仮名補助にあるもの）を追加しました。
- 明治時代に一部で使われたや行い・や行え・わ行う（仮名拡張 A にあるもの）を追加しました。
- 変体仮名を追加しました（グリフの出所は後述）。
- 「し」「そ」の（変体仮名ではない）異体字を追加しました。`salt` で呼び出せます。
- 戦前に使われた「ネ」「ヰ」の異体字を追加しました。`hist` で呼び出せます。

### 変体仮名グリフの出所

Version 2.4 では変体仮名を追加しました。変体仮名フォントはほとんどが明朝体で、ゴシック体は稀です。

- A: [しょかき変体仮名ゴチック](https://booth.pm/ja/items/5633978)に由来するもの（PatchGlyph-*.sfdではオレンジ色でマーク）
- B: [すきまゴシック](https://booth.pm/ja/items/2117070)に由来するもの（PatchGlyph-*.sfdでは赤でマーク）
- C: 独自に追加したもの ([源石ゴシック](https://github.com/ButTaiwan/genseki-font)由来)（PatchGlyph-*.sfdでは黄色でマーク）

#### 仮名補助

|         | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F |
|:-------:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| U+1B00x | A | A | A | A | A | A | A | A | A | A | A | A | B | A | A | A |
| U+1B01x | B | B | B | A | B | A | B | B | B | A | A | B | B | A | A | A |
| U+1B02x | B | A | B | B | A | B | A | A | B | B | A | A | B | B | B | B |
| U+1B03x | A | B | B | B | A | B | B | A | A | B | A | B | B | B | B | A |
| U+1B04x | B | B | B | B | B | B | B | B | A | B | B | B | B | B | A | A |
| U+1B05x | B | A | A | B | B | A | B | B | B | B | A | A | B | B | B | A |
| U+1B06x | C | B | B | B | B | B | A | B | B | B | B | B | A | A | B | B |
| U+1B07x | B | B | A | B | B | B | B | B | B | B | B | A | B | B | B | B |
| U+1B08x | B | C | B | B | B | B | A | B | B | B | B | A | A | B | B | B |
| U+1B09x | B | A | B | B | A | B | B | B | B | B | B | B | A | B | B | A |
| U+1B0Ax | B | B | B | B | B | B | A | B | B | B | B | B | B | B | B | A |
| U+1B0Bx | B | A | B | B | B | B | A | A | B | A | B | B | B | B | B | B |
| U+1B0Cx | A | B | B | B | B | A | B | B | B | B | B | B | B | C | A | B |
| U+1B0Dx | B | A | B | B | A | B | B | B | B | B | C | B | A | B | A | B |
| U+1B0Ex | B | B | B | B | B | C | A | B | B | B | B | B | B | A | B | B |
| U+1B0Fx | C | B | B | B | B | B | B | B | B | B | B | C | B | A | B | B |

#### 仮名拡張A

|         | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F |
|:-------:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|:-:|
| U+1B10x | B | B | B | B | B | B | B | B | B | B | B | B | B | B | B | B |
| U+1B11x | B | B | B | B | B | B | B | B | B | B | A | B | B | B | B | C |
| U+1B12x | C | C | C |   |   |   |   |   |   |   |   |   |   |   |   |   |

派生フォント：算譜岩ゴシック
----------------------------
- East Asian ambiguous width の殆どで全角を使用するようにしたバージョンです。
- 一部 ambiguous 扱いでないのに全角になっている場合があります。

ライセンス
----------
このフォントは、[SIL Open Font License Version 1.1](LICENSE) でライセンスされています。

上記「変体仮名グリフの出所」の A と B についても、SIL Open Font License Version 1.1
でライセンスされています。
