<script setup>
import ArticleDetail from '@/views/Post/components/ArticleDetail.vue'
</script>


<template>
    <div class="content">
        <div class="header">
            <h1></h1>
        </div>
        <div class="row">
            <div class="leftcolumn">

            </div>
            
            <div class="rightcolumn">
                <ArticleDetail/>
            </div>
        </div>

    </div>
</template>

<style scoped>
.content{
    background-color: rgba(204, 204, 204, 0.9);
}

.header{
    height: 300px;
}

.row {
    display: flex;
    align-items: flex-start;
    gap: 20px;
    max-width: 1280px;
    padding: 10px;
    justify-content: center;
    margin: 0 auto;
    width: 100%;
    box-sizing: border-box;
}

.leftcolumn {
  flex: 0 0 20%; /* 固定25%宽度 */
  /* background-color: #f1f1f1; */
  padding: 20px;
  border-radius: 8px;
  box-shadow: 1px 2px 5px #fcbad3;
  background-color: wheat;
}

.rightcolumn {
  background-color: #fcbad3;
  flex: 1;       
  padding: 20px;
  min-width: 0; 
  width: 100%;
  border-radius: 8px;
  /* box-shadow: 2px 2px 5px #000; */
}
</style>