# Fontbakery exemption explained #

## -xfontdata_namecheck ##
This check depends on an external service but it is often offline since Dec 2025.
If offline, the check causes an error, not a fail.

## -xopentype/STAT/ital_axis ##
This check is explained assuming a family of variable fonts, but ours is actually not a variable font.

## -xfile_size ##
File size is not an issue unless used as a webfont.
This is a Han font with large coverage; large size is inevitable.

## -xoverlapping_path_segments ##
For this font, this check crashes with out of memory issue.

## -xwhitespace_ink ##
In program source codes or scripts, fullwidth space is not a whitespace (I mean that causes an error.)
Programming fonts shall intentionally ink the fullwidth space in order to deal with this East-Asia-specific problem.

## -xopentype/xavgcharwidth ##
CJK monospace fonts requires `avgcharwidth` set to the halfwidth advance width.
Otherwise it does not work properly.

## -xcjk_chws_feature ##
Since this is a programming font, `chws` feature is not considered needed.
