<template>
  <div class="header">
    <div class="blog-container">
      <div class="blog-content">
        Ezria-blog
      </div>
      <div class="sub-content" ref="subContent">
        {{ displayedText }}
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';

export default {
  setup() {
    const subContent = ref(null);
    const texts = [
      '不必匆忙。不必火花四溅。不必成为别人，只需做自己。',
      "如果你能在浪费时间中获得乐趣，就不算浪费时间。",
      "给我点赞喵！为什么没人给我点赞喵！是我喵的不够好吗喵！不给我点赞就捅似你们喵！捅似你们喵！",
      "钱没有，工作也没有，自由也没有，几把人生。",
      "立春天 风渐暖 伊人一去不复返。",
      "知而不行，只是未知。",
      "为君沉醉又何妨，只怕酒醒时候断人肠。",
      "时间是存在者的时间。",
      "犹豫就会败北。",
      "雪珠声声入耳，一如古柏，我身依然故我。",
      "不可视他人所得为我之失。",
      "命运之剑有两道剑锋，其中之一是你",
      "年少的时候，你拥有的时间似乎无穷无尽，一月似一年，一年似一生",
      "有人倒下，也要继续前行",
      "萤火虫也喜欢黑暗的地方呀。黑暗的角落里也有美好的事物，但我们总得先去看了才能发现",
      "希望你可以记住我，记住我这样活过，这样在你身边呆过",
      "生活是一场即兴表演，值得庆幸的是我们总是有所感受，并且将一直感受下去",
      "Hello World!!!",
      "for those who can after",
      "云色轻还重 风光淡又浓 向春入二月 花色影重重",
      "最远的旅行，是从自己的身体到自己的心，是从一个人的心到另一个人的心。"

    ];
    const displayedText = ref('');
    const currentText = ref('');
    let typingInterval = null;

    const getRandomText = () => {
      const randomIndex = Math.floor(Math.random() * texts.length);
      return texts[randomIndex];
    };

    const typeWriter = () => {
      displayedText.value = ' ';
      
      currentText.value = getRandomText();
      let i = 0;
      
      if (typingInterval) clearInterval(typingInterval);
      
      typingInterval = setInterval(() => {
        if (i < currentText.value.length) {
          displayedText.value += currentText.value.charAt(i);
          i++;
        } else {
          clearInterval(typingInterval);
          setTimeout(() => {
            typeWriter();
          }, 3000);
        }
      }, 150);
    };

    onMounted(() => {
      typeWriter();
    });

    return {
      subContent,
      displayedText
    };
  }
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: center;
  padding: 20px;
  
}

.blog-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
}

.blog-content {
  font-size: 2rem;
  font-weight: bold;
  color: #8785a2;
}

.sub-content {
  padding: 12px 20px;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
  background-color: rgba(255, 255, 255, 0.1);
  text-align: center;
  min-height: 20px; 
  /* height: 44px;*/
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1rem;
  color: #f38181;
  position: relative;
  box-sizing: border-box;
  font-style:italic
}

.sub-content::after {
  content: "|";
  position: absolute;
  right: 8px;
  animation: blink 0.5s infinite;
  color: rgb(142, 140, 216);
  font-weight: bold;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
</style>