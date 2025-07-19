"""
音頻處理服務 - 基於桌面版 threading_bata4.py 改寫
"""

import numpy as np
import librosa
import soundfile as sf
import io
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

class AudioProcessor:
    def __init__(self, target_sample_rate: int = 8000):
        """
        初始化音頻處理器
        
        Args:
            target_sample_rate: 目標採樣率
        """
        self.target_sample_rate = target_sample_rate
        
        logger.info(f"音頻處理器初始化: target_sample_rate={target_sample_rate}")
    
    def resample_audio(self, audio_data: np.ndarray, original_sr: int) -> np.ndarray:
        """
        重新採樣音頻 (基於桌面版 resample 函數)
        
        Args:
            audio_data: 原始音頻數據
            original_sr: 原始採樣率
            
        Returns:
            重新採樣後的音頻數據
        """
        try:
            if original_sr == self.target_sample_rate:
                return audio_data
            
            # 基於桌面版 threading_bata4.py 的 resample 函數
            # y_8k = librosa.resample(y, sr, 8000)
            resampled_audio = librosa.resample(
                audio_data, 
                orig_sr=original_sr, 
                target_sr=self.target_sample_rate
            )
            
            logger.debug(f"音頻重採樣: {original_sr}Hz -> {self.target_sample_rate}Hz")
            
            return resampled_audio
            
        except Exception as e:
            logger.error(f"音頻重採樣失敗: {str(e)}")
            raise RuntimeError(f"音頻重採樣失敗: {str(e)}")
    
    def normalize_audio(self, audio_data: np.ndarray) -> np.ndarray:
        """
        正規化音頻數據到 [-1, 1] 範圍
        
        Args:
            audio_data: 音頻數據
            
        Returns:
            正規化後的音頻數據
        """
        try:
            # 避免除零錯誤
            max_val = np.max(np.abs(audio_data))
            if max_val == 0:
                return audio_data
            
            # 正規化到 [-1, 1]
            normalized = audio_data / max_val
            
            return normalized.astype(np.float32)
            
        except Exception as e:
            logger.error(f"音頻正規化失敗: {str(e)}")
            raise RuntimeError(f"音頻正規化失敗: {str(e)}")
    
    def process_uploaded_audio(self, audio_bytes: bytes) -> np.ndarray:
        """
        處理上傳的音頻檔案
        
        Args:
            audio_bytes: 音頻檔案的二進制數據
            
        Returns:
            處理後的音頻數據 (float32, 目標採樣率)
        """
        try:
            # 使用 soundfile 讀取音頻數據
            audio_data, sample_rate = sf.read(io.BytesIO(audio_bytes))
            
            logger.info(f"上傳音頻: 採樣率={sample_rate}, 長度={len(audio_data)}, 類型={audio_data.dtype}")
            
            # 如果是立體聲，轉換為單聲道
            if len(audio_data.shape) > 1:
                audio_data = np.mean(audio_data, axis=1)
                logger.debug("立體聲轉換為單聲道")
            
            # 重新採樣
            if sample_rate != self.target_sample_rate:
                audio_data = self.resample_audio(audio_data, sample_rate)
            
            # 正規化
            audio_data = self.normalize_audio(audio_data)
            
            return audio_data
            
        except Exception as e:
            logger.error(f"處理上傳音頻失敗: {str(e)}")
            raise RuntimeError(f"處理上傳音頻失敗: {str(e)}")
    
    def process_stream_audio(self, audio_int16: np.ndarray) -> np.ndarray:
        """
        處理串流音頻數據 (來自前端 WebSocket)
        
        Args:
            audio_int16: Int16 格式的音頻數據
            
        Returns:
            處理後的 float32 音頻數據
        """
        try:
            # 轉換 Int16 到 Float32 (-1.0 到 1.0)
            audio_float = audio_int16.astype(np.float32) / 32767.0
            
            # 確保在有效範圍內
            audio_float = np.clip(audio_float, -1.0, 1.0)
            
            logger.debug(f"串流音頻處理: 長度={len(audio_float)}, 範圍=[{np.min(audio_float):.3f}, {np.max(audio_float):.3f}]")
            
            return audio_float
            
        except Exception as e:
            logger.error(f"處理串流音頻失敗: {str(e)}")
            raise RuntimeError(f"處理串流音頻失敗: {str(e)}")
    
    def validate_audio_length(self, audio_data: np.ndarray, min_length: int = 1000) -> bool:
        """
        驗證音頻長度是否足夠
        
        Args:
            audio_data: 音頻數據
            min_length: 最小長度 (樣本數)
            
        Returns:
            是否有效
        """
        return len(audio_data) >= min_length
    
    def get_audio_info(self, audio_data: np.ndarray) -> dict:
        """
        獲取音頻資訊
        
        Args:
            audio_data: 音頻數據
            
        Returns:
            音頻資訊字典
        """
        return {
            "length": len(audio_data),
            "duration": len(audio_data) / self.target_sample_rate,
            "sample_rate": self.target_sample_rate,
            "dtype": str(audio_data.dtype),
            "min_value": float(np.min(audio_data)),
            "max_value": float(np.max(audio_data)),
            "mean_value": float(np.mean(audio_data))
        }