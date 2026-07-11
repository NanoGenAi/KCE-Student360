import api from "./api";

export const resumeService = {
  getResumeData: async (registerNo) => {
    const response = await api.get(`/students/${registerNo}/resume`);
    const res = response.data;
    // Map to camelCase properties expected by the frontend form
    return {
      id: res.id,
      fileName: res.file_name || res.fileName || "",
      fileUrl: res.file_url || res.fileUrl || "",
      uploadedAt: res.updated_at || res.uploadedAt || "",
      resumeTitle: res.resume_title || res.resumeTitle || "",
      careerObjective: res.career_objective || res.careerObjective || "",
      primaryRole: res.preferred_role || res.preferredRole || res.primaryRole || "",
      keySkills: res.key_skills || res.keySkills || [],
      githubUrl: res.github_url || res.githubUrl || "",
      linkedinUrl: res.linkedin_url || res.linkedinUrl || "",
      portfolioUrl: res.portfolio_url || res.portfolioUrl || "",
      preferredJobRole: res.preferred_role || res.preferredRole || res.preferredJobRole || "",
      useInPortfolio: res.use_in_portfolio || res.useInPortfolio || false
    };
  },

  saveResumeData: async (registerNo, data) => {
    const payload = {
      resume_title: data.resumeTitle || data.resume_title || "Default Title",
      preferred_role: data.preferredJobRole || data.preferred_role || data.primaryRole || "",
      career_objective: data.careerObjective || data.career_objective || "",
      key_skills: data.keySkills || data.key_skills || [],
      github_url: data.githubUrl || data.github_url || "",
      linkedin_url: data.linkedinUrl || data.linkedin_url || "",
      portfolio_url: data.portfolioUrl || data.portfolio_url || "",
      use_in_portfolio: data.useInPortfolio !== undefined ? data.useInPortfolio : (data.use_in_portfolio !== undefined ? data.use_in_portfolio : false)
    };
    const response = await api.post(`/students/${registerNo}/resume`, payload);
    const res = response.data;
    return {
      id: res.id,
      fileName: res.file_name || res.fileName || "",
      fileUrl: res.file_url || res.fileUrl || "",
      uploadedAt: res.updated_at || res.uploadedAt || "",
      resumeTitle: res.resume_title || res.resumeTitle || "",
      careerObjective: res.career_objective || res.careerObjective || "",
      primaryRole: res.preferred_role || res.preferredRole || res.primaryRole || "",
      keySkills: res.key_skills || res.keySkills || [],
      githubUrl: res.github_url || res.githubUrl || "",
      linkedinUrl: res.linkedin_url || res.linkedinUrl || "",
      portfolioUrl: res.portfolio_url || res.portfolioUrl || "",
      preferredJobRole: res.preferred_role || res.preferredRole || res.preferredJobRole || "",
      useInPortfolio: res.use_in_portfolio || res.useInPortfolio || false
    };
  },

  uploadResume: async (registerNo, file) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("resume_title", file.name);

    const response = await api.post(`/students/${registerNo}/resume`, formData, {
      headers: {
        "Content-Type": "multipart/form-data"
      }
    });
    const res = response.data;
    return {
      id: res.id,
      fileName: res.file_name || res.fileName || "",
      fileUrl: res.file_url || res.fileUrl || "",
      uploadedAt: res.updated_at || res.uploadedAt || "",
      resumeTitle: res.resume_title || res.resumeTitle || "",
      careerObjective: res.career_objective || res.careerObjective || "",
      primaryRole: res.preferred_role || res.preferredRole || res.primaryRole || "",
      keySkills: res.key_skills || res.keySkills || [],
      githubUrl: res.github_url || res.githubUrl || "",
      linkedinUrl: res.linkedin_url || res.linkedinUrl || "",
      portfolioUrl: res.portfolio_url || res.portfolioUrl || "",
      preferredJobRole: res.preferred_role || res.preferredRole || res.preferredJobRole || "",
      useInPortfolio: res.use_in_portfolio || res.useInPortfolio || false
    };
  }
};

export default resumeService;
