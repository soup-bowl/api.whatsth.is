import urllib3
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router
from api.cache import Cache
from api.config import Config

def_url  = 'https://gist.githubusercontent.com/soup-bowl/ca302eb775278a581cd4e7e2ea4122a1/raw/definitions.yml'
def_file = urllib3.PoolManager().request('GET', def_url)

config = Config()
cache  = Cache()

if def_file.status == 200:
    print("Loaded latest definition file from GitHub.")
    config.load_yml( def_file.data.decode('utf-8') )
else:
    print("Unable to download definitions file.")
    exit(1)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router.router)

@app.get("/")
async def root():
    return {
        "success": False,
        "message": "No URL specified"
    }
