import { mockStudents } from "./mockStudents";

// Overall leaderboard is sorted by overall_score descending
export const mockOverallLeaderboard = [...mockStudents]
  .sort((a, b) => b.overall_score - a.overall_score)
  .map((student, index) => ({
    rank: index + 1,
    id: student.id,
    register_no: student.register_no,
    name: student.name,
    overall_score: student.overall_score,
    strongest_domain: student.strongest_domain,
    weakest_domain: student.weakest_domain
  }));

// Helper to get domain-specific leaderboard
export const getDomainLeaderboard = (domain) => {
  if (!domain || domain.toLowerCase() === "overall") {
    return mockOverallLeaderboard;
  }
  
  // Sort students by their score in the specific domain
  return [...mockStudents]
    .sort((a, b) => b.domain_scores[domain] - a.domain_scores[domain])
    .map((student, index) => ({
      rank: index + 1,
      id: student.id,
      register_no: student.register_no,
      name: student.name,
      overall_score: student.overall_score,
      domain_score: student.domain_scores[domain],
      strongest_domain: student.strongest_domain,
      weakest_domain: student.weakest_domain
    }));
};
