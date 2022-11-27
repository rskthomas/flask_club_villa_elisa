<template>
  <div class="card">
    <div class="container">
      <h1>
        <slot name="name"> </slot>
      </h1>
      <h2>
        Categoría
        <slot name="category"> - </slot>
      </h2>
      <h3>
        <slot name="schedule"> </slot>
      </h3>
      <p> <slot name="monthly_price"></slot> </p>
      <slot> </slot>
    </div>
  </div>
</template>

<style scoped>

.card {
  /* Add shadows to create the "card" effect */
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  transition: 0.3s;
  background-image: linear-gradient(to left, #c4c4c4, #f5f5f5);
}

/* On mouse-over, add a deeper shadow */
.card:hover {
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
}

.container {
  padding:10px;
  margin: 5px;
}

h1 {
  font-size: 30px;
  font-weight: 600;
  background-image: linear-gradient(to right, #299590, #023d5f);
  color: transparent;
  background-clip: text;
  -webkit-background-clip: text;
}

h2 {
  font-size: 20px;
  font-weight: 600;
  background-image: linear-gradient(to right, #299590, #025a5f);
  color: transparent;
  background-clip: text;
  margin-bottom: 1rem;
}
h3 {
  font-size: 1.2rem;
  font-weight: 500;
}

p {
  font-size: 18px;
  font-weight: 700;
  color: #168a5e;
  margin-top: 1rem;
  margin-right: 1rem;
  text-align: bottom;
}

</style>