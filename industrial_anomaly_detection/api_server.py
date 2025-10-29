"""
Flask API Server for Industrial Anomaly Detection
提供RESTful API和WebSocket实时推送
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import threading
import time
import json
from anomaly_detector import IndustrialAnomalyDetector
from data_generator import IndustrialDataGenerator

app = Flask(__name__, static_folder='static')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# 全局检测器实例
detector = IndustrialAnomalyDetector({
    'window_size': 50,
    'voting_threshold': 0.5
})

# 数据生成器
data_generator = IndustrialDataGenerator()

# 存储历史数据
history_data = []
MAX_HISTORY = 1000

# 实时模拟标志
simulation_running = False
simulation_thread = None


@app.route('/')
def index():
    """返回主页"""
    return send_from_directory('static', 'index.html')


@app.route('/api/detect', methods=['POST'])
def detect_anomaly():
    """
    单点异常检测API
    请求体: {"timestamp": 123456789.0, "value": 42.5}
    """
    try:
        data = request.json
        timestamp = data.get('timestamp', time.time())
        value = data.get('value')
        
        if value is None:
            return jsonify({'error': 'Missing value'}), 400
        
        result = detector.process(timestamp, value)
        
        # 存储历史
        history_data.append(result)
        if len(history_data) > MAX_HISTORY:
            history_data.pop(0)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/batch_detect', methods=['POST'])
def batch_detect():
    """
    批量异常检测API
    请求体: {"data": [{"timestamp": t1, "value": v1}, ...]}
    """
    try:
        data = request.json
        points = data.get('data', [])
        
        if not points:
            return jsonify({'error': 'No data provided'}), 400
        
        results = []
        for point in points:
            timestamp = point.get('timestamp', time.time())
            value = point.get('value')
            
            if value is not None:
                result = detector.process(timestamp, value)
                results.append(result)
                
                # 存储历史
                history_data.append(result)
                if len(history_data) > MAX_HISTORY:
                    history_data.pop(0)
        
        return jsonify({
            'results': results,
            'count': len(results)
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """获取统计信息"""
    try:
        stats = detector.get_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/history', methods=['GET'])
def get_history():
    """获取历史数据"""
    try:
        limit = request.args.get('limit', 100, type=int)
        limit = min(limit, len(history_data))
        
        return jsonify({
            'data': history_data[-limit:],
            'count': len(history_data[-limit:])
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/reset', methods=['POST'])
def reset_detector():
    """重置检测器"""
    try:
        detector.reset()
        history_data.clear()
        return jsonify({'status': 'success', 'message': 'Detector reset'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/simulation/start', methods=['POST'])
def start_simulation():
    """启动数据模拟"""
    global simulation_running, simulation_thread
    
    try:
        if simulation_running:
            return jsonify({'status': 'already_running'})
        
        config = request.json or {}
        interval = config.get('interval', 0.5)  # 秒
        
        simulation_running = True
        simulation_thread = threading.Thread(
            target=simulation_worker,
            args=(interval,),
            daemon=True
        )
        simulation_thread.start()
        
        return jsonify({'status': 'started'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/simulation/stop', methods=['POST'])
def stop_simulation():
    """停止数据模拟"""
    global simulation_running
    
    try:
        simulation_running = False
        return jsonify({'status': 'stopped'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/simulation/status', methods=['GET'])
def simulation_status():
    """获取模拟状态"""
    return jsonify({'running': simulation_running})


def simulation_worker(interval: float):
    """模拟数据生成工作线程"""
    global simulation_running
    
    print(f"Simulation started with interval {interval}s")
    
    while simulation_running:
        # 生成数据点
        timestamp, value = data_generator.generate_next()
        
        # 检测异常
        result = detector.process(timestamp, value)
        
        # 存储历史
        history_data.append(result)
        if len(history_data) > MAX_HISTORY:
            history_data.pop(0)
        
        # 通过WebSocket推送
        socketio.emit('anomaly_data', result, namespace='/')
        
        time.sleep(interval)
    
    print("Simulation stopped")


@socketio.on('connect')
def handle_connect():
    """WebSocket连接建立"""
    print('Client connected')
    emit('connection_response', {'status': 'connected'})


@socketio.on('disconnect')
def handle_disconnect():
    """WebSocket连接断开"""
    print('Client disconnected')


@socketio.on('request_history')
def handle_history_request(data):
    """请求历史数据"""
    limit = data.get('limit', 100)
    limit = min(limit, len(history_data))
    
    emit('history_data', {
        'data': history_data[-limit:],
        'count': len(history_data[-limit:])
    })


if __name__ == '__main__':
    print("=" * 60)
    print("Industrial Anomaly Detection API Server")
    print("=" * 60)
    print("API Endpoints:")
    print("  POST   /api/detect          - Single point detection")
    print("  POST   /api/batch_detect    - Batch detection")
    print("  GET    /api/statistics      - Get statistics")
    print("  GET    /api/history         - Get history data")
    print("  POST   /api/reset           - Reset detector")
    print("  POST   /api/simulation/start - Start simulation")
    print("  POST   /api/simulation/stop  - Stop simulation")
    print("  GET    /api/simulation/status - Get simulation status")
    print("=" * 60)
    print("Starting server on http://localhost:5000")
    print("=" * 60)
    
    socketio.run(app, host='0.0.0.0', port=5000, debug=True, allow_unsafe_werkzeug=True)
