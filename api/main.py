"""Main FastAPI runner.
"""

from os import getenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api import router
from api.redis import init_redis_pool, CacheService

app = FastAPI(
	title="What's This? API",
	description="Inspection application that detects web technologies and informs the user of them - https://whatsth.is",
	contact={
		"name": "Soupbowl",
		"email": "code@soupbowl.io",
		"url": "https://www.soupbowl.io",
	},
	license_info={
		"name": "MIT",
		"url": "https://github.com/soup-bowl/api.whatsth.is/blob/main/LICENSE",
	},
	# https://fastapi.tiangolo.com/advanced/extending-openapi/#configuring-swagger-ui
	docs_url="/",
	swagger_ui_parameters={
		"syntaxHighlight.theme": "monokai"
	},
	redoc_url=None,
	version="0.2.13"
)

app.add_middleware(
	CORSMiddleware,
	allow_origins=[getenv('WTAPI_CORS_POLICY', "*")],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

app.include_router(router.router)

@app.on_event("startup")
async def startup_event():
	"""Events to initiate on the beginning of the API.
	"""
	app.state.redis = await init_redis_pool()
	app.state.rcache = CacheService(app.state.redis)

@app.on_event("shutdown")
async def shutdown_event():
	"""Disposal events after the API goes down.
	"""
	await app.state.redis.close()
