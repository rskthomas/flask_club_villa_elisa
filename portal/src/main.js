import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
export const BASE_API_URL = import.meta.env.VITE_BASE_API_URL;

const app = createApp(App);

app.use(router)

app.mount("#app");



export default {
  app: app,
};
