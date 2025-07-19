"""
MFCC 特徵提取服務 - 基於桌面版 mfccs_value.py 改寫
"""

import numpy as np
import librosa
import logging
from typing import Tuple, Optional

logger = logging.getLogger(__name__)

class MFCCExtractor:
    def __init__(self, n_mfcc: int = 13, target_shape: Tuple[int, int] = (13, 44)):
        """
        初始化 MFCC 提取器
        
        Args:
            n_mfcc: MFCC 係數數量
            target_shape: 目標輸出形狀 (n_mfcc, time_frames)
        """
        self.n_mfcc = n_mfcc
        self.target_shape = target_shape
        
        logger.info(f"MFCC 提取器初始化: n_mfcc={n_mfcc}, target_shape={target_shape}")
    
    def extract(self, audio_data: np.ndarray, sample_rate: int = 8000) -> np.ndarray:
        """
        提取 MFCC 特徵 (基於桌面版 displaymfccprediction 函數)
        
        Args:
            audio_data: 音頻數據 (float32 格式, -1.0 到 1.0)
            sample_rate: 採樣率
            
        Returns:
            MFCC 特徵，形狀為 (1, 13, 44, 1)
            
        Raises:
            ValueError: 音頻數據格式錯誤
            RuntimeError: MFCC 提取失敗
        """
        try:
            # 驗證輸入數據
            if not isinstance(audio_data, np.ndarray):
                raise ValueError("音頻數據必須是 numpy 數組")
            
            if len(audio_data) == 0:
                raise ValueError("音頻數據不能為空")
            
            # 確保數據類型為 float32
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
            
            # 基於桌面版邏輯進行 MFCC 提取
            # 參考: desktop/mfccs_value.py 的 displaymfccprediction 函數
            mfccs = librosa.feature.mfcc(
                y=audio_data,
                sr=sample_rate,
                n_mfcc=self.n_mfcc,
                dct_type=2,
                norm="ortho"
            )
            
            # 正規化 MFCC (基於桌面版)
            normalized_mfcc = librosa.util.normalize(mfccs)  # -1~1
            
            # 調整到目標形狀 (基於桌面版)
            # normalized_mfcc = np.resize(normalized_mfcc, (13, 44))
            normalized_mfcc = np.resize(normalized_mfcc, self.target_shape)
            
            # 重新調整形狀以符合模型輸入要求
            # mfcc_reshaped = normalized_mfcc.reshape(1, 13, 44, 1)
            mfcc_reshaped = normalized_mfcc.reshape(1, self.target_shape[0], self.target_shape[1], 1)
            
            logger.debug(f"MFCC 提取成功: 輸入長度={len(audio_data)}, 輸出形狀={mfcc_reshaped.shape}")
            
            return mfcc_reshaped
            
        except Exception as e:
            logger.error(f"MFCC 提取失敗: {str(e)}")
            raise RuntimeError(f"MFCC 提取失敗: {str(e)}")
    
    def extract_from_file(self, file_path: str) -> np.ndarray:
        """
        從音頻檔案提取 MFCC 特徵
        
        Args:
            file_path: 音頻檔案路徑
            
        Returns:
            MFCC 特徵數組
        """
        try:
            # 載入音頻檔案
            audio_data, sample_rate = librosa.load(file_path, sr=None)
            
            logger.info(f"載入音頻檔案: {file_path}, 採樣率: {sample_rate}, 長度: {len(audio_data)}")
            
            # 提取 MFCC
            return self.extract(audio_data, sample_rate)
            
        except Exception as e:
            logger.error(f"從檔案提取 MFCC 失敗: {str(e)}")
            raise RuntimeError(f"從檔案提取 MFCC 失敗: {str(e)}")
    
    def get_config(self) -> dict:
        """獲取提取器配置"""
        return {
            "n_mfcc": self.n_mfcc,
            "target_shape": self.target_shape,
            "output_shape": (1, self.target_shape[0], self.target_shape[1], 1)
        }