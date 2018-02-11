#!/bin/sh
python extract-mac-boxscore.py 0 $@ |\
	awk "{sub(/[0-9\. ]+$/, \"\"); sub(/^ +/, \"\"); print;}" |\
	awk "{sub(/ [a-z0-9\/]+$/, \"\"); print;}" |\
	sort | uniq

#	awk "{if (NF<2) {last=\$1; first=\"\"} else {first=\$1; last=\$2}; id=tolower((substr(last,1,4) substr(first,1,1) \"001\")); print id \",\" last \",\" first}" |\
