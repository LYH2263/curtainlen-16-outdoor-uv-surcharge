<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
const s = ref({}); const extra = ref(''); const enabled = ref(true); const msg = ref('')
onMounted(async () => {
  s.value = await getJSON('/api/settings')
  extra.value = s.value.exposure_outdoor_uv_extra ?? ''
  enabled.value = (s.value.exposure_outdoor_uv_enabled ?? '1') === '1'
})
async function save(){
  msg.value = ''
  await postJSON('/api/settings', { key: 'exposure_outdoor_uv_extra', value: extra.value })
  s.value = await postJSON('/api/settings', { key: 'exposure_outdoor_uv_enabled', value: enabled.value ? '1' : '0' })
  msg.value = '已保存'
}
</script>
<template><div class="page"><h1>设置</h1>
<p>默认褶倍 {{ s.default_fullness }}</p>
<h2>空间曝晒</h2>
<label>户外抗紫外固定加米（m） <input v-model="extra" placeholder="0.5" /></label>
<label><input type="checkbox" v-model="enabled" /> 启用户外抗紫外类型（停用后新测算回到基础口径）</label>
<button @click="save">保存</button>
<span>{{ msg }}</span>
<p>提示：加米须为非负数字；非法配置将拒绝户外类型测算。已保存的历史记录不受此处修改影响。</p>
</div></template>
