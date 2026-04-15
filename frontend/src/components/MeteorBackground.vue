<script setup>
import { onMounted, onBeforeUnmount } from "vue";

let canvas, ctx, meteors = [], animationId;

class Meteor {
  constructor() {
    this.reset();
    this.speed = 5 + Math.random() * 2;
  }
  reset() {
    this.x = Math.random() * canvas.width * 1.5;
    this.y = -20;
    this.length = 50 + Math.random() * 100;
    this.size = 1 + Math.random() * 3;
    this.angle = Math.PI / 4 + Math.random() * Math.PI / 6;
    this.alpha = 1;
  }
  update() {
    this.x += Math.cos(this.angle) * this.speed;
    this.y += Math.sin(this.angle) * this.speed;
    this.alpha -= 0.001;
    if (this.y > canvas.height || this.alpha <= 0) this.reset();
  }
  draw() {
    const endX = this.x - Math.cos(this.angle) * this.length;
    const endY = this.y - Math.sin(this.angle) * this.length;
    ctx.beginPath();
    ctx.moveTo(this.x, this.y);
    ctx.lineTo(endX, endY);
    const gradient = ctx.createLinearGradient(this.x, this.y, endX, endY);
    gradient.addColorStop(0, `rgba(255,255,255,${this.alpha})`);
    gradient.addColorStop(0.5, `rgba(255,255,255,${this.alpha * 0.7})`);
    gradient.addColorStop(1, `rgba(255,255,255,0)`);
    ctx.strokeStyle = gradient;
    ctx.lineWidth = this.size;
    ctx.lineCap = "round";
    ctx.stroke();
  }
}

const resize = () => {
  if (!canvas) return;
  canvas.width = window.innerWidth;
  canvas.height = window.innerHeight;
};

const animate = () => {
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  meteors.forEach((m) => {
    m.update();
    m.draw();
  });
  animationId = requestAnimationFrame(animate);
};

onMounted(() => {
  canvas = document.getElementById("meteorCanvas");
  ctx = canvas.getContext("2d");
  resize();

  meteors = Array.from({ length: Math.floor(Math.random() * 3 + 3) }, () => new Meteor());
  animate();

  window.addEventListener("resize", resize);
});

onBeforeUnmount(() => {
  cancelAnimationFrame(animationId);
  window.removeEventListener("resize", resize);
});
</script>

<template>
  <canvas id="meteorCanvas" class="meteor-canvas"></canvas>
</template>

<style scoped>
.meteor-canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: linear-gradient(to bottom, #0a0a1a 0%, #1a1a3a 50%, #2d2d5a 100%);
  z-index: -1;
}
</style>
