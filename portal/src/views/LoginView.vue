<template>
  <form @submit.prevent="submit">
    <h1 class="h3 mb-3 fw-normal">Login</h1>

    <div class="form-floating">
      <input
        v-model="data.username"
        type="username"
        class="form-control"
        placeholder="username"
        required />
      <label for="floatingInput">Usuario</label>
    </div>

    <div class="form-floating">
      <input
        v-model="data.password"
        type="password"
        class="form-control"
        placeholder="Password"
        required />
      <label for="floatingPassword">Clave</label>
    </div>

    <button class="w-100 btn btn-lg btn-primary" type="submit">Login</button>
  </form>
</template>

<script lang="ts" setup>
import { reactive, defineEmits } from "vue";
import { useRouter } from "vue-router";
import { BASE_API_URL } from "../main";
const emit = defineEmits(["login"]);

const data = reactive({
  username: "",
  password: "",
});

const router = useRouter();

const submit = async () => {
  let response = await fetch(BASE_API_URL + "/api/auth/login", {
    method: "POST",
    credentials: "include",
    mode: "cors",
    headers: { "Content-Type": "application/json; charset=UTF-8" },
    body: JSON.stringify(data),
  });
  if (!response.ok) {
    alert("Credenciales inválidas");
  } else {
    emit("login");
    await router.push("/");
  }
};
</script>

<style>
.form-signin {
  width: 100%;
  max-width: 330px;
  padding: 15px;
  margin: auto;
}

.form-signin .form-floating:focus-within {
    z-index: 2;
}

  .form-signin input[type="email"] {
    margin-bottom: -1px;
    border-bottom-right-radius: 0;
    border-bottom-left-radius: 0;
  }

  .form-signin input[type="password"] {
    margin-bottom: 10px;
    border-top-left-radius: 0;
    border-top-right-radius: 0;
  }
</style>
