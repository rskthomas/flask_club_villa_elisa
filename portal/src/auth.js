import { BASE_API_URL } from "./main";

const fetchConfig = {
  method: "GET",
  credentials: "include",
  mode: "cors",
};

export default {
  currentUser: async () => {
    try {
      let response = await fetch(
        BASE_API_URL + "/api/auth/user_jwt",
        fetchConfig
      );

      return await response.json();
    } catch (error) {
      console.log(error);
      return { id: null };
    }
  },
};
