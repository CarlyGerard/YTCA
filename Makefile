#Makefile for YTCA

YTCA = php ytca.php

default: 
	$(YTCA) > test.html

clean:
	$(RM) *.html