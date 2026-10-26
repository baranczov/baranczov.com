#!/bin/sh
# Compile with pdfLaTeX (TeX Live / MacTeX / MiKTeX).
set -eu
cd "$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
if command -v pdflatex >/dev/null 2>&1; then
    engine=pdflatex
elif [ -x /Library/TeX/texbin/pdflatex ]; then
    engine=/Library/TeX/texbin/pdflatex
else
    echo 'Install TeX Live, MacTeX or MiKTeX with Russian language support and CM Super fonts.' >&2
    exit 1
fi
mkdir -p .build/texmf-var
export TEXMFVAR="$PWD/.build/texmf-var"
"$engine" -interaction=nonstopmode -halt-on-error -output-directory=.build main.tex
"$engine" -interaction=nonstopmode -halt-on-error -output-directory=.build main.tex
cp .build/main.pdf CV_Danil_Barantsov_updated.pdf
