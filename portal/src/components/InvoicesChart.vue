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

let chartData = ref({
    labels: ['enero', 'febrero'],
    datasets: [{
        label: 'Impagas',
        data: [10, 20],
        stack: 'stack0'
    },
    {
        label: 'Paga',
        data: [1, 2],
        stack: 'stack0',
        backgroundColor: '#f17172f'
    }]
});

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
  scales: {
      x: {
        stacked: true,
      },
      y: {
        stacked: true
      }
    },
    responsive: true,
    interaction: {
      intersect: false,
    },
};

let loaded = ref(true);
const loadData = async () =>{
  let response = await fetch(BASE_API_URL + "/estadisticas/facturacion", {
    method: "GET",
    mode: "cors",
    cache: "default",
    headers: new Headers({
      "Access-Control-Allow-Origin": "*",
      "Content-Type": "application/json",
    }),
  });

  let invoice_info = await response.json();

  chartData.value = {
    labels: [
      "Enero",
      "Febrero",
      "Marzo",
      "Abril",
      "Mayo",
      "Junio",
      "Agosto",
      "Septiembre",
      "Octubre",
      "Noviembre",
      "Diciembre",
    ],
    datasets: [
      {
        label: "Impagas",
        backgroundColor: "#ed0505",
        data: [],
      },
      {
        label: "Pagas",
        backgroundColor: "#8feb34",
        data: [],
      },
    ],
  };
  let last_paid_month = 1;
  let last_unpaid_month = 1;
  for (const month_count of invoice_info) {
    let dataset_index;
    if (month_count.paid) {
      dataset_index = 0;
      if (last_paid_month < month_count.month - 1) {
        let i = last_paid_month;
        while (i < month_count.month - 1 - last_paid_month) {
          chartData.value.datasets[dataset_index].data.push(0);
          i++;
        }
        last_paid_month = month_count.count;
      }
    } else {
      dataset_index = 1;
      if (last_unpaid_month < month_count.month - 1) {
        let i = last_unpaid_month;
        while (i < month_count.month - 1 - last_unpaid_month) {
          chartData.value.datasets[dataset_index].data.push(0);
          i++;
        }
        last_paid_month = month_count.count;
      }
    }
    chartData.value.datasets[dataset_index].data.push(month_count.count);
  }

  loaded.value = true;
};

onMounted(() => {
  loadData();
});
</script>

<template>
  <h2>Estado de cuotas mensuales</h2>
  <Bar
    :chart-options="chartOptions"
    :chart-data="chartData"
    v-if="loaded"
    :plugins="plugins"
  />
</template>
