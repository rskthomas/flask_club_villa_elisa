import { BASE_API_URL } from "./main";
import { ref } from "vue";

const user = ref({ id: null });

const fetchConfig = {
  method: "GET",
  credentials: "include",
  mode: "cors",
};

const getUserFromApi = async () => {
  try {
    let response = await fetch(
      BASE_API_URL + "/api/auth/user_jwt",
      fetchConfig
    );

    return await response.json();
  } catch (error) {
    return { id: null };
  }
};

const isAdmin = (user) => {
  return user.roles.find((role) => role.includes("Administrador")) != undefined;
};
const isOperador = (user) => {
  return user.roles.find((role) => role.includes("Operador")) != undefined;
};

export default {
  currentUser: async () => {
    if (user.value.id == null) {
      user.value = await getUserFromApi();
    }
    return user.value;
  },
  isAdmin: isAdmin,
  isOperador: isOperador,
};
