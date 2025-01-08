# Fruit Analyzer

## Запуск
По умолчанию запускается на *http://127.0.0.1:5000*.

### Front
```
sudo apt-get update && \
  sudo apt-get install -y dotnet-sdk-8.0
```
```
cd front\
dotnet publish . -a x64
dotnet bin/Release/net8.0/linux-x64/FruitAnalyzerFront.dll
```
### Back
```
cd back/
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
fastapi dev app.py
```
