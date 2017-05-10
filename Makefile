receiver:
	python rec.py

sender: 
	cat inputfile.txt | python sender.py

clean: 
	rm -f *.swp
