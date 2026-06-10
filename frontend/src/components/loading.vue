<template>
    <div class="loading">
        <div class="loading_mask_1" id="loading_mask_1"></div>
        <div class="loading_mask_2" id="loading_mask_2"></div>
        <div class="loading_mask_3" id="loading_mask_3"></div>
        <div class="loading_mask_4" id="loading_mask_4"></div>
        <div class="main_window" :class="{ fadeOut: isHide }">
            <div class="text-content">
                <button class="loading_text" @click="hide">{{ tip }}</button>
                <!-- 打字机效果容器 -->
                <div class="typewriter-container" ref="typewriterRef">
                    <div class="type-line" v-for="(line, index) in typeLines" :key="index">
                        <span class="typed-text" :data-text="line"></span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref, defineExpose } from 'vue';

const typeLines = ref([]);
// DOM引用
const typewriterRef = ref(null);

const isHide = ref(false);

const tip = ref('Connecting...');

const typingFinished = ref(false); // 打字机是否打完
const resourceLoaded = ref(false); // 资源是否加载完

// 生成随机IP 127.xx.xx.xx
function generateRandomIP() {
  const part1 = Math.floor(Math.random() * 256);
  const part2 = Math.floor(Math.random() * 256);
  const part3 = Math.floor(Math.random() * 256);
  const part4 = Math.floor(Math.random() * 256);
  return `${part1}.${part2}.${part3}.${part4}`;
}

// 获取当前日期 格式：MM月DD日
function getCurrentDate() {
  const date = new Date();
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  return `${month}月${day}日`;
}

// 初始化打字机文字
function initTypeText() {
  typeLines.value = [
    'Unknown connection',
    getCurrentDate(),
    generateRandomIP(),
    'Unknown user'
  ];
}

// 执行打字机动画
function startTypewriter() {
  if (!typewriterRef.value) return;
  const textElements = typewriterRef.value.querySelectorAll('.typed-text');
  let finishedCount = 0;
  textElements.forEach((el, index) => {
    const text = el.dataset.text;
    let i = 0;
    // 逐行延迟，依次打字
    setTimeout(() => {
      const typing = setInterval(() => {
        el.textContent += text.charAt(i);
        i++;
        if (i > text.length) {
          clearInterval(typing);
          finishedCount++;
          // 所有行都打完了
          if (finishedCount === textElements.length) {
            typingFinished.value = true;
            checkCanHide(); // 检查是否可以关闭
          }
        }
      }, 100); // 打字速度
    }, index * 1000); // 每行间隔时间
  });
}

function open() {
    const loading_mask_1 = document.getElementById('loading_mask_1');
    const loading_mask_2 = document.getElementById('loading_mask_2');
    loading_mask_1.classList.add('active');
    loading_mask_2.classList.add('active');
} 

function hide() {
  tip.value = 'OK!';
  // 触发文字淡出
  isHide.value = true;

  // 延迟执行遮罩关闭，让淡出效果完整播放
  setTimeout(() => {
    const loading_mask_1 = document.getElementById('loading_mask_1');
    const loading_mask_2 = document.getElementById('loading_mask_2');
    const loading_mask_3 = document.getElementById('loading_mask_3');
    const loading_mask_4 = document.getElementById('loading_mask_4');
    
    loading_mask_1.classList.add('widthhide');
    loading_mask_2.classList.add('widthhide');
    loading_mask_3.classList.add('heighthide');
    loading_mask_4.classList.add('heighthide');
  }, 500); // 淡出动画时长 500ms
}

function checkCanHide() {
  if (typingFinished.value && resourceLoaded.value) {
    hide();
  }
}

function setResourceLoaded() {
  resourceLoaded.value = true;
  checkCanHide();
}

onMounted(() => {
    setTimeout(() => {
    open();
}, 1000);

    setTimeout(() => {
    initTypeText();
    // 等待DOM渲染完成
    setTimeout(() => {
      startTypewriter();
    }, 50);
  }, 2000);
})

