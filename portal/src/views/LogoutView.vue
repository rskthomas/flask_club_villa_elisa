<template>
  <form @submit.prevent="submit">
    <button class="w-100 btn btn-lg btn-primary" type="submit">Logout</button>
  </form>
</template>

<script lang="ts" setup>
import { useRouter } from "vue-router";
import { defineEmits, inject } from "vue";

const emit = defineEmits(["logout"]);
const router = useRouter();
const API_URL = inject('ENDPOINT_PATH');

const submit = async () => {
  const response = await fetch(API_URL + "/auth/logout_jwt", {
    method: "GET",
    credentials: "include",
    mode: "cors",
  });

  if (!response.ok) {
    const message = `An error has occured: ${response.status} - ${response.statusText}`;
    throw new Error(message);
  }
  emit("logout");
  await router.push("/login");
};
</script>
