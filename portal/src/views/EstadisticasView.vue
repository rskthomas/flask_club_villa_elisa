<script setup>
import DisciplinesChart from "../components/DisciplinesChart.vue";
import InvoicesChart from "../components/InvoicesChart.vue";
import MembersByGenderChart from "../components/MembersByGenderChart.vue";
import auth from "../auth";
import { useRouter } from "vue-router";

const router = useRouter();

const checkAccessLevel = async () => {
  let user = await auth.currentUser();

  console.log(user);
  if (!user.id) {
    alert("usted debe iniciar sesión para ver esta pantalla");
    router.push("/login");
  } else if (!auth.isAdmin(user) || !auth.isOperador(user)) {
    alert("Usted no tiene permisos suficientes");
    window.location.href = "/";
  }
};

await checkAccessLevel();
</script>

<template>
  <div class="row">
    <div class="col">
      <DisciplinesChart></DisciplinesChart>
    </div>
    <div class="col">
    <MembersByGenderChart></MembersByGenderChart>
    </div>
    <div class="col">
      <InvoicesChart></InvoicesChart>
    </div>
  </div>
</template>
