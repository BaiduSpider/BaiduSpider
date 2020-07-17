"""BaiduSpider API

TODO: 添加关于API的文档
"""
from fastapi import FastAPI
import os
from main import BaiduSpider

app = FastAPI()
spider = BaiduSpider()


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
