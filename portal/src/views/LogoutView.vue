<template>
  <form @submit.prevent="submit">
    <button class="w-100 btn btn-lg btn-primary" type="submit">Logout</button>
  </form>
</template>

<script lang="ts" setup>
import { useRouter } from "vue-router";
import { defineEmits } from "vue";

const emit = defineEmits(["logout"]);
const router = useRouter();

const headers = new Headers({
  "Access-Control-Allow-Origin": "http://localhost:5001",
  "Access-Control-Allow-Credentials": "true",
  "Content-Type": "application/json",
});

const submit = async () => {
  const response = await fetch("http://localhost:5001/api/auth/logout_jwt", {
    method: "GET",
    credentials: "include",
    mode: "cors",
    headers: headers,
  });

  if (!response.ok) {
    const message = `An error has occured: ${response.status} - ${response.statusText}`;
    throw new Error(message);
  }
  emit("logout");
  await router.push("/login");
};
</script>
