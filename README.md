# Shiphero Orders ETL

 ### How to run the app locally?

1. Setup virtual environment (optional)
```
py -m venv venv
```
```
venv\scripts\activate
```

2. Install requirements
```
pip install -r requirements
```

3. Add authentication token in the token.txt

4. Generate schema (optional) (already provided)

5. Extract data (configure data filters and selection manually from the file)
```
py get-orders.py
```

6. Process data (currently the format of the processed data is for demonstration purposes only)
```
py process.py
```