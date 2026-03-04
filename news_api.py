#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
新闻自动更新服务 API
第二阶段：自动更新功能后端
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import random
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)

class NewsUpdaterService:
    def __init__(self):
        self.news_cache = {}
        self.last_update = None
        self.categories = ['ai', 'business', 'finance', 'culture', 'policy']
        
    def get_latest_news(self, category=None, limit=5):
        """获取最新新闻"""
        # 模拟新闻数据（实际使用时从数据库或爬虫获取）
        mock_news = {
            'ai': [
                {
                    'id': 'ai_001',
                    'title': '【OpenAI】GPT-5.3 Instant发布，响应速度提升40%',
                    'summary': 'OpenAI发布最新版本GPT-5.3 Instant，在保持模型能力的同时大幅提升响应速度，为用户带来更流畅的AI体验。',
                    'source': '新浪科技',
                    'url': 'https://finance.sina.com.cn/world/2026-03-04/doc-inhpufut3573444.shtml',
                    'timestamp': datetime.now().isoformat(),
                    'isNew': True
                },
                {
                    'id': 'ai_002',
                    'title': '【百度】文心一言API调用量突破15亿次/日',
                    'summary': '百度公布文心一言最新数据，API日均调用量突破15亿次，企业级应用场景持续扩展。',
                    'source': '36氪',
                    'url': 'https://finance.sina.com.cn/stock/relnews/hk/2026-01-20/doc-inhhxznx7438504.shtml',
                    'timestamp': datetime.now().isoformat(),
                    'isNew': True
                }
            ],
            'business': [
                {
                    'id': 'biz_001',
                    'title': '【淘宝】直播电商GMV突破5.2万亿',
                    'summary': '淘宝直播年度GMV再创新高，专业主播和品牌自播成为增长双引擎。',
                    'source': '电商报',
                    'url': 'https://www.163.com/dy/article/KMS2Q04S0511DBV1.html',
                    'timestamp': datetime.now().isoformat(),
                    'isNew': True
                },
                {
                    'id': 'biz_002',
                    'title': '【Temu】月活用户突破3.5亿',
                    'summary': '拼多多旗下跨境电商平台Temu月活用户持续增长，全球化布局加速。',
                    'source': '界面新闻',
                    'url': 'https://www.icbea.com/industryNews/details/210046',
                    'timestamp': datetime.now().isoformat(),
                    'isNew': False
                }
            ],
            'finance': [
                {
                    'id': 'fin_001',
                    'title': '【A股】沪指站稳4100点，科技股领涨',
                    'summary': 'A股市场延续强势，上证指数站稳4100点，人工智能、芯片板块表现亮眼。',
                    'source': '证券时报',
                    'url': 'https://k.sina.com.cn/article_7857201856_1d45362c001902timk.html',
                    'timestamp': datetime.now().isoformat(),
                    'isNew': True
                }
            ],
            'culture': [
                {
                    'id': 'cul_001',
                    'title': '【故宫】数字文物库访问量破千万',
                    'summary': '故宫博物院数字文物库持续受热捧，高清数字影像访问量突破千万。',
                    'source': '北京日报',
                    'url': 'https://cj.sina.com.cn/articles/view/1645705403/v621778bb02001fh9m',
                    'timestamp': datetime.now().isoformat(),
                    'isNew': True
                }
            ],
            'policy': [
                {
                    'id': 'pol_001',
                    'title': '【国务院】发布数字经济发展规划',
                    'summary': '国务院印发数字经济发展规划，明确未来五年数字经济发展目标和重点任务。',
                    'source': '新华社',
                    'url': '#',
                    'timestamp': datetime.now().isoformat(),
                    'isNew': True
                }
            ]
        }
        
        if category:
            return mock_news.get(category, [])
        return mock_news
    
    def check_updates(self, last_check_time):
        """检查是否有更新"""
        # 模拟返回更新数据
        updates = []
        all_news = self.get_latest_news()
        
        for category, news_list in all_news.items():
            for news in news_list:
                if news.get('isNew'):
                    updates.append({
                        'category': category,
                        'news': news
                    })
        
        return updates

# 初始化服务
news_service = NewsUpdaterService()

@app.route('/api/news', methods=['GET'])
def get_news():
    """获取新闻列表"""
    category = request.args.get('category')
    limit = request.args.get('limit', 5, type=int)
    
    news = news_service.get_latest_news(category, limit)
    return jsonify({
        'status': 'success',
        'data': news,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/news/update', methods=['GET'])
def check_updates():
    """检查新闻更新"""
    last_check = request.args.get('last_check')
    updates = news_service.check_updates(last_check)
    
    return jsonify({
        'status': 'success',
        'hasUpdates': len(updates) > 0,
        'updateCount': len(updates),
        'data': updates,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/news/categories', methods=['GET'])
def get_categories():
    """获取新闻分类"""
    return jsonify({
        'status': 'success',
        'data': [
            {'id': 'ai', 'name': 'AI与科技', 'icon': '🤖'},
            {'id': 'business', 'name': '电商与商业', 'icon': '🛒'},
            {'id': 'finance', 'name': '金融', 'icon': '💰'},
            {'id': 'culture', 'name': '文创与文旅', 'icon': '🎨'},
            {'id': 'policy', 'name': '政策与行业', 'icon': '📋'}
        ]
    })

@app.route('/api/status', methods=['GET'])
def get_status():
    """获取服务状态"""
    return jsonify({
        'status': 'running',
        'version': '2.0.0',
        'lastUpdate': news_service.last_update,
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print('🚀 新闻自动更新服务已启动')
    print('📡 API地址: http://localhost:5000')
    app.run(host='0.0.0.0', port=5000, debug=True)
