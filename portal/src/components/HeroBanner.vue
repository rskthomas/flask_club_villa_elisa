<script setup>
</script>

<template>
  <div class="container-fluid">
    <div class="row">
      <div class="col items">
        <h1>Club Deportivo Villa Elisa</h1>
        <h2>Bienvenido al Portal de Gestión Online</h2>
        <ul>
          <li>Gestione sus pagos mensuales</li>
          <li>Explore las disciplinas que tenemos disponibles</li>
        </ul>
     </div>
      <div class="col">

        <img srcset="/pwa-192x192.png 300w,
             /pwa-512x512.png 400w,
             /logo.png 800w"
          sizes="(max-width: 320px) 200px,
                  (max-width: 480px) 400px,
                  800px"
          src="/logo.png" alt="logo">

      </div>
    </div>
    </div>
</template>
<style>

h1 {
  font-size: 3rem;
  font-weight: 700;
  text-align: center;
}
h2 {
  font-size: 1.5rem;
  font-weight: 700;
  text-align: center;
  margin-top: 0.5rem;
  margin-bottom: 3rem;
}
.col {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
li {
  font-size: 0.9rem;
  font-weight: 700;
  color: #008040;
  text-align: left;
  margin-bottom: 0.5rem;
}

</style>