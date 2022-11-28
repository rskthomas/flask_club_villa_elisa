
<script setup>
  import { onMounted, ref } from 'vue';
  import PaymentItem from '../components/PaymentItem.vue';
  import moment from 'moment';
  import { BASE_API_URL } from "../main";

  const fetchConfig = {
    method: "GET",
    credentials: 'include',
    mode: "cors",
    cache: "default"
  };


  const getPayments = async () => {
    const response = await fetch(BASE_API_URL+'/api/me/payments', fetchConfig);
    if (!response.ok) {
      const message = `An error has occured: ${response.status} - ${response.statusText}`;
      throw new Error(message);
    }

    const data = await response.json();
    return data
  };

  /*empty payments map*/
  const payments = ref({});

  /* reactive fetch state variables*/
  const loading = ref(false);
  const error = ref(null);

  onMounted(async () => {
    try {
      loading.value = true;
      payments.value = await getPayments();
    } catch (err) {
      error.value = err.message;
    } finally {
      loading.value = false;
    }
  });


  // gets date formatted as yyyy-MM-dd
  const formatDate = (date) => {
    return moment(date).format("YYYY-MM-DD");
  }


</script>


<template>
  <h1>Payments</h1>

  <div class="pagos" style>
    <main>
      <div v-if="loading" class="loader"></div> 
      <div v-if="error">{{ error }}</div>

      <div v-if="payments.length">
        <div v-for="pay in payments" style="margin:15px;">

        <PaymentItem>
          <template #month>Factura del mes: {{ pay.month }}</template>
          <template #amount>${{ pay.amount }}</template>
          <template #paid >               
            <h3 v-if="pay.paid" style="color: green">Pagada</h3>
            <h3 v-else="pay.paid" style="color: red">Impaga 
              <router-link :to="`/pay_invoice/${pay.id}`" custom v-slot="{ navigate }" >
                <button @click="navigate" role="link" class="w-50 h-20 btn btn-lg btn-primary" > Pagar </button>
              </router-link>
            </h3>
          </template>
          <template #payment_date>{{ formatDate(pay.payment_date) }}</template>
        </PaymentItem>
      
      </div>
    </div>

    </main>
  </div>

</template>

<style scoped>
.pagos {
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