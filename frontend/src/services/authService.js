import api from "./api";

export const authService = {
  login: async (email, password) => {
    // Normalizes input to accept email, username, or register number
    const response = await api.post("/auth/login", { email, password });
    return response.data;
  },

  getMe: async () => {
    const response = await api.get("/auth/me");
    return response.data;
  },
  
  logout: async () => {
    try {
      const response = await api.post("/auth/logout");
      return response.data;
    } catch (error) {
      return { success: true, message: "Logged out locally" };
    }
  }
};
