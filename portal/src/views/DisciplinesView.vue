<script setup>
import { onMounted, ref } from 'vue';
import DisciplineItem from '../components/DisciplineItem.vue'

const headers = new Headers({
  "Access-Control-Allow-Origin": "*",
  "Content-Type": "application/json"
});

const fetchConfig = {
  method: "GET",
  headers: headers,
  //TODO: Solve CORS issue on production?
  mode: "no-cors",
  cache: "default"
};


//Localhost path for dev usage. TODO: Change to production path
const apiURL = "http://127.0.0.1:5000/api";


const getDisciplines = async () => {
  const response = await fetch(apiURL + "/club/disciplines", fetchConfig);
  console.log(typeof response)
  const data = await response.json();
  console.log(data)
  return data;
  disciplines.value = await JSON.parse(response);
};

/*empty disciplines map*/
const disciplines = ref([]);

/* reactive variables*/
const loading = ref(false);
const error = ref(null);

onMounted(async () => {
  try {
    loading.value = true;
    await getDisciplines();
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});

</script>


<template>
  <div class="disciplines">
    <main>
      <div v-if="loading">Loading...</div>

      <div v-if="error">{{ error }}</div>

      <div v-if="disciplines.length">
        <DisciplineItem v-for="discipline in disciplines" />
        <DisciplineItem>
          <template #icon>
            <ToolingIcon />
          </template>

          <template #name>{{ discipline.category }}</template>



          <template #category> - 2015</template>
          <template #schedule>Lunes a Jueves de 16 a 75 hs</template>
          <template #monthly_price>20 euros</template>

        </DisciplineItem>
      </div>

    </main>
  </div>



</template>

<style scoped>
.disciplines {
  margin-top: 2rem;
  display: flex;
  flex: 1;
  
}

</style>