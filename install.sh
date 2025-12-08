#!/bin/sh

mkdir -p katex
curl -L -o "katex/katex_min.css" https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css
curl -L -o "katex/katex_min.js" https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js
curl -L -o "katex/auto_render_min.js" https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/contrib/auto-render.min.js

BASE=https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/fonts
mkdir -p katex/fonts

for f in \
KaTeX_AMS-Regular.woff2 \
KaTeX_Caligraphic-Bold.woff2 \
KaTeX_Caligraphic-Regular.woff2 \
KaTeX_Fraktur-Bold.woff2 \
KaTeX_Fraktur-Regular.woff2 \
KaTeX_Main-Bold.woff2 \
KaTeX_Main-BoldItalic.woff2 \
KaTeX_Main-Italic.woff2 \
KaTeX_Main-Regular.woff2 \
KaTeX_Math-BoldItalic.woff2 \
KaTeX_Math-Italic.woff2 \
KaTeX_SansSerif-Bold.woff2 \
KaTeX_SansSerif-Italic.woff2 \
KaTeX_SansSerif-Regular.woff2 \
KaTeX_Script-Regular.woff2 \
KaTeX_Size1-Regular.woff2 \
KaTeX_Size2-Regular.woff2 \
KaTeX_Size3-Regular.woff2 \
KaTeX_Size4-Regular.woff2 \
KaTeX_Typewriter-Regular.woff2
do
    curl -L -o katex/fonts/$f $BASE/$f
done

