import api from "./api";

const SUBMISSIONS_KEY_PREFIX = "student360_submissions_";

const getSubmissions = (registerNo) => {
  const data = localStorage.getItem(`${SUBMISSIONS_KEY_PREFIX}${registerNo}`);
  if (data) {
    try {
      return JSON.parse(data);
    } catch (e) {
      console.error("Error parsing submissions from localStorage", e);
    }
  }
  return { projects: [], certifications: [], achievements: [] };
};

const saveSubmissions = (registerNo, submissions) => {
  localStorage.setItem(`${SUBMISSIONS_KEY_PREFIX}${registerNo}`, JSON.stringify(submissions));
};

export const studentSubmissionService = {
  // Sync utility called on authentication session starts
  syncSubmissionsWithBackend: async (registerNo) => {
    try {
      const [projResp, certResp, achResp] = await Promise.all([
        api.get("/student/projects/me"),
        api.get("/student/certifications/me"),
        api.get("/student/achievements/me")
      ]);

      const submissions = {
        projects: projResp.data || [],
        certifications: certResp.data || [],
        achievements: achResp.data || []
      };

      saveSubmissions(registerNo, submissions);
      return submissions;
    } catch (error) {
      console.warn("Could not sync student submissions with backend:", error.message);
      return getSubmissions(registerNo);
    }
  },

  submitProject: async (projectData) => {
    const registerNo = projectData.registerNo || "22AD001";
    
    try {
      // 1. Try submitting to FastAPI backend using multipart/form-data FormData
      const formData = new FormData();
      formData.append("title", projectData.title);
      formData.append("description", projectData.description);
      formData.append("tech_stack", Array.isArray(projectData.tech_stack) ? JSON.stringify(projectData.tech_stack) : projectData.tech_stack);
      formData.append("role", projectData.role || "Developer");
      formData.append("github_link", projectData.github_link || "");
      formData.append("live_demo_link", projectData.live_link || projectData.live_demo_link || "");
      
      const fileObj = projectData.file || projectData.proof_file;
      if (fileObj) {
        formData.append("file", fileObj);
      }

      const response = await api.post("/student/projects", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      const newProject = response.data;

      // Update local storage cache to keep synchronous UI queries updated
      const submissions = getSubmissions(registerNo);
      submissions.projects.push(newProject);
      saveSubmissions(registerNo, submissions);

      return {
        success: true,
        message: "Project submitted for mentor review.",
        project: newProject
      };
    } catch (error) {
      if (error.code === "ERR_NETWORK" || !error.response) {
        console.warn("Backend offline. Saving project submission to localStorage fallback.");
        // Local fallback
        const newProject = {
          id: "p_user_" + Date.now(),
          title: projectData.title,
          description: projectData.description,
          tech_stack: Array.isArray(projectData.tech_stack) 
            ? projectData.tech_stack 
            : projectData.tech_stack.split(",").map(s => s.trim()).filter(Boolean),
          github_link: projectData.github_link || "",
          live_link: projectData.live_link || "",
          project_type: projectData.project_type || "Other",
          status: "Pending",
          submitted_date: new Date().toISOString().split("T")[0]
        };

        const submissions = getSubmissions(registerNo);
        submissions.projects.push(newProject);
        saveSubmissions(registerNo, submissions);

        return {
          success: true,
          message: "Project submitted locally (Offline Fallback).",
          project: newProject
        };
      }
      throw error;
    }
  },

  submitCertification: async (certificationData) => {
    const registerNo = certificationData.registerNo || "22AD001";
    
    try {
      const formData = new FormData();
      formData.append("title", certificationData.title);
      formData.append("issuer", certificationData.issuer);
      formData.append("credential_id", certificationData.credential_id || "");
      formData.append("issue_date", certificationData.issue_date);
      if (certificationData.expiry_date) {
        formData.append("expiry_date", certificationData.expiry_date);
      }
      formData.append("certificate_link", certificationData.verification_link || certificationData.certificate_link || "");
      
      const fileObj = certificationData.file || certificationData.proof_file;
      if (fileObj) {
        formData.append("file", fileObj);
      }

      const response = await api.post("/student/certifications", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      const newCert = response.data;

      const submissions = getSubmissions(registerNo);
      submissions.certifications.push(newCert);
      saveSubmissions(registerNo, submissions);

      return {
        success: true,
        message: "Certification submitted for mentor review.",
        certification: newCert
      };
    } catch (error) {
      if (error.code === "ERR_NETWORK" || !error.response) {
        console.warn("Backend offline. Saving certification to localStorage fallback.");
        const newCert = {
          id: "c_user_" + Date.now(),
          title: certificationData.title,
          issuer: certificationData.issuer,
          credential_id: certificationData.credential_id || "",
          issue_date: certificationData.issue_date,
          expiry_date: certificationData.expiry_date || "",
          verification_link: certificationData.verification_link || "",
          status: "Pending",
          submitted_date: new Date().toISOString().split("T")[0]
        };

        const submissions = getSubmissions(registerNo);
        submissions.certifications.push(newCert);
        saveSubmissions(registerNo, submissions);

        return {
          success: true,
          message: "Certification submitted locally (Offline Fallback).",
          certification: newCert
        };
      }
      throw error;
    }
  },

  submitAchievement: async (achievementData) => {
    const registerNo = achievementData.registerNo || "22AD001";
    
    try {
      const formData = new FormData();
      formData.append("title", achievementData.title);
      formData.append("achievement_type", achievementData.type || achievementData.achievement_type || "Other");
      formData.append("organization", achievementData.organization || achievementData.event || "");
      formData.append("description", achievementData.description);
      formData.append("achievement_date", achievementData.date || achievementData.achievement_date);
      formData.append("proof_link", achievementData.proof_link || "");
      
      const fileObj = achievementData.file || achievementData.proof_file;
      if (fileObj) {
        formData.append("file", fileObj);
      }

      const response = await api.post("/student/achievements", formData, {
        headers: { "Content-Type": "multipart/form-data" }
      });
      const newAchievement = response.data;

      const submissions = getSubmissions(registerNo);
      submissions.achievements.push(newAchievement);
      saveSubmissions(registerNo, submissions);

      return {
        success: true,
        message: "Achievement submitted for mentor review.",
        achievement: newAchievement
      };
    } catch (error) {
      if (error.code === "ERR_NETWORK" || !error.response) {
        console.warn("Backend offline. Saving achievement to localStorage fallback.");
        const newAchievement = {
          id: "a_user_" + Date.now(),
          title: achievementData.title,
          type: achievementData.type || "Other",
          description: achievementData.description,
          event: achievementData.event || "",
          date: achievementData.date,
          proof_link: achievementData.proof_link || "",
          status: "Pending",
          submitted_date: new Date().toISOString().split("T")[0]
        };

        const submissions = getSubmissions(registerNo);
        submissions.achievements.push(newAchievement);
        saveSubmissions(registerNo, submissions);

        return {
          success: true,
          message: "Achievement submitted locally (Offline Fallback).",
          achievement: newAchievement
        };
      }
      throw error;
    }
  },

  getUserSubmissions: (registerNo) => {
    return getSubmissions(registerNo);
  },

  removeProject: (registerNo, projectId) => {
    const submissions = getSubmissions(registerNo);
    submissions.projects = submissions.projects.filter(p => p.id !== projectId);
    saveSubmissions(registerNo, submissions);
    return { success: true };
  },
  
  removeCertification: (registerNo, certId) => {
    const submissions = getSubmissions(registerNo);
    submissions.certifications = submissions.certifications.filter(c => c.id !== certId);
    saveSubmissions(registerNo, submissions);
    return { success: true };
  },

  removeAchievement: (registerNo, achId) => {
    const submissions = getSubmissions(registerNo);
    submissions.achievements = submissions.achievements.filter(a => a.id !== achId);
    saveSubmissions(registerNo, submissions);
    return { success: true };
  },

  updateProject: (registerNo, updatedProject) => {
    const submissions = getSubmissions(registerNo);
    submissions.projects = submissions.projects.map(p => p.id === updatedProject.id ? {
      ...p,
      ...updatedProject,
      tech_stack: Array.isArray(updatedProject.tech_stack) 
        ? updatedProject.tech_stack 
        : updatedProject.tech_stack.split(",").map(s => s.trim()).filter(Boolean)
    } : p);
    saveSubmissions(registerNo, submissions);
    return { success: true };
  },

  updateCertification: (registerNo, updatedCert) => {
    const submissions = getSubmissions(registerNo);
    submissions.certifications = submissions.certifications.map(c => c.id === updatedCert.id ? {
      ...c,
      ...updatedCert
    } : c);
    saveSubmissions(registerNo, submissions);
    return { success: true };
  },

  updateAchievement: (registerNo, updatedAch) => {
    const submissions = getSubmissions(registerNo);
    submissions.achievements = submissions.achievements.map(a => a.id === updatedAch.id ? {
      ...a,
      ...updatedAch
    } : a);
    saveSubmissions(registerNo, submissions);
    return { success: true };
  }
};
