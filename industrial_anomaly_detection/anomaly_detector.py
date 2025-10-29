"""
Industrial Time Series Anomaly Detection Module
支持多种异常检测算法
"""

import numpy as np
from scipy import stats
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from collections import deque
import warnings
warnings.filterwarnings('ignore')


@dataclass
class AnomalyResult:
    """异常检测结果"""
    timestamp: float
    value: float
    is_anomaly: bool
    anomaly_score: float
    method: str
    confidence: float
    threshold: float


class StatisticalDetector:
    """基于统计方法的异常检测器"""
    
    def __init__(self, window_size: int = 50, n_sigma: float = 3.0):
        self.window_size = window_size
        self.n_sigma = n_sigma
        self.history = deque(maxlen=window_size)
    
    def detect(self, value: float) -> Tuple[bool, float, float]:
        """
        使用Z-score检测异常
        Returns: (is_anomaly, anomaly_score, threshold)
        """
        self.history.append(value)
        
        if len(self.history) < 10:
            return False, 0.0, self.n_sigma
        
        mean = np.mean(self.history)
        std = np.std(self.history)
        
        if std < 1e-6:
            return False, 0.0, self.n_sigma
        
        z_score = abs((value - mean) / std)
        is_anomaly = z_score > self.n_sigma
        
        return is_anomaly, z_score, self.n_sigma


class IQRDetector:
    """基于四分位距的异常检测器"""
    
    def __init__(self, window_size: int = 50, iqr_multiplier: float = 1.5):
        self.window_size = window_size
        self.iqr_multiplier = iqr_multiplier
        self.history = deque(maxlen=window_size)
    
    def detect(self, value: float) -> Tuple[bool, float, float]:
        """
        使用IQR方法检测异常
        Returns: (is_anomaly, anomaly_score, threshold)
        """
        self.history.append(value)
        
        if len(self.history) < 10:
            return False, 0.0, 0.0
        
        q1 = np.percentile(self.history, 25)
        q3 = np.percentile(self.history, 75)
        iqr = q3 - q1
        
        lower_bound = q1 - self.iqr_multiplier * iqr
        upper_bound = q3 + self.iqr_multiplier * iqr
        
        is_anomaly = value < lower_bound or value > upper_bound
        
        if iqr > 0:
            if value < lower_bound:
                anomaly_score = abs((value - lower_bound) / iqr)
            elif value > upper_bound:
                anomaly_score = abs((value - upper_bound) / iqr)
            else:
                anomaly_score = 0.0
        else:
            anomaly_score = 0.0
        
        return is_anomaly, anomaly_score, self.iqr_multiplier


class MADDetector:
    """基于中位数绝对偏差的异常检测器"""
    
    def __init__(self, window_size: int = 50, threshold: float = 3.5):
        self.window_size = window_size
        self.threshold = threshold
        self.history = deque(maxlen=window_size)
    
    def detect(self, value: float) -> Tuple[bool, float, float]:
        """
        使用MAD (Median Absolute Deviation) 检测异常
        Returns: (is_anomaly, anomaly_score, threshold)
        """
        self.history.append(value)
        
        if len(self.history) < 10:
            return False, 0.0, self.threshold
        
        median = np.median(self.history)
        mad = np.median([abs(x - median) for x in self.history])
        
        if mad < 1e-6:
            return False, 0.0, self.threshold
        
        modified_z_score = 0.6745 * abs(value - median) / mad
        is_anomaly = modified_z_score > self.threshold
        
        return is_anomaly, modified_z_score, self.threshold


class EWMADetector:
    """基于指数加权移动平均的异常检测器"""
    
    def __init__(self, alpha: float = 0.3, n_sigma: float = 3.0):
        self.alpha = alpha
        self.n_sigma = n_sigma
        self.ewma = None
        self.ewma_var = None
        self.initialized = False
    
    def detect(self, value: float) -> Tuple[bool, float, float]:
        """
        使用EWMA检测异常
        Returns: (is_anomaly, anomaly_score, threshold)
        """
        if not self.initialized:
            self.ewma = value
            self.ewma_var = 0.0
            self.initialized = True
            return False, 0.0, self.n_sigma
        
        # 更新EWMA
        prev_ewma = self.ewma
        self.ewma = self.alpha * value + (1 - self.alpha) * self.ewma
        
        # 更新方差
        error = value - prev_ewma
        self.ewma_var = self.alpha * (error ** 2) + (1 - self.alpha) * self.ewma_var
        
        std = np.sqrt(self.ewma_var)
        
        if std < 1e-6:
            return False, 0.0, self.n_sigma
        
        z_score = abs(value - self.ewma) / std
        is_anomaly = z_score > self.n_sigma
        
        return is_anomaly, z_score, self.n_sigma


