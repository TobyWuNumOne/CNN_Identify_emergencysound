<template>
  <div class="home">
    <div class="hero-section">
      <h2>選擇識別方式</h2>
      <p>您可以選擇即時錄音識別或上傳音頻檔案進行分析</p>
    </div>
    
    <div class="options-grid">
      <div class="option-card">
        <div class="option-icon">🎤</div>
        <h3>即時錄音識別</h3>
        <p>使用麥克風進行即時聲音識別，適合持續監控環境聲音</p>
        <router-link to="/recorder" class="btn btn-primary">
          開始錄音
        </router-link>
      </div>
      
      <div class="option-card">
        <div class="option-icon">📁</div>
        <h3>音頻檔案上傳</h3>
        <p>上傳現有的音頻檔案進行分析，支援 WAV、MP3 等格式</p>
        <router-link to="/upload" class="btn btn-primary">
          上傳檔案
        </router-link>
      </div>
    </div>
    
    <div class="info-section">
      <div class="card">
        <h3>🎯 系統功能</h3>
        <ul>
          <li><strong>救護車聲音識別</strong> - 檢測救護車警報聲</li>
          <li><strong>警車聲音識別</strong> - 檢測警車警報聲</li>
          <li><strong>環境聲音過濾</strong> - 過濾日常環境噪音</li>
          <li><strong>即時視覺化</strong> - 顯示音頻波形和頻譜</li>
        </ul>
      </div>
      
      <div class="card">
        <h3>📊 系統狀態</h3>
        <div class="status-grid">
          <div class="status-item">
            <span class="status-label">後端連線:</span>
            <span :class="['status-value', backendStatus ? 'status-online' : 'status-offline']">
              {{ backendStatus ? '正常' : '離線' }}
            </span>
          </div>
          <div class="status-item">
            <span class="status-label">AI 模型:</span>
            <span :class="['status-value', modelStatus ? 'status-online' : 'status-offline']">
              {{ modelStatus ? '已載入' : '未載入' }}
            </span>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue'
import { checkBackendHealth } from '../services/apiService'

export default {
  name: 'Home',
  setup() {
    const backendStatus = ref(false)
    const modelStatus = ref(false)
    
    const checkSystemStatus = async () => {
      try {
        const health = await checkBackendHealth()
        backendStatus.value = health.status === 'healthy'
        modelStatus.value = health.model_loaded || false
      } catch (error) {
        console.error('系統狀態檢查失敗:', error)
        backendStatus.value = false
        modelStatus.value = false
      }
    }
    
    onMounted(() => {
      checkSystemStatus()
      // 每30秒檢查一次狀態
      setInterval(checkSystemStatus, 30000)
    })
    
    return {
      backendStatus,
      modelStatus
    }
  }
}
</script>

<style scoped>
.hero-section {
  text-align: center;
  margin-bottom: 3rem;
}

.hero-section h2 {
  font-size: 2.5rem;
  color: #333;
  margin-bottom: 1rem;
}

.hero-section p {
  font-size: 1.2rem;
  color: #666;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  margin-bottom: 3rem;
}

.option-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 8px 30px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
}

.option-card:hover {
  transform: translateY(-5px);
}

.option-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.option-card h3 {
  color: #333;
  margin-bottom: 1rem;
}

.option-card p {
  color: #666;
  margin-bottom: 2rem;
  line-height: 1.6;
}

.info-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.info-section ul {
  list-style: none;
  padding: 0;
}

.info-section li {
  padding: 0.5rem 0;
  border-bottom: 1px solid #eee;
}

.info-section li:last-child {
  border-bottom: none;
}

.status-grid {
  display: grid;
  gap: 1rem;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.5rem 0;
}

.status-label {
  font-weight: 600;
  color: #333;
}

.status-value {
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
}

.status-online {
  background: #d4edda;
  color: #155724;
}

.status-offline {
  background: #f8d7da;
  color: #721c24;
}
</style>