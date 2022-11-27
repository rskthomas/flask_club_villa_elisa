<script setup>
import { Pie } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
} from "chart.js";
import { onMounted, ref } from "vue";
import { BASE_API_URL } from "../main";

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale);
let possible_colors = ["#ebcc34", "#34eb9c", "#34eb9c", "#7134eb"];
const chartData = ref({
  labels: [],
  datasets: [
    {
      backgroundColor: [],
      data: [],
    },
  ],
});

let loaded = ref(false);

const chartOptions = {
  responsive: true,
  maintainAspectRatio: false,
};

const loadData = async () => {
  let response = await fetch(
    BASE_API_URL + "/api/estadisticas/miembros_por_genero",
    {
      method: "GET",
      mode: "cors",
      cache: "default",
      credentials: "include",
      headers: new Headers({
        "Content-Type": "application/json",
      }),
    }
  );

  let gender_count = await response.json();

  for (const gender_info of gender_count) {
    chartData.value.labels.push(gender_info.gender);
    chartData.value.datasets[0].backgroundColor.push(possible_colors.pop());
    chartData.value.datasets[0].data.push(gender_info.count);
  }

  loaded.value = true;
};
onMounted(loadData);
</script>
<template>
  <h2>Inscriptos por Género</h2>
  <Pie :chart-options="chartOptions" :chart-data="chartData" v-if="loaded" />
</template>
