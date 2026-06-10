<script setup>
import { ref, onMounted, onUnmounted } from 'vue';

const planeRef = ref(null);
let deg = 0, ex = 0, ey = 0, vx = 100, vy = 100, count = 0;
let animationFrameId = null;

// 鼠标移动事件处理函数
const handleMouseMove = (e) => {
  if (!planeRef.value) return;
  // 计算相对于飞机中心的偏差
  ex = e.clientX - planeRef.value.offsetLeft - planeRef.value.clientWidth / 2;
  ey = e.clientY - planeRef.value.offsetTop - planeRef.value.clientHeight / 2;
  
  // 弧度转角度
  deg = Math.atan2(ey, ex) * (180 / Math.PI) + 45;
  count = 0;
};

const draw = () => {
  if (planeRef.value) {
    planeRef.value.style.transform = `rotate(${deg}deg)`;
    
    if (count < 100) {
      vx += ex / 100;
      vy += ey / 100; // 修复了这里的 xy 错误
    }
    
    planeRef.value.style.left = vx + 'px';
    planeRef.value.style.top = vy + 'px';
    count++;
  }
  animationFrameId = requestAnimationFrame(draw);
};

onMounted(() => {
  window.addEventListener('mousemove', handleMouseMove);
  draw();
});

onUnmounted(() => {
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
  }
  window.removeEventListener('mousemove', handleMouseMove);
});
</script>

<template>
  <div class="not-found">
    
    <div id="wifi-loader">
        <svg class="circle-outer" viewBox="0 0 86 86">
            <circle class="back" cx="43" cy="43" r="40"></circle>
            <circle class="front" cx="43" cy="43" r="40"></circle>
            <circle class="new" cx="43" cy="43" r="40"></circle>
        </svg>
        <svg class="circle-middle" viewBox="0 0 60 60">
            <circle class="back" cx="30" cy="30" r="27"></circle>
            <circle class="front" cx="30" cy="30" r="27"></circle>
        </svg>
        <svg class="circle-inner" viewBox="0 0 34 34">
            <circle class="back" cx="17" cy="17" r="14"></circle>
            <circle class="front" cx="17" cy="17" r="14"></circle>
        </svg>
        <div class="text" data-text="404"></div>
    </div>

    <button class="learn-more">
      <span class="circle" aria-hidden="true">
      <span class="icon arrow"></span>
      </span>
      <span class="button-text" @click="$router.push('/')">回到首页</span>
    </button>

    <div class="square">
        <ul>
          <li></li>
          <li></li>
          <li></li>
          <li></li>
          <li></li>
        </ul>
      </div>
      <div class="circle">
        <ul>
          <li></li>
          <li></li>
          <li></li>
          <li></li>
          <li></li>
        </ul>
      </div>
      
  </div>
  <div id="plane" ref="planeRef">
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" width="40" height="40">
      <path fill="currentColor" d="m64 448 832-320-128 704-446.08-243.328L832 192 242.816 545.472zm256 512V657.024L512 768z"></path>
    </svg>
  </div>
</template>

<style scoped>
/* From Uiverse.io by cssbuttons-io */ 
button {
 position: relative;
 display: inline-block;
 cursor: pointer;
 outline: none;
 border: 0;
 vertical-align: middle;
 text-decoration: none;
 background: transparent;
 padding: 0;
 font-size: inherit;
 font-family: inherit;
 margin-top: 50px;
}

button.learn-more {
 width: 12rem;
 height: auto;
}

button.learn-more .circle {
 transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
 position: relative;
 display: block;
 margin: 0;
 width: 3rem;
 height: 3rem;
 background: #282936;
 border-radius: 1.625rem;
}

button.learn-more .circle .icon {
 transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
 position: absolute;
 top: 0;
 bottom: 0;
 margin: auto;
 background: #fff;
}

button.learn-more .circle .icon.arrow {
 transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
 left: 0.625rem;
 width: 1.125rem;
 height: 0.125rem;
 background: none;
}

button.learn-more .circle .icon.arrow::before {
 position: absolute;
 content: "";
 top: -0.29rem;
 right: 0.0625rem;
 width: 0.625rem;
 height: 0.625rem;
 border-top: 0.125rem solid #fff;
 border-right: 0.125rem solid #fff;
 transform: rotate(45deg);
}

button.learn-more .button-text {
 transition: all 0.45s cubic-bezier(0.65, 0, 0.076, 1);
 position: absolute;
 top: 0;
 left: 0;
 right: 0;
 bottom: 0;
 padding: 0.75rem 0;
 margin: 0 0 0 1.85rem;
 color: #282936;
 font-weight: 700;
 line-height: 1.6;
 text-align: center;
 text-transform: uppercase;
}

button:hover .circle {
 width: 100%;
}

button:hover .circle .icon.arrow {
 background: #fff;
 transform: translate(1rem, 0);
}

button:hover .button-text {
 color: #fff;
}

#plane {
  color: #333;
  position: absolute;
  z-index: 999; /* 确保在背景之上 */
  pointer-events: none; /* 防止遮挡鼠标事件 */
  transition: transform 0.2s ease; /* 让旋转更平滑 */
}

