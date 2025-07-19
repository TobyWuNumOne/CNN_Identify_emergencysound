<template>
  <div id="app">
    <header class="app-header">
      <h1>🚨 緊急聲音識別系統</h1>
      <p>基於 CNN 的即時聲音識別 - 幫助聽障人士識別警急聲音</p>
    </header>
    
    <main class="app-main">
      <router-view />
    </main>
    
    <footer class="app-footer">
      <p>&copy; 2024 Emergency Sound Detection System</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style scoped>
.app-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 2rem;
  text-align: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.app-header h1 {
  margin: 0 0 0.5rem 0;
  font-size: 2.5rem;
  font-weight: 700;
}

.app-header p {
  margin: 0;
  font-size: 1.1rem;
  opacity: 0.9;
}

.app-main {
  min-height: calc(100vh - 200px);
  padding: 2rem;
}

.app-footer {
  background: #f8f9fa;
  padding: 1rem;
  text-align: center;
  border-top: 1px solid #e9ecef;
  color: #6c757d;
}
</style>