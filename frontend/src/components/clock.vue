<template>
  <div class="clock-container">
    <div id="clock">
      <div v-for="(digits, groupIndex) in digitStructure" :key="groupIndex" class="digit-group">
        <div v-for="(digitList, digitIndex) in digits" :key="digitIndex" class="digit">
          <div v-for="n in digitList" :key="n" class="digit-number"
            :class="{ bright: isActiveDigit(groupIndex, digitIndex, n) }">
            {{ n }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, onBeforeUnmount } from 'vue';

export default {
  name: 'Clock',
  setup() {
    const digitStructure = [
      [[0, 1, 2], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]], // 小时
      [[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]], // 分钟
      [[0, 1, 2, 3, 4, 5], [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]]  // 秒
    ];

    const currentTime = ref([0, 0, 0, 0, 0, 0]); // 存储时分秒的每一位数字
    let animationFrameId = null;

    const updateTime = () => {
      const date = new Date();
      const timeString = [
        date.getHours(),
        date.getMinutes(),
        date.getSeconds()
      ].map(n => `0${n}`.slice(-2)).join('');

      currentTime.value = timeString.split('').map(Number);
    };

    const isActiveDigit = (groupIndex, digitIndex, n) => {
      const timeIndex = groupIndex * 2 + digitIndex;
      return currentTime.value[timeIndex] === n;
    };

    onMounted(() => {
      updateTime();
      animationFrameId = setInterval(updateTime, 1000);
    });

    onBeforeUnmount(() => {
      if (animationFrameId) {
        clearInterval(animationFrameId);
      }
    });

    return {
      digitStructure,
      currentTime,
      isActiveDigit
    };
  }
};
</script>

<style scoped>
@keyframes gradientShift {
  0% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }

  100% {
    background-position: 0% 50%;
  }
}

.clock-container {
  font: 100%/1.5 sans-serif;
  color: black;
  text-align: center;
  overflow: hidden;
  background: linear-gradient(-45deg, #fcbad3, #b5ead7, #c7ceea, #ffdac1);
  background-size: 400% 400%;
  animation: gradientShift 15s ease infinite;
  width: 100%;
  height: 300px;
  display: flex;
  justify-content: center;
  align-items: center;
  border-radius: 8px;
  border-style: solid;
  border-color: var(--border);
  box-shadow: 2px 2px #000;
}

#clock {
  font-size: 16px;
  width: 100%;
  height: 100%;
  font-family: 'Orbitron', sans-serif;

}

.digit-group {
  display: inline-block;
  height: 100%;
}

.digit-group:not(:last-child):after {
  content: ":";
  font-size: 36px;
}

.digit {
  display: inline-block;
  width: 25px;
  height: 160px;
}

.digit .digit-number {
  color: rgba(255, 255, 255, 0.5);
  transform: rotate(-90deg);
  transition: font-size 200ms, transform 350ms, color 150ms;
}

.digit .digit-number.bright {
  color: inherit;
  font-size: 36px;
  transform: rotate(0deg);
}
</style>