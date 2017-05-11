receiver:
	python rec.py > out1.txt 2> err1.txt

sender: 
	cat inputfile.txt | python sender.py 2> err2.txt

clean: 
	rm -f *.swp
