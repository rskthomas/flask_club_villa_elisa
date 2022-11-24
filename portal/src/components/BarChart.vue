<script setup>
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";
import { onMounted, ref } from "vue";
import { BASE_API_URL } from "../main";

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);

let chartData = ref(null);

let plugins = [
  {
    title: {
      display: true,
      text: "Chart.js Bar Chart - Stacked",
    },
    responsive: true,
  },
];

let chartOptions = {
  type: "bar",
  data: chartData,
  plugins: plugins,
};
let chartIDKey = "just-a-key";
let loaded = ref(false);
const loadData = async () =>{
  let response = await fetch(BASE_API_URL + "/estadisticas/disciplinas", {
    method: "GET",
    mode: "cors",
    cache: "default",
    headers: new Headers({
      "Access-Control-Allow-Origin": "*",
      "Content-Type": "application/json",
    }),
  });

  let disciplinas = await response.json();

  chartData.value = {
    labels: [],
    datasets: [
      {
        label: "Cantidad de inscriptos",
        backgroundColor: "#f87979",
        data: [],
      },
    ],
  };

  for (const disciplina of disciplinas) {
    chartData.value.labels.push(disciplina.name);
    chartData.value.datasets[0].data.push(disciplina.count);
  }
  loaded.value = true;
};

onMounted(() => {
  loadData();
});
</script>

<template>
  <Bar
    :chart-options="chartOptions"
    :chart-data="chartData"
    v-if="loaded"
    :chart-id="chartIDKey"
    :plugins="plugins"
  />
</template>
