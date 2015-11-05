#Makefile for YTCA

YTCA = php ytca.php

default: 
	$(YTCA) > index.html

clean:
	$(RM) *.html