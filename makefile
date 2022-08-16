.PHONY: main.pdf all clean

main.pdf: main.tex
	latexmk -synctex=1 -interaction=nonstopmode -pdf -outdir=. ./main -shell-escape

clean:
	latexmk -CA
