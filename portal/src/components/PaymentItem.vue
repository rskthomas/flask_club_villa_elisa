<template>
  <div class="card">
    <div class="container">
      <h1>
        <slot name="month"> </slot>
      </h1>
      <h2>
        <slot name="amount"> </slot>
      </h2>
      <h3>
        <slot name="paid"> </slot>
      </h3>
      <h3>
        <slot name="payment_date"> </slot>
      </h3>
      <br />
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
  padding:15px;
  margin: 5px;
}

h1 {
  font-size: 26px;
  font-weight: 600;
  background-image: linear-gradient(to right, #2d9529, #025f3b);
  color: transparent;
  background-clip: text;
  -webkit-background-clip: text;
}

h3 {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 0.4rem;
  color: var(--color-heading);
}
</style>