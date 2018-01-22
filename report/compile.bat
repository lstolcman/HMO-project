@echo off
call setenv.bat

del *.aux
del *.log
del *.out
del *.pdf

pdflatex report
pdflatex report

del *.aux
del *.log
del *.out

