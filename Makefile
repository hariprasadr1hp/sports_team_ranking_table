.PHONY: all test clean

all: main.py
	python main.py

test:
	pytest -q

generate: genhtml

genhtml:
	emacs --batch --no-init-file --visit report.org --funcall org-html-export-to-html

clean: clean-pyc clean-build clean-gen

clean-pyc:
	find . -name '*.pyc' -exec rm --force {} + 
	find . -name '*.pyo' -exec rm --force {} + 

clean-build:
	rm --force --recursive build/
	rm --force --recursive dist/
	rm --force --recursive *.egg-info

clean-gen:
	rm -f *.html~ *.pdf~ *.tex~