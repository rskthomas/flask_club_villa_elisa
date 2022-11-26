<script setup>
import DisciplinesChart from "../components/DisciplinesChart.vue";
import InvoicesChart from "../components/InvoicesChart.vue";
import MembersByGenderChart from "../components/MembersByGenderChart.vue";
</script>

<template>
  <div class="row">
    <div class="col">
      <DisciplinesChart></DisciplinesChart>
    </div>
    <div class="col">
    <MembersByGenderChart></MembersByGenderChart>
    </div>
    <div class="col">
      <InvoicesChart></InvoicesChart>
    </div>
  </div>
</template>
