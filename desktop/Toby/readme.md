# Toby 資料夾說明

本資料夾包含多個 Python 腳本，主要用於緊急聲音識別（如警報聲、救護車聲等）相關的音訊特徵處理、模型測試，以及圖形介面展示。以下為各檔案簡要說明：

> ⚠️ 注意：此清單僅包含前 10 個檔案，可能未涵蓋全部內容，完整檔案請至 [Toby 目錄](https://github.com/TobyWuNumOne/CNN_Identify_emergencysound/tree/37b37ccd950a16a56d1538cfa8627d0ac19c2b33/Toby) 查看。

## 目錄結構與檔案說明

- `__pycache__/`
  - Python 編譯後快取檔案，無需手動操作。

- `check_wav.py`
  - 用於檢查或處理 wav 音訊檔案的腳本。

- `confirm_the_sound.py`
  - 進行聲音確認與判斷的主程式，可能與模型推論、分類有關。

- `mfccs_value.py`
  - 用來計算音訊特徵（MFCCs，梅爾頻率倒譜係數）的腳本。

- `test.ipynb`
  - Jupyter Notebook，用於互動式測試或記錄處理流程。

- `test_gui.py`
  - 提供圖形化介面的測試腳本，方便用戶操作與展示。

- `test_threading.py`
  - 測試多執行緒運作，提升處理效率的腳本。

- `test_threading_bata2.py`
  - 多執行緒測試的另一版本，可能含有不同優化或嘗試。

- `testimg.py`
  - 用於測試或處理影像（如 spectrogram）相關功能的腳本。

- `test連續mfcc.py`
  - 針對連續音訊資料計算 MFCC 特徵的腳本，適用於長時間錄音分析。

- `threading_bata3.py`, `threading_bata4.py`
  - 多執行緒相關的實驗版本。

- `trance_sound.py`
  - 處理或轉換聲音資料的腳本。

## 使用建議

- 建議優先閱讀 `confirm_the_sound.py`、`mfccs_value.py` 及 `test_gui.py`，這些是核心邏輯與互動介面。
- 若需進行批次音訊測試，可參考多執行緒系列腳本。
- 若需進行特徵分析或模型驗證，可利用 Notebook 或 `testimg.py`。

## 進階說明

- 相關腳本可能需依賴特定的 Python 套件（如 `librosa`, `numpy`, `tkinter` 等），請依需求安裝。
- 若有更多檔案或需求，請至 [Toby 目錄](https://github.com/TobyWuNumOne/CNN_Identify_emergencysound/tree/37b37ccd950a16a56d1538cfa8627d0ac19c2b33/Toby) 查看完整內容。

---

如需協助，請開啟 Issue 或聯絡專案作者。