class EnsembleDetector:
    """集成多个检测器的异常检测系统"""
    
    def __init__(
        self,
        window_size: int = 50,
        voting_threshold: float = 0.5,
        enable_zscore: bool = True,
        enable_iqr: bool = True,
        enable_mad: bool = True,
        enable_ewma: bool = True
    ):
        self.voting_threshold = voting_threshold
        self.detectors = {}
        
        if enable_zscore:
            self.detectors['zscore'] = StatisticalDetector(window_size)
        if enable_iqr:
            self.detectors['iqr'] = IQRDetector(window_size)
        if enable_mad:
            self.detectors['mad'] = MADDetector(window_size)
        if enable_ewma:
            self.detectors['ewma'] = EWMADetector()
    
    def detect(self, timestamp: float, value: float) -> AnomalyResult:
        """
        使用所有检测器进行投票判断异常
        Returns: AnomalyResult对象
        """
        votes = []
        scores = []
        details = {}
        
        for name, detector in self.detectors.items():
            is_anomaly, score, threshold = detector.detect(value)
            votes.append(1 if is_anomaly else 0)
            scores.append(score)
            details[name] = {
                'is_anomaly': is_anomaly,
                'score': score,
                'threshold': threshold
            }
        
        # 投票决定
        vote_ratio = np.mean(votes)
        is_anomaly = vote_ratio >= self.voting_threshold
        
        # 综合异常分数
        avg_score = np.mean(scores)
        
        # 置信度
        confidence = vote_ratio if is_anomaly else (1 - vote_ratio)
        
        result = AnomalyResult(
            timestamp=timestamp,
            value=value,
            is_anomaly=is_anomaly,
            anomaly_score=avg_score,
            method='ensemble',
            confidence=confidence,
            threshold=self.voting_threshold
        )
        
        return result


class IndustrialAnomalyDetector:
    """工业时序异常检测主类"""
    
    def __init__(self, config: Optional[Dict] = None):
        if config is None:
            config = {}
        
        self.window_size = config.get('window_size', 50)
        self.voting_threshold = config.get('voting_threshold', 0.5)
        
        self.detector = EnsembleDetector(
            window_size=self.window_size,
            voting_threshold=self.voting_threshold
        )
        
        self.anomaly_count = 0
        self.total_count = 0
        self.recent_anomalies = deque(maxlen=100)
    
    def process(self, timestamp: float, value: float) -> Dict:
        """
        处理单个时序数据点
        Returns: 包含检测结果的字典
        """
        result = self.detector.detect(timestamp, value)
        
        self.total_count += 1
        if result.is_anomaly:
            self.anomaly_count += 1
            self.recent_anomalies.append({
                'timestamp': timestamp,
                'value': value,
                'score': result.anomaly_score
            })
        
        return {
            'timestamp': result.timestamp,
            'value': result.value,
            'is_anomaly': result.is_anomaly,
            'anomaly_score': round(result.anomaly_score, 4),
            'confidence': round(result.confidence, 4),
            'method': result.method,
            'anomaly_rate': round(self.anomaly_count / max(self.total_count, 1), 4)
        }
    
    def get_statistics(self) -> Dict:
        """获取统计信息"""
        return {
            'total_count': self.total_count,
            'anomaly_count': self.anomaly_count,
            'anomaly_rate': round(self.anomaly_count / max(self.total_count, 1), 4),
            'recent_anomalies_count': len(self.recent_anomalies)
        }
    
    def reset(self):
        """重置检测器"""
        self.detector = EnsembleDetector(
            window_size=self.window_size,
            voting_threshold=self.voting_threshold
        )
        self.anomaly_count = 0
        self.total_count = 0
        self.recent_anomalies.clear()
