import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";

const app = createApp(App);

app.use(router)

app.mount("#app");

export const BASE_API_URL = "http://localhost:5001/api";

export default {
  app: app,
};
