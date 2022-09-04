.PHONY: main.pdf all charts clean

main.pdf: main.tex
	[[ -f ./assets/ltlenc_time_comparison.png \
	   && -f ./assets/ltlenc_stvar_comparison.png ]] || $(MAKE) charts
	latexmk -synctex=1 -interaction=nonstopmode -pdf -outdir=. ./main -shell-escape

charts:
	python ./assets/generate_charts.py

clean:
	latexmk -CA
	rm ./assets/ltlenc_stvar_comparison.png
	rm ./assets/ltlenc_time_comparison.png
