<template>
  <div class="card">
    <div class="container">
      <h1>
        <slot name="name"> </slot>
        <slot name="category"> - </slot>
      </h1>
      <h3>
        <slot name="schedule"> </slot>
      </h3>
      <slot name="monthly_price"></slot>
      <br />
      <slot> </slot>
    </div>
  </div>
</template>

<style scoped>
.details {
  flex: 1;
  margin-left: 1rem;
}

h3 {
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 0.4rem;
  color: var(--color-heading);
}

.card {
  /* Add shadows to create the "card" effect */
  box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2);
  transition: 0.3s;
  background-image: linear-gradient(to left, #c4c4c4, #e8e8e8);
}

/* On mouse-over, add a deeper shadow */
.card:hover {
  box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
}

/* Add some padding inside the card container */
.container {
  padding:15px;
  margin: 5px;
}
h1 {
  font-size: 26px;
  font-weight: 600;
  background-image: linear-gradient(to left, #2d9529, #025f3b);
  color: transparent;
  background-clip: text;
  -webkit-background-clip: text;
}
</style>