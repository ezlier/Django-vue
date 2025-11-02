<template>
    <h1>📕文章管理</h1>
    <el-table :data="articles" style="width: 100%" max-height="600">
        <el-table-column type="index" width="50" />
        <el-table-column prop="date" sortable label="Date" width="150" />
        <el-table-column prop="title" label="Name" />
        <el-table-column fixed="right" label="Operations" min-width="120">
            <template #default="scope">
                <el-button link type="danger" size="small" @click.prevent="deleteRow(scope.row)">
                    删除
                </el-button>
            </template>
        </el-table-column>
    </el-table>
    <el-upload 
    ref="uploadRef"
    class="upload-demo"
    style="max-width: 300px;"
    action="http://127.0.0.1:8000/api/articles/"
    :auto-upload="false"
    :headers="headers"
    name="file"
    :on-success="handleUploadSuccess"
    :on-error="handleUploadError">
        <template #trigger>
            <el-button type="primary">select file</el-button>
        </template>

        <el-button class="ml-3" type="success" @click="submitUpload">
            upload to server
        </el-button>
        <p>上传完请刷新页面</p>
    </el-upload>
</template>

<script setup>
import { getArticles,deleteArticle  } from "@/utils/article";
import { onMounted, ref } from "vue";
import { ElMessage } from "element-plus";

const articles = ref([]);
const uploadRef = ref(null);

// ✅ 封装获取文章函数
const fetchArticles = async () => {
  const res = await getArticles();
  articles.value = res.data;
};

// 页面加载时获取
onMounted(fetchArticles);

// 删除行
const deleteRow = async (row) => {
  try {
    await deleteArticle(row.slug)
    ElMessage.success(`已删除：${row.title}`)
    fetchArticles() // 自动刷新表格
  } catch (err) {
    ElMessage.error("删除失败：" + err)
  }
}
// 上传相关
const submitUpload = () => {
  uploadRef.value.submit();
};

// ✅ 上传成功时刷新表格
const handleUploadSuccess = () => {
  ElMessage.success("上传成功！请手动刷新页面");
  fetchArticles();
};

// 上传失败时提示
const handleUploadError = (err) => {
  ElMessage.error("上传失败：" + err);
};
</script>