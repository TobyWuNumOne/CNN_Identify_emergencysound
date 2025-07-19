import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import AudioRecorder from '../views/AudioRecorder.vue'
import FileUpload from '../views/FileUpload.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/recorder',
    name: 'AudioRecorder',
    component: AudioRecorder
  },
  {
    path: '/upload',
    name: 'FileUpload',
    component: FileUpload
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router