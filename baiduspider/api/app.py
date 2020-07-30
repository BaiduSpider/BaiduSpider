"""BaiduSpider API

TODO: 添加关于API的文档
"""
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import os
import sys
# 导入包
sys.path.append(os.path.abspath('./baiduspider/core'))

from main import BaiduSpider

app = FastAPI()
spider = BaiduSpider()
# CORS
app.add_middleware(
    CORSMiddleware,
    # 允许所有CORS访问
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/web')
async def search_web(query: str, page: int = 1) -> dict:
    return {
        'status': 'success',
        'results': spider.search_web(query, page)
    }


@app.get('/pic')
async def search_pic(query: str, page: int = 1):
    return {
        'status': 'success',
        'results': spider.search_pic(query, page)
    }


@app.get('/zhidao')
async def search_zhidao(query: str, page: int = 1):
    return {
        'status': 'success',
        'results': spider.search_zhidao(query, page)
    }


@app.get('/video')
async def search_video(query: str, page: int = 1):
    return {
        'status': 'success',
        'results': spider.search_video(query, page)
    }


@app.get('/news')
async def search_news(query: str, page: int = 1):
    return {
        'status': 'success',
        'results': spider.search_news(query, page)
    }


@app.get('/wenku')
async def search_wenku(query: str, page: int = 1):
    return {
        'status': 'success',
        'results': spider.search_wenku(query, page)
    }


@app.get('/jingyan')
async def search_jingyan(query: str, page: int = 1):
    return {
        'status': 'success',
        'results': spider.search_jingyan(query, page)
    }


@app.get('/baike')
async def search_baike(query: str):
    return {
        'status': 'success',
        'results': spider.search_baike(query)
    }


@app.get('/status')
async def get_status():
    return {
        'status': 'online'
    }
