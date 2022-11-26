const ENDPOINT_PATH = "http://localhost:5000/api"

const fetchConfig = {
  method: "GET",
  credentials: "include",
  mode: "cors",
};

export default {
  currentUser: async () => {
    try {
      let response = await fetch(
        ENDPOINT_PATH + "/auth/user_jwt",
        fetchConfig
      );

      return response.json();
    } catch (error) {
      console.log(error);
      return { id: null };
    }
  },
};
