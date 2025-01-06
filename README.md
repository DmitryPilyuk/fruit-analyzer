# Fruit Analyzer

## Запуск
### Front
[.NET](https://learn.microsoft.com/ru-ru/dotnet/core/install/linux-ubuntu-install?tabs=dotnet8&pivots=os-linux-ubuntu-2410)
```
sudo apt-get update && \
  sudo apt-get install -y dotnet-sdk-8.0
```
App
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
Запускается на *http://127.0.0.1:8000*.
