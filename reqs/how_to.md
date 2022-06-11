1. Go to root directory (*fl_sentence_metadata_extractor/*)  

2. Create venv:  
`python3 -m venv ENV`  

3. Activate venv:  
    - **Windows:** `ENV\Scripts\activate.bat`  
    - **Mac:** `source ENV/bin/activate`  

4. Upgrade pip:  
`python3 -m pip3 install --upgrade pip`  

5. `cd` to `src/reqs/`  

6. `python setup.py install`

#### Notes  
- If your package is mostly for development purposes but *you aren’t planning on redistributing* it, **requirements.txt** should be enough (even when the package is developed on multiple machines).  

- If your package is developed *only by yourself* (i.e. on a single machine) but you are planning to redistribute it, then **setup.py/setup.cfg** should be enough.  

- If you package is developed on multiple machines and you also need to redistribute it, you will need both the requirements.txt and setup.py/setup.cfg files.  
