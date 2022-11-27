<template>
  <form @submit.prevent="submit">
    <button class="w-100 btn btn-lg btn-primary" type="submit">Logout</button>
  </form>
</template>

<script lang="ts" setup>
import { useRouter } from "vue-router";
import { defineEmits } from "vue";
import { BASE_API_URL } from "../main";
const emit = defineEmits(["logout"]);
const router = useRouter();

const headers = new Headers({
  "Content-Type": "application/json",
});

const submit = async () => {
  const response = await fetch(BASE_API_URL + "/api/auth/logout_jwt", {
    method: "GET",
    credentials: "include",
    mode: "cors",
  });

  if (!response.ok) {
    const message = `An error has occured: ${response.status} - ${response.statusText}`;
    throw new Error(message);
  }
  emit("logout");
  
  await router.push("/");
  /*awful way to refresh navbar, but gets the job done*/
  router.go(0);
};
</script>
