<template>
  <div class="header">
    <!-- 新增：左右布局容器 -->
    <div class="hero-wrapper" :class="{'fade-in': showContent}">
      <!-- 左侧：自我介绍 + 网站名 -->
      <div class="intro-box">
        <div class="loader">
          <div :data-glitch="WebSetting.WebSettingList.web_name" class="glitch">
            {{ WebSetting.WebSettingList.web_name }}
          </div>
        </div>
      </div>

      <!-- 右侧：头像 -->
      <div class="avatar-box">
        <img class="avatar" :src="avatarUrl" alt="avatar" />
      </div>
    </div>

    <!-- 底部打字机标语（之前加的） -->
    <div class="footer-slogan">
      <span class="sub-content">{{ displayedText }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, defineExpose, computed } from 'vue'
import { useWebSettingStore } from '@/stores/WebSetting'

const WebSetting = useWebSettingStore()

const showContent = ref(false)

const texts = [
  '不必匆忙。不必火花四溅。不必成为别人，只需做自己。',
  '如果你能在浪费时间中获得乐趣，就不算浪费时间。',
  '给我点赞喵！为什么没人给我点赞喵！是我喵的不够好吗喵！不给我点赞就捅似你们喵！捅似你们喵！',
  '钱没有，工作也没有，自由也没有，几把人生。',
  '立春天 风渐暖 伊人一去不复返。',
  '知而不行，只是未知。',
  '为君沉醉又何妨，只怕酒醒时候断人肠。',
  '时间是存在者的时间。',
  '犹豫就会败北。',
  '雪珠声声入耳，一如古柏，我身依然故我。',
  '不可视他人所得为我之失。',
  '命运之剑有两道剑锋，其中之一是你。',
  '年少的时候，你拥有的时间似乎无穷无尽，一月似一年，一年似一生。',
  '有人倒下，也要继续前行。',
  '萤火虫也喜欢黑暗的地方呀。黑暗的角落里也有美好的事物，但我们总得先去看了才能发现。',
  '希望你可以记住我，记住我这样活过，这样在你身边呆过。',
  '生活是一场即兴表演，值得庆幸的是我们总是有所感受，并且将一直感受下去。',
  'Hello World!!!',
  'for those who can after',
  '云色轻还重 风光淡又浓 向春入二月 花色影重重。',
  '最远的旅行，是从自己的身体到自己的心，是从一个人的心到另一个人的心。',
  '秩序织就经纬 因果结成铁网。',
  '万物依轨运行 静默直至终章。',
  '人本过客来无处，休说故里在何方。',
  '随遇而安无不可，人间到处有花香。',
  '如果你把每一天都当作生命中最后一天去生活，那么总有一天你会发现自己是正确的。',
  '你能从圆心画出多少半径，生活就有多少种方式。',
  '人们总说时间可以改变很多事，但事实上必须由你自己做出那些改变。',
  '年年乐事，华灯竞处，人月圆时。',
  '最长的路也有尽头，最黑暗的夜晚也会迎接清晨。',
  '我会走得很远，远过这些山丘，远过这些大海，直到靠近星星。',
  '生活永远是，也仅仅是我们现在经历的这一刻。',
  '全力以赴度过今天，自然就能看清楚明天。',
  '你并非孤立无援，也绝非无关紧要。就像叶子是树的一部分，雨滴是海洋的一部分，你是世间万物的一部分。',
  '对世间的一切事物报以虚无的态度其实是轻松的，真正困难的是如何勇敢地介入其中。',
  // ... 其他语录
]

const displayedText = ref('')
let timer = null
let isDeleting = false
let currentTextIndex = Math.floor(Math.random() * texts.length)
let charIndex = 0

const startFadeIn = () => {
  setTimeout(() => {
    showContent.value = true
  }, 200)
}

const getRandomTextIndex = () => {
  if (texts.length <= 1) return 0
  
  let newIndex
  do {
    newIndex = Math.floor(Math.random() * texts.length)
  } while (newIndex === currentTextIndex)
  
  return newIndex
}

