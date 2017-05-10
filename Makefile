receiver:
	python rec.py > out1.txt

sender: 
	cat inputfile.txt | python sender.py

clean: 
	rm -f *.swp
