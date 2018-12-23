## Backend API info
https://backend.smartcheck.ml/api

## Build Setup

``` bash
# install dependencies
pipenv install

# start virtual environment mode
pipenv shell

# install solc
python contracts_controller.py --option install

# deploy contracts to blockchain network
# check variables in contracts_controller.json
python contracts_controller.py --option deploy

# build for production with minification
pipenv lock --pre --clear --verbose

# serve at localhost:5000
python run.py
```

## Deploy (with Zappa)

``` bash
# initialize serverless framework
zappa init

# deploy 
zappa deploy dev

# update
zappa update dev
```
