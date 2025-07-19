"""
模型服務 - 基於桌面版 model_prediction.py 和 mfccs_value.py 改寫
"""

import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
import logging
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)

class ModelService:
    def __init__(self, model_path: str = "../../shared/models/simple-train-nb30&25"):
        """
        初始化模型服務
        
        Args:
            model_path: 模型檔案路徑
        """
        self.model_path = model_path
        self.model: Optional[keras.Model] = None
        self.labels = ["ambulance", "environment", "police"]
        self.is_model_loaded = False
        
        # 載入模型
        self._load_model()
    
    def _load_model(self) -> None:
        """載入 CNN 模型"""
        try:
            # 檢查模型檔案是否存在
            if not os.path.exists(self.model_path):
                logger.error(f"模型檔案不存在: {self.model_path}")
                return
            
            # 載入模型 (基於桌面版邏輯)
            self.model = keras.models.load_model(self.model_path)
            self.is_model_loaded = True
            
            logger.info(f"模型載入成功: {self.model_path}")
            logger.info(f"模型輸入形狀: {self.model.input_shape}")
            logger.info(f"模型輸出形狀: {self.model.output_shape}")
            
        except Exception as e:
            logger.error(f"模型載入失敗: {str(e)}")
            self.is_model_loaded = False
    
    def is_loaded(self) -> bool:
        """檢查模型是否已載入"""
        return self.is_model_loaded and self.model is not None
    
    def predict(self, mfcc_features: np.ndarray) -> np.ndarray:
        """
        進行模型預測
        
        Args:
            mfcc_features: MFCC 特徵，形狀應為 (1, 13, 44, 1)
            
        Returns:
            預測結果數組
            
        Raises:
            RuntimeError: 模型未載入或預測失敗
        """
        if not self.is_loaded():
            raise RuntimeError("模型未載入，無法進行預測")
        
        try:
            # 檢查輸入形狀
            expected_shape = (1, 13, 44, 1)
            if mfcc_features.shape != expected_shape:
                logger.warning(f"輸入形狀不匹配: {mfcc_features.shape}, 期望: {expected_shape}")
                # 嘗試重新調整形狀
                mfcc_features = mfcc_features.reshape(expected_shape)
            
            # 進行預測 (基於桌面版 displaymfccprediction 函數)
            prediction = self.model.predict(mfcc_features, verbose=0)
            
            # 返回第一個預測結果
            return prediction[0]
            
        except Exception as e:
            logger.error(f"模型預測失敗: {str(e)}")
            raise RuntimeError(f"模型預測失敗: {str(e)}")
    
    def check_emergency(self, prediction: np.ndarray, threshold: float = 0.7) -> Dict:
        """
        檢查是否為緊急情況 (基於桌面版邏輯)
        
        Args:
            prediction: 模型預測結果
            threshold: 信心度閾值
            
        Returns:
            包含警報資訊的字典
        """
        try:
            # 找到最高信心度的類別
            max_idx = np.argmax(prediction)
            confidence = float(prediction[max_idx])
            predicted_label = self.labels[max_idx]
            
            # 基於桌面版 mfccs_value.py 的邏輯
            # if prediction == "police" or prediction == "ambulance":
            is_emergency = (
                predicted_label in ["ambulance", "police"] and 
                confidence > threshold
            )
            
            return {
                "is_emergency": is_emergency,
                "type": predicted_label if is_emergency else None,
                "confidence": confidence,
                "all_predictions": {
                    label: float(prediction[i]) 
                    for i, label in enumerate(self.labels)
                }
            }
            
        except Exception as e:
            logger.error(f"緊急情況檢查失敗: {str(e)}")
            return {
                "is_emergency": False,
                "type": None,
                "confidence": 0.0,
                "error": str(e)
            }
    
    def get_labels(self) -> List[str]:
        """獲取標籤列表"""
        return self.labels.copy()
    
    def get_model_info(self) -> Dict:
        """獲取模型資訊"""
        if not self.is_loaded():
            return {"status": "not_loaded"}
        
        return {
            "status": "loaded",
            "model_path": self.model_path,
            "input_shape": self.model.input_shape,
            "output_shape": self.model.output_shape,
            "labels": self.labels,
            "total_params": self.model.count_params()
        }