<script setup>
import DisciplinesChart from "../components/DisciplinesChart.vue";
import InvoicesChart from "../components/InvoicesChart.vue";
import PieChart from "../components/PieChart.ts";
</script>

<template>
  <div class="row">
    <div class="col">
      <DisciplinesChart></DisciplinesChart>
    </div>
    <div class="col">
    <PieChart></PieChart>
    </div>
    <div class="col">
      <InvoicesChart></InvoicesChart>
    </div>
  </div>
</template>
