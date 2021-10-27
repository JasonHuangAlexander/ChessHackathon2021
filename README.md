# INTRODUCTION

A platform using different AI and non-AI algorithms to play the game of chess.

# PREREQUISITES

You will need these on Azure:

* A subscription
* A resource group

You will need this locally to deploy to Azure:

* Azure CLI

# DEPLOY WEBAPP LOCALLY

It useful to run and debug the webapp locally before deploying to Azure.

1. generate credentials
   1. browse https://garage-06.visualstudio.com/_git/Chess%20AI%202356%20104783
   2. click **Clone** > **Generate Git Credentials**
   3. copy username and password to a safe place
2. clone repo to a local directory
   1. git clone https://garage-06.visualstudio.com/Chess%20AI%202356%20104783/_git/Chess%20AI%202356%20104783
   2. use credentials from above 
3. cd Chess%20AI%202356%20104783
4. py -3 -m venv env
5. env\scripts\activate
6. pip install -r requirements.txt
7. set environment variables. For example, on Windows:
   1. SET APP_KEY={choose a secure key for your webapp}
8. download engines
   1. Stockfish: https://stockfishchess.org/download/
      1. example: download and unzip AVX2
   2. Leela: https://lczero.org/play/download/
      1. example: download and unzip DNNL BLAS
   3. Andoma: https://github.com/healeycodes/andoma
      1. example: git clone https://github.com/healeycodes/andoma.git
   4. set the full path for each engine's executable in engines.py 
9. flask run
10. browse http://localhost:5000/

# DEPLOY WEBAPP TO AZURE

```
set sub=%YOUR_SUB%
set rg=%YOUR_RG%
set app_plan=%YOUR_APP_SERVICE_PLAN% (e.g. chessaiappserviceplan)
set sku=B1
set app_name=%YOUR_APP_NAME% (e.g. chessai)
```

1. cd Chess%20AI%202356%20104783
2. uncomment each engine's full path under "Azure" in engines.py
3. deploy web app to Azure
> az webapp up --plan %app_plan% --sku %sku% --name %app_name% --subscription %sub% --resource-group %rg%
4. download engines
   1. from the Azure portal, ssh into the web app
   2. stockfish (https://stockfishchess.org/download/)
      1. mkdir /home/stockfish
      2. cd /home/stockfish
      3. wget https://stockfishchess.org/files/stockfish_14_linux_x64.zip
      4. unzip *.zip
   3. leela (https://lczero.org/play/download/)
      > no Linux download available and no working build yet.
   4. Andoma: https://github.com/healeycodes/andoma
      1. mkdir /home/andoma
      2. cd /home/andoma
      3. wget https://github.com/healeycodes/andoma/archive/refs/heads/main.zip
      4. unzip *.zip

5. once available, add these web app configuration parameters:
```
| Name | Value |
| --- | --- |
| APP_KEY | choose a secure key for your webapp |
```
6. browse: https://%YOUR_APP_NAME%.azurewebsites.net/

# USAGE

1. Select color (or just accept the default)
2. Select algorithm (or just accept the default)
3. Play the game
4. You can click **New Game** at any time