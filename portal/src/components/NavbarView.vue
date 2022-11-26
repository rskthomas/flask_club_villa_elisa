<script setup>
import auth from "../auth";
import { onMounted, ref } from "vue";

let user = ref({ id: null });
let loaded = ref(false);

const loadUser = async () => {
  user.value = await auth.currentUser();
  loaded.value = true;
};

const isAdmin = (user) => {
  return user.roles.find((role) => role.includes("Administrador")) != undefined;
};
const isOperador = (user) => {
  return user.roles.find((role) => role.includes("Operador")) != undefined;
};
onMounted(() => loadUser());
</script>

<template>
  <nav class="navbar navbar-expand-md navbar-dark bg-dark mb-4">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand">Home</router-link>
      <div>
        <ul class="navbar-nav me-auto mb-2 mb-md-0">
          <li class="nav-item" v-if="loaded && !user.id">
            <router-link to="/login" class="nav-link active">Login</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/disciplines" class="nav-link active"
              >Disciplinas</router-link
            >
          </li>
          <li class="nav-item" v-if="loaded && user.id && (isAdmin(user) || isOperador(user))">
            <router-link to="/estadisticas" class="nav-link active"
              >Estadisticas</router-link
            >
          </li>
          <li class="nav-item" v-if="loaded && user.id">
            <router-link to="/logout" class="nav-link active"
              >Logout</router-link
            >
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>
