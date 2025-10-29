# 🏭 工业时序异常检测系统

完整的工业时间序列异常检测解决方案，包含后端检测引擎、RESTful API 服务器和实时可视化前端。

## ✨ 特性

### 异常检测算法
- **Z-Score检测**: 基于标准差的统计方法
- **IQR检测**: 四分位距离群点检测
- **MAD检测**: 中位数绝对偏差检测
- **EWMA检测**: 指数加权移动平均检测
- **集成检测**: 多算法投票机制，提高准确率

### 系统功能
- ⚡ 实时异常检测与推送（WebSocket）
- 📊 实时数据可视化（Chart.js）
- 🎯 单点和批量检测API
- 📈 统计信息与历史记录
- 🔄 数据模拟生成器
- 🎨 现代化响应式UI

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /workspace/industrial_anomaly_detection
pip install -r requirements.txt
```

### 2. 启动服务器

```bash
python api_server.py
```

服务器将在 `http://localhost:5000` 启动

### 3. 打开前端

浏览器访问: `http://localhost:5000`

## 📡 API端点

### 实时检测
```bash
# 单点检测
curl -X POST http://localhost:5000/api/detect \
  -H "Content-Type: application/json" \
  -d '{"timestamp": 1234567890.0, "value": 42.5}'

# 批量检测
curl -X POST http://localhost:5000/api/batch_detect \
  -H "Content-Type: application/json" \
  -d '{"data": [{"timestamp": 1234567890.0, "value": 42.5}, ...]}'
```

### 统计与历史
```bash
# 获取统计信息
curl http://localhost:5000/api/statistics

# 获取历史数据
curl http://localhost:5000/api/history?limit=100
```

### 模拟控制
```bash
# 启动数据模拟
curl -X POST http://localhost:5000/api/simulation/start \
  -H "Content-Type: application/json" \
  -d '{"interval": 0.5}'

# 停止模拟
curl -X POST http://localhost:5000/api/simulation/stop

# 重置检测器
curl -X POST http://localhost:5000/api/reset
```

## 🔧 配置说明

### 检测器配置

编辑 `api_server.py` 中的配置:

```python
detector = IndustrialAnomalyDetector({
    'window_size': 50,           # 滑动窗口大小
    'voting_threshold': 0.5      # 集成投票阈值
})
```

### 数据生成器配置

编辑 `data_generator.py`:

```python
generator = IndustrialDataGenerator(
    base_value=100.0,              # 基准值
    noise_level=5.0,               # 噪声水平
    trend_coefficient=0.01,        # 趋势系数
    seasonal_amplitude=10.0,       # 季节性振幅
    seasonal_period=100,           # 季节性周期
    anomaly_probability=0.05,      # 异常概率（5%）
    anomaly_magnitude=30.0         # 异常幅度
)
```

## 🎯 使用场景

- **工业生产监控**: 实时监控生产线传感器数据
- **设备健康管理**: 检测设备运行异常
- **质量控制**: 识别产品质量偏差
- **预测性维护**: 提前发现潜在故障
- **能源管理**: 监控能耗异常

## 📊 检测算法详解

### Z-Score检测
基于标准差，适用于正态分布数据:
- 异常阈值: 通常为3σ
- 优点: 简单高效
- 缺点: 对极端值敏感

### IQR检测
基于四分位距，对离群点鲁棒:
- 异常范围: Q1 - 1.5×IQR ~ Q3 + 1.5×IQR
- 优点: 不受极端值影响
- 缺点: 需要足够数据点

### MAD检测
基于中位数绝对偏差:
- 修正Z-Score: 0.6745 × |x - median| / MAD
- 优点: 最鲁棒的统计方法
- 缺点: 计算稍慢

### EWMA检测
指数加权移动平均:
- 自适应阈值
- 优点: 快速响应变化
- 缺点: 需要调参

### 集成检测
多算法投票:
- 结合所有方法优点
- 投票阈值可配置
- 最佳综合性能

## 🧪 测试

### 生成测试数据
```bash
python data_generator.py
```

### Python代码测试
```python
from anomaly_detector import IndustrialAnomalyDetector

# 创建检测器
detector = IndustrialAnomalyDetector()

# 检测数据点
result = detector.process(timestamp=1234567890.0, value=105.5)

print(f"Is anomaly: {result['is_anomaly']}")
print(f"Anomaly score: {result['anomaly_score']}")
print(f"Confidence: {result['confidence']}")
```

## 📦 项目结构

```
industrial_anomaly_detection/
├── anomaly_detector.py      # 异常检测核心引擎
├── api_server.py            # Flask API服务器
├── data_generator.py        # 数据生成器
├── requirements.txt         # Python依赖
├── README.md               # 项目文档
└── static/
    └── index.html          # 前端可视化界面
```

## 🎨 前端功能

- **实时图表**: 动态展示时序数据和异常点
- **统计面板**: 显示检测统计信息
- **异常列表**: 展示最近的异常记录
- **控制面板**: 
  - 启动/停止数据模拟
  - 手动输入数据测试
  - 重置检测器
  - 调整模拟参数

## 🔒 生产部署建议

1. **安全性**:
   - 添加API认证（JWT、API Key）
   - 使用HTTPS
   - 配置CORS白名单

2. **性能**:
   - 使用Gunicorn/uWSGI
   - 添加Redis缓存
   - 数据库持久化（PostgreSQL/TimescaleDB）

3. **监控**:
   - 添加日志系统
   - 性能监控（Prometheus）
   - 错误追踪（Sentry）

4. **扩展**:
   - 容器化（Docker）
   - 负载均衡
   - 微服务架构

## 📝 技术栈

- **后端**: Python, Flask, Flask-SocketIO
- **科学计算**: NumPy, SciPy
- **前端**: HTML5, CSS3, JavaScript
- **可视化**: Chart.js
- **实时通信**: Socket.IO

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

---

**Created with ❤️ for Industrial IoT**
