const ENDPOINT_PATH = "http://localhost:5001";

const fetchConfig = {
  method: "GET",
  credentials: "include",
  mode: "cors",
  headers: { "Content-Type": "application/json; charset=UTF-8" },
};

export default {
  currentUser: async () => {
    try {
      let response = await fetch(
        ENDPOINT_PATH + "/api/auth/user_jwt",
        fetchConfig
      );

      return response.json();
    } catch (error) {
      console.log(error);
      return { id: null };
    }
  },
};
