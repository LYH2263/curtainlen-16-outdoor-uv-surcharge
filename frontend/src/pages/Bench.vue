<script setup>
import { onMounted, ref } from 'vue'
import { getJSON, postJSON } from '../api'
import PanelCut from '../components/PanelCut.vue'
const windows = ref([]); const fabrics = ref([]); const types = ref([])
const wid = ref(1); const fid = ref(1); const etype = ref('indoor'); const out = ref(null); const err = ref('')
onMounted(async () => {
  windows.value = (await getJSON('/api/windows')).items.filter(x=>x.data_quality==='clean')
  fabrics.value = (await getJSON('/api/fabrics')).items.filter(x=>x.data_quality==='clean')
  types.value = (await getJSON('/api/exposure/types')).items
  if (types.value.length) etype.value = types.value[0].key
  if (windows.value.length) wid.value = windows.value[0].id
  if (fabrics.value.length) fid.value = fabrics.value[0].id
})
async function go(save){
  err.value = ''; out.value = null
  try {
    out.value = save
      ? await postJSON('/api/estimate',{window_id:wid.value,fabric_id:fid.value,save:true,exposure_type:etype.value})
      : await getJSON(`/api/estimate?window_id=${wid.value}&fabric_id=${fid.value}&exposure_type=${etype.value}`)
  } catch(e){ err.value = e.message }
}
</script>
<template><div class="page"><h1>算料</h1>
<select v-model.number="wid"><option v-for="x in windows" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<select v-model.number="fid"><option v-for="x in fabrics" :key="x.id" :value="x.id">{{ x.name }}</option></select>
<select v-model="etype"><option v-for="t in types" :key="t.key" :value="t.key" :disabled="!t.enabled">{{ t.label }}<template v-if="t.extra_meters">（+{{ t.extra_meters }}m）</template></option></select>
<button @click="go(false)">试算</button><button @click="go(true)">保存</button>
<p v-if="err" class="err">{{ err }}</p>
<template v-if="out">
<p>{{ out.exposure_label }}：基础 {{ out.base_meters }} m + 加米 {{ out.extra_meters }} m = 订货 {{ out.order_meters }} m</p>
<PanelCut :panels="out.panels" :cut-height="out.cut_height" :meters="out.base_meters" />
</template>
</div></template>
