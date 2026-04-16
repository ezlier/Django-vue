<template>
  <div class="clock-container">
    <h1 class="digital-clock">{{ timeString }}</h1>
    <h4 class="date">{{ getFormatDate() }}</h4>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { Solar } from 'lunar-javascript';

function getFormatDate() {
  const now = new Date();
  const solar = Solar.fromDate(now);
  const lunar = solar.getLunar();

  // 公历：4月4日
  const solarText = `${solar.getMonth()}月${solar.getDay()}日`;

  // 星期：星期六
  const weekArr = ['日', '一', '二', '三', '四', '五', '六'];
  const weekText = `星期${weekArr[now.getDay()]}`;

  // 农历：二月十七（强制显示“月”）
  const monthStr = lunar.getMonthInChinese()+"月"; // 二月
  const dayStr = lunar.getDayInChinese();     // 十七
  const lunarText = monthStr + dayStr;

  // 最终拼接
  return `${solarText} ${weekText} ${lunarText}`;
}

// 测试
console.log(getFormatDate());


// 响应式变量，用于存储格式化后的时间字符串
const timeString = ref('00:00');
let timerId = null;

// 格式化时间逻辑
const updateClock = () => {
  const now = new Date();
  const hour = String(now.getHours()).padStart(2, '0');
  const min = String(now.getMinutes()).padStart(2, '0');
  
  timeString.value = `-${hour}:${min}-`;
};

onMounted(() => {
  // 组件挂载时启动，立即更新一次，然后每秒更新一次
  updateClock();
  timerId = setInterval(updateClock, 1000);
});

onUnmounted(() => {
  // 组件卸载时记得清理掉，防止后台持续运行
  if (timerId) {
    clearInterval(timerId);
  }
});
</script>

<style scoped>
.clock-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-radius: var(--border-radius);
  background: var(--bg-color);
  border: var(--border);
  box-shadow: var(--box-shadow);
}

.digital-clock {
  font-family: 文楷;
  font-size: 50px;
  /* 渐变色文字逻辑 */
  background: linear-gradient(135deg, #14ffe9, #ffeb3b, #ff00e0);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  
  /* 辉光效果 */
  text-shadow: 0 0 4px rgba(255, 255, 255, 0.7);
  
  /* 颜色循环动画 */
  animation: timeColor 3s linear infinite;
}

.date {
  font-family: 文楷;

  background: linear-gradient(135deg, #14ffe9, #ffeb3b, #ff00e0);
  background-clip: text;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  
  /* 辉光效果 */
  text-shadow: 0 0 4px rgba(255, 255, 255, 0.7);
  
  /* 颜色循环动画 */
  animation: timeColor 3s linear infinite;
}


@keyframes timeColor {
  to {
    filter: hue-rotate(360deg);
  }
}
</style>