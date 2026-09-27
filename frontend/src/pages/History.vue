<script setup>
import { onMounted, ref } from 'vue'
import { getJSON } from '../api'
const items = ref([])
onMounted(async () => { items.value = (await getJSON('/api/runs')).items })
</script>
<template><div class="page"><h1>记录</h1><ul>
<li v-for="r in items" :key="r.id">
  #{{ r.id }} {{ r.window_name }} / {{ r.fabric_name }}
  <span class="tag">{{ r.exposure.label }}</span>
  订货 {{ r.exposure.order_meters }} m
  <template v-if="r.exposure.extra_meters">（基础 {{ r.exposure.base_meters }} m + 加米 {{ r.exposure.extra_meters }} m）</template>
</li>
</ul></div></template>
