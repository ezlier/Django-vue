<script setup>
import Welcome from './components/welcome.vue';
import postlist from './components/postlist.vue';
import About from '@/views/Home/components/about.vue';
import RandomArticle from '@/views/Home/components/RandomArticle.vue'
import Clock from '@/views/Home/components/clock.vue';
</script>

<template>
    <div class="header">
        <Welcome/>
    </div>
    <div class="content">
        <div class="row">
            <div class="leftcolumn">
                <About/>
                <div class="sticky-container">
                    <RandomArticle class="RandomArticle"/>
                    <Clock class="clock-wrapper"/>
                </div>
            </div>
            
            <div class="rightcolumn">
                <postlist/>
            </div>
        </div>

    </div>
</template>

<style scoped>
.sticky-container {
  position: sticky;
  top: 50px;
}

.RandomArticle{
  margin-top: 20px;
}

.clock-wrapper {
  width: 100%;
  margin-top: 20px;
}

.content{
    background-color: rgba(204, 204, 204, 0.9);
}

.header{
    height: 100vh;
    display: flex;
    justify-content: center; /* 水平居中 */
    align-items: center;
}

.row {
    display: flex;
    align-items: stretch;
    gap: 20px;
    max-width: 1280px;
    padding: 10px;
    justify-content: center;
    margin: 0 auto;
    width: 100%;
    box-sizing: border-box;
}

.leftcolumn {
    padding-bottom: 20px;
    flex: 0 0 22%;
    padding: 20px;
    border-radius: 8px;
    position: relative;
}

.rightcolumn {
    flex: 1;       
    padding: 20px;
    min-width: 0; 
    width: 100%;
    border-radius: 8px;
    /* box-shadow: 2px 2px 5px #000; */
}

@media (max-width: 1000px) {
  .leftcolumn {
    display: none;
  }
}
</style>