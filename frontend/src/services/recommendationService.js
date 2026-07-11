import api from "./api";
import { mockStudents } from "../data/mockStudents";

export const recommendationService = {
  getDomainRecommendations: async (domain, limit) => {
    try {
      const response = await api.get(`/students/recommend?domain=${domain}&limit=${limit}`);
      return response.data;
    } catch (error) {
      console.warn(`Recommendation API failed for domain=${domain}, limit=${limit}. Returning mock recommendations:`, error.message);
      
      const category = domain || "Overall";
      let sortedList = [];

      if (category.toLowerCase() === "overall") {
        sortedList = [...mockStudents].sort((a, b) => b.overall_score - a.overall_score);
      } else {
        sortedList = [...mockStudents].sort((a, b) => b.domain_scores[category] - a.domain_scores[category]);
      }

      // Limit results
      const limitedList = sortedList.slice(0, Number(limit) || 5);

      // Map to the required table fields
      return limitedList.map((student, index) => {
        const domainScore = category.toLowerCase() === "overall" ? student.overall_score : student.domain_scores[category];
        
        let strengthLevel = "Moderate";
        if (domainScore >= 90) strengthLevel = "Elite";
        else if (domainScore >= 80) strengthLevel = "High";

        let reason = "";
        if (category.toLowerCase() === "overall") {
          reason = `Secured an excellent cumulative average of ${student.overall_score}% across all subjects.`;
        } else {
          reason = `Demonstrated top-tier capability in ${category} with a domain score of ${domainScore}%.`;
        }

        return {
          rank: index + 1,
          id: student.id,
          register_no: student.register_no,
          name: student.name,
          domain_score: domainScore,
          overall_score: student.overall_score,
          strength_level: strengthLevel,
          reason: reason
        };
      });
    }
  }
};
