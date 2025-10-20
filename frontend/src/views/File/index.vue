<script setup>
import { ref, onMounted, computed } from "vue"
import { getArticles } from "@/utils/article"

const articles = ref([])

onMounted(async () => {
  const res = await getArticles()
  articles.value = res.data
})

const sortedArticles = computed(() => {
  return [...articles.value].sort((a, b) => new Date(b.date) - new Date(a.date))
})
</script>

<template>
    <div class="content">
        <div class="header">

        </div>

        <div class="row">
            <div class="leftcolumn">

            </div>
            
            <div class="rightcolumn">
                <el-timeline style="max-width: 600px">
                    <el-timeline-item placement="top">
                        Event start
                    </el-timeline-item>

                    <el-timeline-item
                        v-for="a in sortedArticles"
                        :key="a.slug"
                        center
                        :timestamp="a.date"
                        placement="top"
                    >
                        <RouterLink :to="`/post/${a.slug}`" class="card">
                        <el-card>
                            <h4>{{ a.title }}</h4>
                            <p>{{ a.date }}</p>
                        </el-card>
                        </RouterLink>
                    </el-timeline-item>

                    <el-timeline-item placement="top">
                        Event end
                    </el-timeline-item>
                </el-timeline>
            </div>
        </div>

    </div>
</template>

<style scoped>
.content{
    background-color: rgba(204, 204, 204, 0.9);
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
    flex: 1;       
    padding: 20px;
    min-width: 0; 
    width: 100%;
    border-radius: 8px;
    /* box-shadow: 2px 2px 5px #000; */
}



a {
    text-decoration: none;
    color: inherit;
}

a:hover {
    text-decoration: none;
}

:deep(.el-timeline-item__tail) {
  background: linear-gradient(to bottom, #fcbad3, #a3d8f4);
  opacity: 0.7;
}

:deep(.el-timeline-item__node) {
  background-color: #fcbad3;
  box-shadow: 0 0 6px rgba(252, 186, 211, 0.8);
}

.card {
  display: block;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
}


.card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 15px rgba(252, 186, 211, 0.5);
}

.card h4 {
  margin: 0;
  color: #444;
  font-weight: 600;
}

.card p {
  color: #888;
  margin-top: 4px;
  font-size: 14px;
}

/* 🩵 时间戳文字柔化 */
:deep(.el-timeline-item__timestamp) {
  color: #777;
  font-size: 13px;
}
</style>