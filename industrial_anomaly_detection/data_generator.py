"""
Industrial Time Series Data Generator
生成带有异常的工业时序数据
"""

import numpy as np
import time
from typing import Tuple


class IndustrialDataGenerator:
    """工业传感器数据生成器"""
    
    def __init__(
        self,
        base_value: float = 100.0,
        noise_level: float = 5.0,
        trend_coefficient: float = 0.01,
        seasonal_amplitude: float = 10.0,
        seasonal_period: int = 100,
        anomaly_probability: float = 0.05,
        anomaly_magnitude: float = 30.0
    ):
        """
        Args:
            base_value: 基准值
            noise_level: 噪声水平
            trend_coefficient: 趋势系数
            seasonal_amplitude: 季节性振幅
            seasonal_period: 季节性周期
            anomaly_probability: 异常发生概率
            anomaly_magnitude: 异常幅度
        """
        self.base_value = base_value
        self.noise_level = noise_level
        self.trend_coefficient = trend_coefficient
        self.seasonal_amplitude = seasonal_amplitude
        self.seasonal_period = seasonal_period
        self.anomaly_probability = anomaly_probability
        self.anomaly_magnitude = anomaly_magnitude
        
        self.counter = 0
        self.start_time = time.time()
    
    def generate_next(self) -> Tuple[float, float]:
        """
        生成下一个数据点
        Returns: (timestamp, value)
        """
        timestamp = time.time()
        
        # 基础值
        value = self.base_value
        
        # 添加趋势
        trend = self.trend_coefficient * self.counter
        value += trend
        
        # 添加季节性
        seasonal = self.seasonal_amplitude * np.sin(
            2 * np.pi * self.counter / self.seasonal_period
        )
        value += seasonal
        
        # 添加随机噪声
        noise = np.random.normal(0, self.noise_level)
        value += noise
        
        # 随机添加异常
        if np.random.random() < self.anomaly_probability:
            anomaly_type = np.random.choice(['spike', 'drop', 'shift'])
            
            if anomaly_type == 'spike':
                value += self.anomaly_magnitude
            elif anomaly_type == 'drop':
                value -= self.anomaly_magnitude
            else:  # shift
                value += np.random.choice([-1, 1]) * self.anomaly_magnitude * 0.5
        
        self.counter += 1
        
        return timestamp, value
    
    def generate_batch(self, n: int) -> Tuple[np.ndarray, np.ndarray]:
        """
        生成一批数据
        Args:
            n: 数据点数量
        Returns: (timestamps, values)
        """
        timestamps = []
        values = []
        
        for _ in range(n):
            t, v = self.generate_next()
            timestamps.append(t)
            values.append(v)
        
        return np.array(timestamps), np.array(values)
    
    def reset(self):
        """重置生成器"""
        self.counter = 0
        self.start_time = time.time()


def generate_sample_dataset(n_points: int = 1000, save_path: str = None) -> dict:
    """
    生成示例数据集
    Args:
        n_points: 数据点数量
        save_path: 保存路径（可选）
    Returns: 包含时间戳和值的字典
    """
    generator = IndustrialDataGenerator()
    timestamps, values = generator.generate_batch(n_points)
    
    dataset = {
        'timestamps': timestamps.tolist(),
        'values': values.tolist(),
        'metadata': {
            'n_points': n_points,
            'base_value': generator.base_value,
            'noise_level': generator.noise_level,
            'anomaly_probability': generator.anomaly_probability
        }
    }
    
    if save_path:
        import json
        with open(save_path, 'w') as f:
            json.dump(dataset, f, indent=2)
        print(f"Dataset saved to {save_path}")
    
    return dataset


if __name__ == '__main__':
    # 测试数据生成器
    print("Testing Data Generator...")
    
    generator = IndustrialDataGenerator()
    
    print("\nGenerating 10 sample points:")
    for i in range(10):
        timestamp, value = generator.generate_next()
        print(f"Point {i+1}: timestamp={timestamp:.2f}, value={value:.2f}")
    
    # 生成示例数据集
    print("\nGenerating sample dataset...")
    dataset = generate_sample_dataset(1000, 'sample_data.json')
    print(f"Generated {len(dataset['values'])} data points")
