#!/bin/bash
sed -Ee 's/([A-Z]+)[^}]+/\1/g' \
	-e 's/\?\=/\=/g' \
	-e 's/\?\?/\=S/g' \ # for unknown abbrevations
	-e 's/\=ADVPRO\}/\=ADV\}/g' \
	-e 's/\=ANUM\}/\=A\}/g' \
	-e 's/\=APRO\}/\=A\}/g' \
	-e 's/\=COM\}/\=ADV\}/g' \
	-e 's/\=NUM\}/\=S\}/g' \
	-e 's/\=PART\}/\=ADV\}/g' \
	-e 's/\=SPRO\}/\=S\}/g' \
	-e 's/\=INTJ\}/\=ADV\}/g' 	ch3.txt > ch3_out.txt
