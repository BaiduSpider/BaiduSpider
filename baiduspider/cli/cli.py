from main import BaiduSpider
import os
import sys
# 导入包
sys.path.append(os.path.abspath('./baiduspider/core'))

import click
from tabulate import tabulate
import readline

spider = BaiduSpider()


@click.command()
@click.option('--query', help='搜索关键词', prompt='请输入搜索关键词')
@click.option('--pn', help='搜索结果页码', prompt='请输入页码', default=1)
def search_web(query, pn):
    r"""搜索百度网页"""
    result_ = spider.search_web(query, pn=pn)
    results = []
    related = {}
    click.clear()
    for r in result_['results']:
        if r['type'] == 'result':
            if r['time'] is None:
                r['time'] = ''
            if r['origin'] is None:
                r['origin'] = ''
            if r['des'] is None:
                r['des'] = '暂无简介'
            click.echo(('%s\033[1m \033\x1b]8;;%s\a%s\x1b]8;;\a\033[0m %s' % (r['time'], r['url'], r['title'], r['origin'])))
            click.echo(r['des'])
        elif r['type'] == 'calc':
            click.echo('\033[1m \x1b %s\033[0m 计算' % r['process'])
            click.echo('=%s' % r['result'])
        elif r['type'] == 'baike':
            click.echo(('\033[1m \033\x1b]8;;%s\a%s\x1b]8;;\a\033[0m 百科' % (r['result']['url'], r['result']['title'])))
            click.echo(r['result']['des'])
        elif r['type'] == 'news':
            click.echo('\033[1m %s的最新新闻\033[0m 资讯' % query)
            for _ in r['results']:
                click.echo('%s\033[1m \033\x1b]8;;%s\a%s\x1b]8;;\a\033[0m %s' % (_['time'], _['url'], _['title'], _['author']))
        elif r['type'] == 'video':
            click.echo('\033[1m %s的相关视频\033[0m 视频' % query)
            for _ in r['results']:
                click.echo('\033[1m \033\x1b]8;;%s\a%s\x1b]8;;\a\033[0m 时长：%s - %s' % (_['url'], _['title'], _['length'], (_['origin'] if _['origin'] else '暂无')))
        elif r['type'] == 'total':
            click.echo('BaiduSpider共找到搜索结果大约%d个' % result_['results'][0]['result'])
        elif r['type'] == 'related':
            related = r
        if r['type'] != 'related':
            click.echo('-' * 100)
            
    click.echo('\033[1m相关搜索\033[0m')
    i = 0
    for r in related['results']:
        if i % 4 == 0 and i != 0:
            print('')
        print(format(r, '<20'), end='')
        i += 1
    click.echo('')
    click.echo('-' * 100)
    click.echo(('\033[1m共%d页，第%d页\033[0m\n' % (result_['total'], pn)).rjust(100))

if __name__ == '__main__':
    search_web()