.not-found {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  text-align: center;
  flex-direction: column;
  background: linear-gradient(200deg, #e3c5eb, #a9c1ed);
}


@keyframes textColor {
  to {
    filter: hue-rotate(360deg);
  }
}


ul li{
  position: absolute;
  border: 1px solid whitesmoke;
  background-color: white;
  width: 30px;
  height: 30px;
  list-style: none;
  opacity: 0;
}

.square li {
  top: 40vh;
  left: 60vw;
  animation: square 10s linear infinite;
}

.square li:nth-child(2){
  top: 80vh;
  left: 10vw;
  animation-delay: 2s;
}

.square li:nth-child(3){
  top: 80vh;
  left: 85vw;
  animation-delay: 5s;
}

.square li:nth-child(4){
  top: 10vh;
  left: 70vw;
  animation-delay: 8s;
}

.square li:nth-child(5){
  top: 10vh;
  left: 10vw;
  animation-delay: 11s;
}

.circle li{
  bottom: 0;
  left: 15vw;
  animation: circle 10s linear infinite;
}

.circle li:nth-child(2){
  left: 25vw;
  animation-delay: 2s;
}

.circle li:nth-child(3){
  left: 55vw;
  animation-delay: 5s;
}

.circle li:nth-child(4){
  left: 75vw;
  animation-delay: 6s;
}

.circle li:nth-child(5){
  left: 45vw;
  animation-delay: 10s;
}

#wifi-loader {
  --background: #62abff;
  --front-color: #4f29f0;
  --back-color: #c3c8de;
  --text-color: #414856;
  width: 64px;
  height: 64px;
  border-radius: 50px;
  position: relative;
  display: flex;
  justify-content: center;
  align-items: center;
}

#wifi-loader svg {
  position: absolute;
  display: flex;
  justify-content: center;
  align-items: center;
}

#wifi-loader svg circle {
  position: absolute;
  fill: none;
  stroke-width: 6px;
  stroke-linecap: round;
  stroke-linejoin: round;
  transform: rotate(-100deg);
  transform-origin: center;
}

#wifi-loader svg circle.back {
  stroke: var(--back-color);
}

#wifi-loader svg circle.front {
  stroke: var(--front-color);
}

#wifi-loader svg.circle-outer {
  height: 86px;
  width: 86px;
}

#wifi-loader svg.circle-outer circle {
  stroke-dasharray: 62.75 188.25;
}

#wifi-loader svg.circle-outer circle.back {
  animation: circle-outer135 1.8s ease infinite 0.3s;
}

#wifi-loader svg.circle-outer circle.front {
  animation: circle-outer135 1.8s ease infinite 0.15s;
}

#wifi-loader svg.circle-middle {
  height: 60px;
  width: 60px;
}

#wifi-loader svg.circle-middle circle {
  stroke-dasharray: 42.5 127.5;
}

#wifi-loader svg.circle-middle circle.back {
  animation: circle-middle6123 1.8s ease infinite 0.25s;
}

#wifi-loader svg.circle-middle circle.front {
  animation: circle-middle6123 1.8s ease infinite 0.1s;
}

#wifi-loader svg.circle-inner {
  height: 34px;
  width: 34px;
}

#wifi-loader svg.circle-inner circle {
  stroke-dasharray: 22 66;
}

#wifi-loader svg.circle-inner circle.back {
  animation: circle-inner162 1.8s ease infinite 0.2s;
}

#wifi-loader svg.circle-inner circle.front {
  animation: circle-inner162 1.8s ease infinite 0.05s;
}

#wifi-loader .text {
  position: absolute;
  bottom: -40px;
  display: flex;
  justify-content: center;
  align-items: center;
  text-transform: lowercase;
  font-weight: 500;
  font-size: 14px;
  letter-spacing: 0.2px;
}

#wifi-loader .text::before, #wifi-loader .text::after {
  content: attr(data-text);
}

#wifi-loader .text::before {
  color: var(--text-color);
}

#wifi-loader .text::after {
  color: var(--front-color);
  animation: text-animation76 3.6s ease infinite;
  position: absolute;
  left: 0;
}

@keyframes circle-outer135 {
  0% {
    stroke-dashoffset: 25;
  }

  25% {
    stroke-dashoffset: 0;
  }

  65% {
    stroke-dashoffset: 301;
  }

  80% {
    stroke-dashoffset: 276;
  }

  100% {
    stroke-dashoffset: 276;
  }
}

@keyframes circle-middle6123 {
  0% {
    stroke-dashoffset: 17;
  }

  25% {
    stroke-dashoffset: 0;
  }

  65% {
    stroke-dashoffset: 204;
  }

  80% {
    stroke-dashoffset: 187;
  }

  100% {
    stroke-dashoffset: 187;
  }
}

@keyframes circle-inner162 {
  0% {
    stroke-dashoffset: 9;
  }

  25% {
    stroke-dashoffset: 0;
  }

  65% {
    stroke-dashoffset: 106;
  }

  80% {
    stroke-dashoffset: 97;
  }

  100% {
    stroke-dashoffset: 97;
  }
}

@keyframes text-animation76 {
  0% {
    clip-path: inset(0 100% 0 0);
  }

  50% {
    clip-path: inset(0);
  }

  100% {
    clip-path: inset(0 0 0 100%);
  }
}
 

@keyframes square{
  0%{
    transform: scale(0) rotateY(0deg);
    opacity: 1;
  }
  100%{
    transform: scale(5) rotateY(1000deg);
    opacity: 0;
  }
}
@keyframes circle{
  0%{
    transform: scale(0) rotateY(0deg);
    opacity: 1;
    bottom: 0;
    border-radius: 0;
  }
  100%{
    transform: scale(5) rotateY(1000deg);
    opacity: 0;
    bottom: 90vh;
    border-radius: 50%;
  }
}
</style>