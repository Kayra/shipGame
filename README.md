# shipGame

(Please ensure you have virtualenv and python3 installed)

virtualenv -p python3 venv

source venv/bin/activate

pip install -r requirements.txt

py.test shipGame (run tests)

python -m shipGame.app (calculate the game with the contents of shipGame/input.txt)
