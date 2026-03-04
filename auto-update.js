// auto-update.js - 新闻网站自动更新功能
// 第二阶段开发内容

class NewsAutoUpdater {
    constructor() {
        this.lastUpdateTime = null;
        this.updateInterval = 3600000; // 默认1小时检查一次更新
        this.newsSources = {
            ai: [
                { name: '新浪AI', url: 'https://finance.sina.com.cn/tech/', selector: '.news-item' },
                { name: '36氪AI', url: 'https://36kr.com/search/articles/AI', selector: '.article-item' }
            ],
            business: [
                { name: '新浪财经', url: 'https://finance.sina.com.cn/', selector: '.news-item' },
                { name: '财联社', url: 'https://www.cls.cn/', selector: '.news-item' }
            ],
            finance: [
                { name: '东方财富', url: 'https://finance.eastmoney.com/', selector: '.news-item' },
                { name: '证券时报', url: 'https://stcn.com/', selector: '.news-item' }
            ],
            culture: [
                { name: '文旅中国', url: 'https://www.wenlv.cn/', selector: '.news-item' },
                { name: '新浪文创', url: 'https://finance.sina.com.cn/culture/', selector: '.news-item' }
            ],
            policy: [
                { name: '中国政府网', url: 'http://www.gov.cn/', selector: '.news-item' },
                { name: '发改委', url: 'https://www.ndrc.gov.cn/', selector: '.news-item' }
            ]
        };
    }

    // 初始化自动更新
    init() {
        console.log('🔄 自动更新功能已启动');
        this.checkForUpdates();
        setInterval(() => this.checkForUpdates(), this.updateInterval);
        
        // 显示上次更新时间
        this.displayLastUpdateTime();
    }

    // 检查更新
    async checkForUpdates() {
        console.log('🔍 检查新闻更新...');
        const now = new Date();
        
        try {
            // 模拟获取最新新闻（实际使用时需要后端API支持）
            const updates = await this.fetchLatestNews();
            if (updates && updates.length > 0) {
                this.updateNewsDisplay(updates);
                this.lastUpdateTime = now;
                this.saveUpdateTime();
                this.showUpdateNotification(updates.length);
            }
        } catch (error) {
            console.error('❌ 检查更新失败:', error);
        }
    }

    // 获取最新新闻（模拟）
    async fetchLatestNews() {
        // 实际使用时，这里应该调用后端API
        // 由于浏览器CORS限制，需要后端代理
        return new Promise((resolve) => {
            // 模拟返回更新数据
            setTimeout(() => {
                resolve([]); // 空数组表示暂无更新
            }, 1000);
        });
    }

    // 更新新闻显示
    updateNewsDisplay(updates) {
        updates.forEach(update => {
            const card = this.findNewsCard(update.category, update.title);
            if (card) {
                this.highlightUpdate(card);
            }
        });
    }

    // 查找新闻卡片
    findNewsCard(category, title) {
        const cards = document.querySelectorAll(`[data-category="${category}"]`);
        return Array.from(cards).find(card => {
            const cardTitle = card.querySelector('.news-title');
            return cardTitle && cardTitle.textContent.includes(title);
        });
    }

    // 高亮更新
    highlightUpdate(card) {
        card.classList.add('news-updated');
        setTimeout(() => {
            card.classList.remove('news-updated');
        }, 5000);
    }

    // 显示更新通知
    showUpdateNotification(count) {
        const notification = document.createElement('div');
        notification.className = 'update-notification';
        notification.innerHTML = `
            <span>🎉 已更新 ${count} 条新闻</span>
            <button onclick="this.parentElement.remove()">×</button>
        `;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    // 保存更新时间
    saveUpdateTime() {
        localStorage.setItem('lastNewsUpdate', this.lastUpdateTime.toISOString());
    }

    // 显示上次更新时间
    displayLastUpdateTime() {
        const lastUpdate = localStorage.getItem('lastNewsUpdate');
        if (lastUpdate) {
            const date = new Date(lastUpdate);
            console.log('📅 上次更新时间:', date.toLocaleString());
        }
    }

    // 手动刷新
    manualRefresh() {
        console.log('🔄 手动刷新新闻...');
        this.checkForUpdates();
    }

    // 设置更新间隔
    setUpdateInterval(minutes) {
        this.updateInterval = minutes * 60 * 1000;
        console.log(`⏱️ 更新间隔已设置为 ${minutes} 分钟`);
    }
}

// 页面加载完成后初始化
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.newsUpdater = new NewsAutoUpdater();
        window.newsUpdater.init();
    });
} else {
    window.newsUpdater = new NewsAutoUpdater();
    window.newsUpdater.init();
}
