import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getAdminTags, createTag, updateTag, deleteTag } from '@/api/admin'
import { ElMessage } from 'element-plus'

export const useTagStore = defineStore('tag', () => {
  const tags = ref<AdminTag[]>([])
  const loading = ref(false)

  async function fetchTags() {
    loading.value = true
    try {
      const res = await getAdminTags()
      tags.value = res.data.data
    } finally {
      loading.value = false
    }
  }

  async function addTag(name: string) {
    await createTag(name)
    ElMessage.success('标签创建成功')
    await fetchTags()
  }

  async function renameTag(id: number, name: string) {
    await updateTag(id, name)
    ElMessage.success('标签更新成功')
    await fetchTags()
  }

  async function removeTag(id: number) {
    await deleteTag(id)
    ElMessage.success('标签已删除')
    await fetchTags()
  }

  return { tags, loading, fetchTags, addTag, renameTag, removeTag }
})

export interface AdminTag {
  id: number
  name: string
}
