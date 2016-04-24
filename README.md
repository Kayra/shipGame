# shipGame

### This was a code test for a junior position at a company I applied to.
### Very happy with how it turned out so keeping it here as a milestone of my progress.


(Please ensure you have virtualenv and python3 installed)

virtualenv -p python3 venv

source venv/bin/activate

pip install -r requirements.txt

py.test shipGame (run tests)

python -m shipGame.app (calculate the game with the contents of shipGame/input.txt)
