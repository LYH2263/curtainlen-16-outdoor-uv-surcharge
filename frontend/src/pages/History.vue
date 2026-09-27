<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template><div class="page"><h1>记录</h1><ul>
<li v-for="r in items" :key="r.id">
  #{{ r.id }} {{ r.window_name }}
  <template v-if="r.result?.exposure_label">【{{ r.result.exposure_label }}】</template>
  订货 {{ r.result?.order_meters ?? r.result?.meters }}m
  <template v-if="r.result?.extra_meters">（基础 {{ r.result.base_meters }}m + 加米 {{ r.result.extra_meters }}m）</template>
</li>
</ul></div></template>
