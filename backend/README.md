## Local Development Env Setup

``` bash
# install dependencies
pipenv --python /usr/local/bin/python3 install

# start virtual environment mode
pipenv shell

# serve at localhost:5000
python run.py
```

## URL access
```
http://localhost:5000/api
```

## MySQL Localhost Server, Created DBs and ID/PW required : root/rootpw
```sql
CREATE SCHEMA `simplesmartcheck` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci;
CREATE SCHEMA `simplesmartcheckusers` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_520_ci;
```