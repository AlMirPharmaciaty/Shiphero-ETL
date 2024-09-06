# Shiphero ETL

 ### How to run the app locally?

1. Setup virtual environment
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

3. Add authentication token in the `.env` file

4. Generate schema (optional) (already generated)

5. Extract data (to json) (configure data selection manually from the file)
```
py extract_orders.py --datefrom=2024-08-01
```

6. Load data (into database)
```
py load_orders.py
```