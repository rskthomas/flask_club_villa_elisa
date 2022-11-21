<template v-on:login="loadUser" v-on:logout="unlinkUser">
  <nav class="navbar navbar-expand-md navbar-dark bg-dark mb-4">
    <div class="container-fluid">
      <router-link to="/" class="navbar-brand">Home</router-link>
      <div>
        <ul class="navbar-nav me-auto mb-2 mb-md-0">
          <li class="nav-item" v-if="!user || user.id == null">
            <router-link to="/login" class="nav-link active">Login</router-link>
          </li>
          <li class="nav-item">
            <router-link to="/disciplines" class="nav-link active">Disciplinas</router-link>
                </li>
          <li class="nav-item" v-if="user && user.id">
            <router-link to="/logout" class="nav-link active">Logout</router-link>
                >
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import auth from "../auth";
import { ref } from "vue";

let user = ref({ id: null });

const loadUser = async () => {
 user.value = await auth.currentUser();
};

const unlinkUser = async () => {
    console.log('unlinkeando user')
    console.log('unlinkeando user')
    console.log('unlinkeando user')
    console.log('unlinkeando user')
    console.log('unlinkeando user')
    user.value = {id: null}
}

loadUser();
</script>
