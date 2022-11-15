<template>
    <form @submit.prevent="submit">
    <button class="w-100 btn btn-lg btn-primary" type="submit">Logout</button>
  </form>
</template>
  
  
<script lang="ts">
import {useRouter} from "vue-router";

export default {
  name: "Logout",
  setup() {
    const router = useRouter();

    const submit = async () => {
      await fetch('http://localhost:5001/api/auth/logout_jwt', {
        method: 'GET',
        credentials: 'include',
        mode: "no-cors",
        headers: {
            'Content-Type':'application/json; charset=UTF-8'
        }     
      });  

      await router.push('/login');
    }
    
    return {
      submit
    }
  }
}
</script>