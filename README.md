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

3. Add authentication token in the `.env` file

4. Generate schema (optional) (already provided)

5. Extract data (to json) (configure data selection manually from the file)
```
py extract.py --date=2024-08-01
```

6. Transform data (json to csv) (currently the format of the processed data is for demonstration purposes only)
```
py transform.py
```

7. Load data (into sqlite) (the db model is not production-ready)
```
py load.py
```