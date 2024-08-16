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

3. Extract data (configure data filters and selection manually from the file)
```
py get-orders.py
```

4. Process data
```
py process.py
```