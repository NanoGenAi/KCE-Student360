import React, { createContext, useState, useEffect } from "react";
import { authService } from "../services/authService";
import { studentSubmissionService } from "../services/studentSubmissionService";

export const AuthContext = createContext();

const MOCK_USERS = [
  { email: "faculty@student360.com", password: "Password123!", name: "Dr. Ramanujam", role: "faculty" },
  { email: "mentor@student360.com", password: "Password123!", name: "Dr. Monisha R", role: "mentor" },
  { email: "student@student360.com", password: "Password123!", name: "Shahul", role: "student", studentId: "1", registerNo: "22AD001" },
  { email: "admin@student360.com", password: "Password123!", name: "Admin Officer", role: "admin" }
];

const getErrorMessage = (error) => {
  if (!error) return "Login failed";

  if (typeof error === "string") return error;

  if (error.response?.data?.error?.message) {
    return error.response.data.error.message;
  }

  if (error.response?.data?.detail) {
    if (typeof error.response.data.detail === "string") {
      return error.response.data.detail;
    }

    if (Array.isArray(error.response.data.detail)) {
      return error.response.data.detail
        .map((item) => item.msg || JSON.stringify(item))
        .join(", ");
    }

    return JSON.stringify(error.response.data.detail);
  }

  if (error.message) return error.message;

  return "Login failed. Please check your credentials.";
};

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [backendError, setBackendError] = useState("");

  useEffect(() => {
    const verifySession = async () => {
      const savedUser = localStorage.getItem("currentUser") || localStorage.getItem("user");
      const token = localStorage.getItem("access_token") || localStorage.getItem("token");
      
      if (token && savedUser) {
        try {
          // Verify with backend
          const fetchedUser = await authService.getMe();
          localStorage.setItem("currentUser", JSON.stringify(fetchedUser));
          setUser(fetchedUser);

          if (fetchedUser.role === "student") {
            const regNo = fetchedUser.registerNo || fetchedUser.register_no;
            if (regNo) {
              await studentSubmissionService.syncSubmissionsWithBackend(regNo);
            }
          }
        } catch (err) {
          if (err.code === "ERR_NETWORK" || !err.response) {
            console.warn("Backend server is not running. Please start FastAPI backend.");
            setBackendError("Backend server is not running. Please start FastAPI backend.");
            // Network fallback: use local storage data
            setUser(JSON.parse(savedUser));
          } else {
            // Token invalid/expired: logout
            console.warn("Session invalid, clearing credentials.");
            localStorage.clear();
            setUser(null);
          }
        }
      }
      setLoading(false);
    };

    verifySession();
  }, []);

  const login = async (email, password) => {
    setLoading(true);
    setBackendError("");
    
    console.log("Login endpoint: /auth/login");
    console.log("Login identifier:", email);
    
    try {
      // 1. Attempt backend login
      const response = await authService.login(email, password);
      console.log("Login response:", response);
      
      localStorage.setItem("access_token", response.access_token);
      localStorage.setItem("refresh_token", response.refresh_token);
      localStorage.setItem("currentUser", JSON.stringify(response.user));
      
      // Also write legacy keys for absolute compatibility with any components reading them
      localStorage.setItem("user", JSON.stringify(response.user));
      localStorage.setItem("token", response.access_token);

      setUser(response.user);
      if (response.user.role === "student") {
        const regNo = response.user.registerNo || response.user.register_no;
        if (regNo) {
          await studentSubmissionService.syncSubmissionsWithBackend(regNo);
        }
      }
      setLoading(false);
      return response.user;
    } catch (error) {
      console.log("Login error response:", error.response?.data);
      
      if (error.code === "ERR_NETWORK" || !error.response) {
        console.warn("Backend server is not running. Falling back to mock authentication.");
        setBackendError("Backend server is not running. Please start FastAPI backend.");
        
        // Mock fallback
        const foundUser = MOCK_USERS.find(
          (u) => (u.email.toLowerCase() === email.toLowerCase() || u.role === email) && u.password === password
        );

        if (foundUser) {
          const userData = {
            id: foundUser.role === "student" ? 1 : 99,
            name: foundUser.name,
            email: foundUser.email,
            username: foundUser.role,
            role: foundUser.role,
            studentId: foundUser.studentId ? parseInt(foundUser.studentId) : null,
            student_id: foundUser.studentId ? parseInt(foundUser.studentId) : null,
            registerNo: foundUser.registerNo || null,
            register_no: foundUser.registerNo || null,
            profileImage: null,
            profile_image: null
          };
          
          const mockToken = `mock-jwt-token-for-${foundUser.role}`;
          localStorage.setItem("access_token", mockToken);
          localStorage.setItem("currentUser", JSON.stringify(userData));
          localStorage.setItem("user", JSON.stringify(userData));
          localStorage.setItem("token", mockToken);
          
          setUser(userData);
          setLoading(false);
          return userData;
        } else {
          setLoading(false);
          throw new Error("Invalid credentials (Mock Fallback)");
        }
      } else {
        setLoading(false);
        // Error returned from backend, extract message safely
        const detailMsg = getErrorMessage(error);
        throw new Error(detailMsg);
      }
    }
  };

  const logout = async () => {
    await authService.logout();
    
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("currentUser");
    localStorage.removeItem("user");
    localStorage.removeItem("token");
    
    setUser(null);
  };

  const updateUser = (updates) => {
    setUser((prev) => {
      const merged = {
        ...prev,
        ...updates,
        profileImage:
          updates.profileImage ||
          updates.profile_image ||
          prev?.profileImage ||
          prev?.profile_image ||
          null,
        profile_image:
          updates.profile_image ||
          updates.profileImage ||
          prev?.profile_image ||
          prev?.profileImage ||
          null,
        profileImageUpdatedAt: updates.profileImageUpdatedAt || Date.now(),
      };

      localStorage.setItem("currentUser", JSON.stringify(merged));
      localStorage.setItem("user", JSON.stringify(merged));

      return merged;
    });
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, isAuthenticated: !!user, updateUser, backendError }}>
      {children}
    </AuthContext.Provider>
  );
};
