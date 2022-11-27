<script setup>
import DisciplinesChart from "../components/DisciplinesChart.vue";
import InvoicesChart from "../components/InvoicesChart.vue";
import MembersByGenderChart from "../components/MembersByGenderChart.vue";
import auth from "../auth";
import { useRouter } from "vue-router";
import { ref } from "vue";
const router = useRouter();
const enoughPermissions = ref(false);

const checkAccessLevel = async () => {
  let user = await auth.currentUser();

  if (!user.id) {
    alert("usted debe iniciar sesión para ver esta pantalla");
    router.push("/login");
  } else if (!auth.isAdmin(user) && !auth.isOperador(user)) {
    alert("Usted no tiene permisos suficientes");
    window.location.href = "/";
  } else {
    enoughPermissions.value = true;
  }
};

checkAccessLevel();
</script>

<template>
  <div class="row">
    <div class="col">
      <DisciplinesChart v-if="enoughPermissions"></DisciplinesChart>
    </div>
    <div class="col">
    <MembersByGenderChart v-if="enoughPermissions"></MembersByGenderChart>
    </div>
    <div class="col">
      <InvoicesChart v-if="enoughPermissions"></InvoicesChart>
    </div>
  </div>
</template>
