<script setup>
import { onMounted, ref, inject } from 'vue';
import DisciplineItem from '../components/DisciplineItem.vue'

/* simple GET request, no headers needed*/

import { BASE_API_URL } from "../main";

const fetchConfig = {
  method: "GET",
  credentials: 'include',
  mode: "cors",
  cache: "default"
};

const getDisciplines = async () => {
  const response = await fetch(BASE_API_URL + "/club/disciplines", fetchConfig);
  if (!response.ok) {
          console.log("Error fetching disciplines", response);
          const message = `An error has occured: ${response.status} - ${response.statusText}`;
          throw new Error(message);
        }

  const data = await response.json();
  return data
};

/*empty disciplines map*/
const disciplines = ref([]);

/* reactive fetch state variables*/
const loading = ref(false);
const error = ref(null);

onMounted(async () => {
  try {
    loading.value = true;
    disciplines.value = await getDisciplines();
  } catch (err) {
    error.value = err.message;
  } finally {
    loading.value = false;
  }
});

</script>


<template>
  <h1>Disciplinas</h1>

  <div class="disciplines" style>
    <main>
      <div v-if="loading" class="loader"></div> 
      <div v-if="error">{{ error }}</div>

      <div v-if="disciplines.length">
        <div v-for="discipline in disciplines" style="margin:15px;">

        <DisciplineItem>
          <template #name>{{ discipline.name }}</template>
          <template #category> {{discipline.category}} </template>
          <template #schedule> {{discipline.schedule}}</template>
          <template #monthly_price>$ {{ discipline.monthly_price }} mensuales</template>
          <template #description>{{ discipline.description }}</template>
        </DisciplineItem>
      
      </div>
    </div>

    </main>
  </div>

</template>

<style scoped>
.disciplines {
  margin: 1rem;
  display: flex;
  padding: 1rem;  
}

.loader {
  border: 5px solid #f3f3f3; /* Light grey */
  border-top: 5px solid #3498db; /* Blue */
  border-radius: 50%;
  width: 50px;
  height: 50px;
  animation: spin 2s linear infinite;
 
}
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
h1 {
  text-align: center;
  font-size: 60px;
  font-weight: 600;
  color: grey;
  background-clip: text;
}

</style>