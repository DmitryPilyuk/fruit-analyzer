# Fruit Analyzer

## Запуск
### Front
```
sudo apt-get update && \
  sudo apt-get install -y dotnet-sdk-8.0
```
```
cd front/
dotnet run
```
В терминале будет выведен ip
### Back
```
cd back/
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev app.py
```
