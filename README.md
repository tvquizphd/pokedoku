## Pokedoku

Install anaconda [on Linux](https://docs.anaconda.com/anaconda/install/linux/), [on MacOS](https://docs.anaconda.com/anaconda/install/mac-os/), or [on Windows](https://docs.anaconda.com/anaconda/install/windows/).

```
conda update -n base -c defaults conda
conda update conda

conda create -n pokedoku python=3.11
conda activate pokedoku 
conda install fastapi=0
conda install uvicorn=0
conda install pydantic=1
conda install python-dotenv=1
conda install pydantic-settings=2
pip install pypokedex==1
```

### Run demo

```
python test.py
```
