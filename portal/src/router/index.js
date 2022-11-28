import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import LoginView from '../views/LoginView.vue'
import LogoutView from '../views/LogoutView.vue'
import DisciplinesView from '../views/DisciplinesView.vue'
import PaymentsView from '../views/PaymentsView.vue'
import PayInvoiceView from '../views/PayInvoiceView.vue'
import EstadisticasView from "../views/EstadisticasView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/", name: "home", component: HomeView },
    { path: "/login", name: "login", component: LoginView },
    { path: "/logout", name: "logout", component: LogoutView },
    { path: "/disciplines", name: "disciplines", component: DisciplinesView },
    {path: '/payments', name: 'payments', component: PaymentsView},
    {path: '/pay_invoice/:invoiceId', name: 'pay_invoice', component: PayInvoiceView},
    {
      path: "/estadisticas",
      name: "estadisticas",
      component: EstadisticasView,
    },
  ],
});

export default router;