const typeWriter = () => {
  const currentFullText = texts[currentTextIndex]
  
  if (isDeleting) {
    // 退格删除：截取长度递减
    displayedText.value = currentFullText.substring(0, charIndex - 1)
    charIndex--
  } else {
    // 正常打字：截取长度递增
    displayedText.value = currentFullText.substring(0, charIndex + 1)
    charIndex++
  }

  // 速度逻辑
  let typeSpeed = isDeleting ? 50 : 150 // 删除时速度快一点

  // 状态转换判断
  if (!isDeleting && charIndex === currentFullText.length) {
    // 打字完成了，停顿 3 秒再开始删除
    typeSpeed = 3000
    isDeleting = true
  } else if (isDeleting && charIndex === 0) {
    // 删除干净了，随机换下一句
    isDeleting = false
    currentTextIndex = getRandomTextIndex()
    typeSpeed = 500
  }

  timer = setTimeout(typeWriter, typeSpeed)
}

const avatarUrl = computed(() => {
  const baseUrl = WebSetting.WebSettingList?.name_avatar
  if (!baseUrl) return ''
  
  // 添加时间戳参数
  const timestamp = new Date().getTime()
  // 检查URL是否已有参数
  const separator = baseUrl.includes('?') ? '&' : '?'
  return `${baseUrl}${separator}t=${timestamp}`
})

onMounted(() => {
  typeWriter()
  setTimeout(() => {
    startFadeIn()
  }, 1000)
})

onUnmounted(() => {
  clearTimeout(timer)
})

defineExpose({
  startFadeIn
})
</script>

<style scoped>
.header {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
  position: relative; /* 必须加 */
}

.hero-wrapper {
  display: flex;
  align-items: center;
  gap: 40px;
  opacity: 0;
  transition: opacity 1s ease;
}

.hero-wrapper.fade-in {
  opacity: 1;
}

.intro-box {
  text-align: left;
}
.intro-text {
  font-size: 1.6rem;
  color: #fff;
  margin-bottom: 10px;
}


/* 头像圆形 */
.avatar-box {
  flex-shrink: 0;
}
.avatar {
  width: 160px;
  height: 160px;
  border-radius: 50%;
  object-fit: cover;
  box-shadow: 0 0 15px 5px rgba(255, 0, 0, 0.2);
}

.blog-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.blog-content {
  font-size: 4rem;
  font-weight: bold;
  color: whitesmoke;
}



.sub-content {
  font-size: 1.5rem;
  color: whitesmoke;
  font-style: italic;
  position: relative;
  white-space: pre-wrap;
  text-shadow: 0 0 4px rgba(255, 255, 255, 0.7);
  mix-blend-mode: difference
}

/* 光标效果 */
.sub-content::after {
  content: "|";
  margin-left: 5px;
  animation: blink 0.7s infinite;
  color: rgb(142, 140, 216);
  font-weight: bold;
}

.glitch {
  position: relative;
  font-size: 4rem;
  font-weight: bold;
  line-height: 1.2;
  color: #fff;
  letter-spacing: 5px;
  z-index: 1;
  animation: shift 1s ease-in-out infinite alternate;
}

.glitch:before,
.glitch:after {
  display: block;
  content: attr(data-glitch);
  position: absolute;
  top: 0;
  left: 0;
  opacity: 0.8;
}

.glitch:before {
  animation: glitch 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) both infinite;
  color: #fcbad3;
  z-index: -1;
}

.glitch:after {
  animation: glitch 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94) reverse both infinite;
  color: #a8d8ea;
  z-index: -2;
}

.footer-slogan {
  position: absolute;
  bottom: 25px;
  left: 50%;
  transform: translateX(-50%);
  width: 90%;
  text-align: center;
}

/* 保留你原来的光标、字体样式 */
.sub-content {
  font-size: 1.5rem;
  color: whitesmoke;
  font-style: italic;
  position: relative;
  white-space: pre-wrap;
  text-shadow: 0 0 4px rgba(255, 255, 255, 0.7);
  mix-blend-mode: difference
}
.sub-content::after {
  content: "|";
  margin-left: 5px;
  animation: blink 0.7s infinite;
  color: rgb(142, 140, 216);
  font-weight: bold;
}

/* 让 header 相对定位，否则底部定位会失效 */
.header {
  position: relative;
}

@keyframes glitch {
  0% {
    transform: translate(0);
  }

  20% {
    transform: translate(-3px, 3px);
  }

  40% {
    transform: translate(-3px, -3px);
  }

  60% {
    transform: translate(3px, 3px);
  }

  80% {
    transform: translate(3px, -3px);
  }

  to {
    transform: translate(0);
  }
}



@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

@media (max-width: 720px) {
  .blog-content { font-size: 2rem; }
  .sub-content { font-size: 1.1rem; }
}
</style>