defineExpose({
  setResourceLoaded
});
</script>

<style scoped>
.loading-container {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    
}

.loading_mask_1 {
    position: absolute;
    top: 0;
    left: 0;
    width: 40vw;
    height: 100%;
    background-color: #1a1a1a;
    z-index: 200;
    animation: width 1s ease-in ;
}

.loading_mask_2 {
    position: absolute;
    top: 0;
    right: 0;
    width: 40vw;
    height: 100%;
    background-color: #1a1a1a;
    z-index: 200;
    animation: width 1s ease-in ;
}

.loading_mask_3 {
    position: absolute;
    bottom: 0;
    left: 0;
    width: 100vw;
    height: 20vh;
    background-color: #1a1a1a;
    z-index: 201;    
}

.loading_mask_4 {
    position: absolute;
    top: 0;
    left: 25vw;
    width: 50vw;
    height: 20vh;
    background-color: #1a1a1a;
    z-index: 201;
    
    animation: start 1s ease-in-out ;
}

.loading_mask_1.active,
.loading_mask_2.active {
    width: 25vw;
    animation: widthAnim 1s ease-in-out ;
}


.loading_mask_1.widthhide,
.loading_mask_2.widthhide {
    width: 0;
    animation: hideAnim 1s ease-in-out ;
}

.loading_mask_3.heighthide,
.loading_mask_4.heighthide {
    left: 0;
    width: 100vw;
    height: 0;
    animation: heightAnim 1s ease-in ;
}



.main_window {
    position: absolute;
    top: 20vh;
    left: 25vw;
    width: 50vw;
    height: 60vh;
    z-index: 199;
    background-color: rgba(0, 0, 0, 0.9);    
    transition: opacity 0.5s ease;
}

.main_window.fadeOut {
  opacity: 0;
  pointer-events: none;
}

/* 文字容器：统一控制淡出 */
.text-content {
  transition: opacity 0.5s ease;
  opacity: 1;
}
/* 淡出动画类 */
.text-content.fadeOut {
  opacity: 0;
  pointer-events: none;
}

.loading_text {
  position: absolute;
  right: 20px;
  bottom: 20px;
  display: block;
  text-align: center;
  color: #AEBDDD ;
  transition: all 0.3s ease-in-out;
  border: none;
  outline: none;
  background: none;
  padding: 10px;
}

.loading_text::before,
.loading_text::after {
  content: "";
	position: absolute;
	width: 20px;
	height: 20px;
	border: 2px solid #AEBDDD;
	transition: all 0.3s ease-in-out 0.3s;
  box-sizing: border-box;
}

.loading_text::before {
    top: 0;
	left: 0;
	/* 删除左边的伪元素的右和下边框 */
	border-right: 0;
	border-bottom: 0;
}

.loading_text::after {
    right: 0;
	bottom: 0;
	/* 删除右边的伪元素的上边和左边的边框 */
	border-top: 0;
	border-left: 0;
}

.loading_text:hover {
  background-color: #AEBDDD;
	color: #000;
  box-shadow: 0 0 20px #AEBDDD;
}

.loading_text:hover::before,
.loading_text:hover::after {
    width: 100%;
	height: 100%;
	transition-delay: 0s;
}

@keyframes start {
    0% {
        height: 80vh;   
        border-bottom: 1px solid #fff;
    }
    100% {
        height: 20vh;   
        border-bottom: 1px solid #fff;
    }
}

@keyframes widthAnim {
  from { width: 40vw; }
  to   { width: 25vw; }    
}

@keyframes heightAnim {
  from { height: 20vh; }
  to   { height: 0; }    
}

@keyframes hideAnim {
  from { width: 25vw; }
  to   { width: 0; }    
}

.typewriter-container {
  position: absolute;
  bottom: 20px;
  left: 20px;
  color: #AEBDDD;
  font-family: "Courier New", monospace;
  font-size: 16px;
  line-height: 1.8;
}

/* 打字行样式 */
.type-line {
  white-space: nowrap;
  overflow: hidden;
}
</style>