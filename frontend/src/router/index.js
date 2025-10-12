import { createRouter, createWebHistory } from 'vue-router'
import Layout from '@/views/Layout/index.vue'
import Home from '@/views/Home/index.vue'
import File from '@/views/File/index.vue'
import About from '@/views/About/index.vue'



const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/',
      component:Layout,
      children:[
          {
            path:'',
            component:Home
          },
          {
            path:'file',
            component:File
          },
          {
            path:'about',
            component:About
          }
      ]
    }
  ],
})

export default router
