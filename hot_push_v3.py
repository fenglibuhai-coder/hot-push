#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热点推送机器人 - GitHub Actions 版本
自动从多个平台抓取实时热点并推送到钉钉群聊
"""

import json
import urllib.request
import urllib.parse
import urllib.error
import ssl
import re
import os
from datetime import datetime

# 从环境变量读取 Webhook 地址（更安全）
WEBHOOK_URL = os.getenv('DINGTALK_WEBHOOK', 'https://oapi.dingtalk.com/robot/send?access_token=10de97ac90aa5fd37112042426da283c620a4ac4fa314e9277a24200c71ee95a')

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

# 创建 SSL 上下文（忽略证书验证）
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE


def fetch_weibo():
    """抓取微博热搜"""
    try:
        url = 'https://tophub.today/n/KqndgxeLl9'
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
            html = response.read().decode('utf-8')
        
        pattern = r'<a href="([^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        results = []
        for link, title in matches[10:20]:  # 跳过导航，取前10条热搜
            results.append({
                'title': title.strip(),
                'link': link if link.startswith('http') else f'https://tophub.today{link}',
                'hot': ''
            })
        return results[:10]
    except Exception as e:
        print(f'微博抓取失败: {e}')
        return []


def fetch_zhihu():
    """抓取知乎热榜"""
    try:
        url = 'https://tophub.today/n/mproPpoq6O'
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
            html = response.read().decode('utf-8')
        
        pattern = r'<a href="([^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        results = []
        for link, title in matches[10:20]:
            results.append({
                'title': title.strip(),
                'link': link if link.startswith('http') else f'https://tophub.today{link}',
                'hot': ''
            })
        return results[:10]
    except Exception as e:
        print(f'知乎抓取失败: {e}')
        return []


def fetch_douyin():
    """抓取抖音热榜"""
    try:
        url = 'https://tophub.today/n/DpQvNABoNE'
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
            html = response.read().decode('utf-8')
        
        pattern = r'<a href="([^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        results = []
        for link, title in matches[10:20]:
            results.append({
                'title': title.strip(),
                'link': link if link.startswith('http') else f'https://tophub.today{link}',
                'hot': ''
            })
        return results[:10]
    except Exception as e:
        print(f'抖音抓取失败: {e}')
        return []


def fetch_xiaohongshu():
    """抓取小红书热榜"""
    try:
        url = 'https://tophub.today/n/ly8Q0K9dVx'
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
            html = response.read().decode('utf-8')
        
        pattern = r'<a href="([^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        results = []
        for link, title in matches[10:20]:
            results.append({
                'title': title.strip(),
                'link': link if link.startswith('http') else f'https://tophub.today{link}',
                'hot': ''
            })
        return results[:10]
    except Exception as e:
        print(f'小红书抓取失败: {e}')
        return []


def fetch_36kr():
    """抓取36氪热点"""
    try:
        url = 'https://tophub.today/n/KqndgapoLl'
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
            html = response.read().decode('utf-8')
        
        pattern = r'<a href="([^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        results = []
        for link, title in matches[10:20]:
            results.append({
                'title': title.strip(),
                'link': link if link.startswith('http') else f'https://tophub.today{link}',
                'hot': ''
            })
        return results[:10]
    except Exception as e:
        print(f'36氪抓取失败: {e}')
        return []


def fetch_sspai():
    """抓取少数派精选"""
    try:
        url = 'https://tophub.today/n/mq7pQn50Ko'
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
            html = response.read().decode('utf-8')
        
        pattern = r'<a href="([^"]+)"[^>]*>([^<]+)</a>'
        matches = re.findall(pattern, html)
        
        results = []
        for link, title in matches[10:15]:
            results.append({
                'title': title.strip(),
                'link': link if link.startswith('http') else f'https://tophub.today{link}',
                'hot': ''
            })
        return results[:5]
    except Exception as e:
        print(f'少数派抓取失败: {e}')
        return []


def format_section(name, emoji, items):
    """格式化单个平台的热点内容"""
    if not items:
        return f'### {emoji} {name}\n\n暂无数据\n\n---\n\n'
    
    lines = [f'### {emoji} {name}\n']
    for i, item in enumerate(items, 1):
        title = item['title']
        link = item['link']
        hot = item.get('hot', '')
        
        # 构建标题（带热度值）
        display_title = f'{title} 🔥{hot}' if hot else title
        
        # 构建链接
        lines.append(f'{i}. [{display_title}]({link})')
    
    lines.append('\n---\n')
    return '\n'.join(lines)


def build_message():
    """构建完整的推送消息"""
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    
    weibo = fetch_weibo()
    zhihu = fetch_zhihu()
    douyin = fetch_douyin()
    xiaohongshu = fetch_xiaohongshu()
    kr36 = fetch_36kr()
    sspai = fetch_sspai()
    
    title = f'🔥 全网热点速报 ({now})'
    
    content = f'''# 🔥 全网热点速报

> 📅 抓取时间：{now}

---

{format_section("微博热搜", "📱", weibo)}

{format_section("知乎热榜", "🧠", zhihu)}

{format_section("抖音热榜", "🎵", douyin)}

{format_section("小红书热榜", "📕", xiaohongshu)}

{format_section("36氪热点", "📰", kr36)}

{format_section("少数派精选", "⚡", sspai)}

> 🤖 自动推送 | 每日 10:30 和 16:30 更新
'''
    
    return title, content


def send_to_dingtalk():
    """发送消息到钉钉"""
    title, content = build_message()
    
    data = {
        'msgtype': 'markdown',
        'markdown': {
            'title': title,
            'text': content
        }
    }
    
    try:
        payload = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(
            WEBHOOK_URL,
            data=payload,
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=10, context=ssl_context) as response:
            result = json.loads(response.read().decode('utf-8'))
            
            if result.get('errcode') == 0:
                print('✅ 钉钉推送成功！')
            else:
                print(f'❌ 钉钉推送失败: {result}')
    except Exception as e:
        print(f'❌ 推送异常: {e}')


if __name__ == '__main__':
    send_to_dingtalk()
