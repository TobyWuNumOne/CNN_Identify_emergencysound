# CNN Emergency Sound Identification (聽障人士輔助辨識警急)

This project is designed to help people with hearing impairments identify emergency sounds using Convolutional Neural Networks (CNN). The system can detect and classify various emergency sounds such as sirens, alarms, and other warning signals.

## 功能特點 (Features)

- Real-time audio processing and visualization
- Emergency sound detection and classification
- Sound wave frequency analysis
- Dynamic audio visualization
- Multi-channel audio support
- Audio filtering capabilities
- Recording and playback functionality

## 系統需求 (System Requirements)

### 軟體需求 (Software Requirements)

- Python 3.x
- Required Python packages:
  - numpy
  - pyaudio
  - wave
  - matplotlib
  - librosa
  - tkinter

## 專案結構 (Project Structure)

```
CNN_Identify_emergencysound/
├── Toby/
│   ├── check_wav.py          # WAV file analysis tool
│   ├── confirm_the_sound.py  # Sound processing and visualization
│   ├── threading_bata3.py    # Threading implementation for audio processing
│   ├── threading_bata4.py    # Enhanced threading implementation
│   └── readme.md            # Detailed documentation for Toby directory
└── README.md                # Main project documentation
```

## 安裝說明 (Installation)

1. Clone the repository:
```bash
git clone https://github.com/TobyWuNumOne/CNN_Identify_emergencysound.git
cd CNN_Identify_emergencysound
```

2. Install required Python packages:
```bash
pip install numpy pyaudio wave matplotlib librosa tkinter
```

## 使用方法 (Usage)

### 音頻分析 (Audio Analysis)

1. 執行音頻分析工具:
```python
python Toby/check_wav.py
```
This will display audio file properties including:
- Channel count
- Sample rate
- Bit depth
- Number of frames
- Duration

### 即時音頻處理 (Real-time Audio Processing)

1. 啟動即時音頻處理:
```python
python Toby/confirm_the_sound.py
```
Features:
- Real-time audio visualization
- Frequency spectrum analysis
- Dynamic waveform display

### 音頻識別 (Sound Identification)

1. 運行音頻識別系統:
```python
python Toby/threading_bata4.py
```
The system will:
- Record audio in segments
- Process the audio for identification
- Resample the audio as needed
- Perform emergency sound classification

## 技術細節 (Technical Details)

### 音頻處理參數 (Audio Processing Parameters)

- 採樣率 (Sample Rate): 44100 Hz (default)
- 聲道數 (Channels): 支援單聲道和立體聲 (Supports mono and stereo)
- 位元深度 (Bit Depth): 支援 16/24/32 位元 (Supports 16/24/32 bit)
- 幀緩衝區大小 (Frame Buffer): 根據 fps 動態調整 (Dynamically adjusted based on fps)

### 音頻分析功能 (Audio Analysis Features)

- 時域波形顯示 (Time Domain Waveform Display)
- 頻譜分析 (Frequency Spectrum Analysis)
- 實時過濾器 (Real-time Filtering)
- 動態可視化 (Dynamic Visualization)

## 貢獻指南 (Contributing)

如果您想為專案做出貢獻，請:
1. Fork 專案
2. 創建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟一個 Pull Request

## 授權 (License)

This project is licensed under the MIT License - see the LICENSE file for details.

## 聯絡方式 (Contact)

如需協助，請開啟 Issue 或聯絡專案作者。

## 致謝 (Acknowledgments)

感謝所有為此專案做出貢獻的開發者。
