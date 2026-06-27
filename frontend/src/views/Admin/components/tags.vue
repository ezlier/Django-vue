<template>
    <h1>标签管理</h1>
    <el-table :data="tags" border>
        <el-table-column prop="id" label="ID" width="100" />
        <el-table-column prop="name" label="标签名称" />
        <el-table-column prop="article_count" label="文章数量" />
        <el-table-column fixed="right" label="Operations">
            <template #default="scope">
                <el-button link type="warning" size="small" @click="handleEdit(scope.row)">
                    修改
                </el-button>
                <el-button link type="danger" size="small" @click.prevent="delete_Tag(scope.row)">
                    删除
                </el-button>
            </template>
        </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" title="修改标签" width="30%">
        <el-form :model="editForm">
            <el-form-item label="标签名称">
                <el-input v-model="editForm.name" autocomplete="off" />
            </el-form-item>
        </el-form>
        <template #footer>
            <span class="dialog-footer">
                <el-button @click="dialogVisible = false">取消</el-button>
                <el-button type="primary" @click="submitEdit">确认</el-button>
            </span>
        </template>
    </el-dialog>
</template>

<script setup>
import { getAdminTags, updateTag, deleteTag } from '@/utils/article';
import { onMounted, ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';

const tags = ref([]);
const dialogVisible = ref(false);

// 3. 定义编辑表单的数据模型
const editForm = reactive({
    id: '',
    name: ''
});

// 获取数据
const loadTags = async () => {
    const res = await getAdminTags();
    tags.value = res.data.results;
}

onMounted(() => {
    loadTags();
})

// 4. 打开弹窗并回显数据
const handleEdit = (row) => {
    dialogVisible.value = true;
    // 使用浅拷贝，避免直接修改表格显示的数据
    editForm.id = row.id;
    editForm.name = row.name;
}

// 5. 提交修改
const submitEdit = async () => {
    await updateTag(editForm.id, editForm.name);
    
    ElMessage.success('修改成功');
    dialogVisible.value = false;
    
    // 重新刷新列表
    await loadTags();
}

const delete_Tag = async (row) => {
    try {
        await deleteTag(row.id)
        ElMessage.success("已删除")
        loadTags()
    } catch(err) {
        ElMessage.error(err)
    }
}
</script>