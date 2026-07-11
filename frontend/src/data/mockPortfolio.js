import { mockStudents } from "./mockStudents";

export const mockPortfolios = {
  "22AD001": {
    register_no: "22AD001",
    name: "Shahul",
    title: "AI & DS Student",
    avatar: "https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=150",
    about: "I am a passionate Information Technology student with a strong focus on Full Stack Web Development and Cloud Technologies. I love building highly scalable applications and solving complex algorithmic challenges. With a solid foundation in DSA and cloud deployment, I aim to create web solutions that deliver exceptional user experiences.",
    skills: ["React", "Tailwind CSS", "Node.js", "Express", "PostgreSQL", "AWS (EC2, S3, Lambda)", "Git & Github", "Python", "Data Structures"],
    projects: [
      {
        title: "E-Commerce Cloud Platform",
        description: "A serverless e-commerce platform built using React, Node.js, and AWS.",
        role: "Frontend Lead",
        tech_stack: ["React", "Tailwind CSS", "Node.js", "AWS"],
        github_link: "https://github.com/shahul/ecommerce-cloud",
        live_link: "https://ecommerce-cloud.demo.com",
        approval_status: "Approved"
      },
      {
        title: "Automated Portfolio Builder",
        description: "AI-powered tool that automatically generates portfolios for college students.",
        role: "Full Stack Developer",
        tech_stack: ["React", "Express", "PostgreSQL", "Gemini API"],
        github_link: "https://github.com/shahul/portfolio-builder",
        live_link: "https://portfolio-builder.demo.com",
        approval_status: "Pending"
      }
    ],
    certifications: [
      {
        title: "AWS Certified Developer - Associate",
        issuer: "Amazon Web Services",
        issue_date: "2025-05-15",
        approval_status: "Pending"
      },
      {
        title: "Meta Front-End Developer Professional Certificate",
        issuer: "Meta (Coursera)",
        issue_date: "2024-11-20",
        approval_status: "Approved"
      }
    ],
    achievements: [
      {
        title: "Smart India Hackathon 2025 Winner",
        description: "First prize in the Ministry of Education category for building a decentralized academic document verification system.",
        date: "2025-02-18",
        approval_status: "Approved"
      },
      {
        title: "LeetCode 500+ Badges",
        description: "Solved over 500 coding questions on LeetCode with a peak rating of 1850.",
        date: "2025-06-01",
        approval_status: "Approved"
      }
    ],
    academic_highlights: {
      cgpa: "9.24 / 10",
      strongest_domain: "FullStack (95/100)",
      weakest_domain: "Aptitude (75/100)",
      overall_performance_level: "Excellent",
      class_rank: "Top 5%"
    },
    contact: {
      email: "shahul@student360.com",
      linkedin: "https://linkedin.com/in/shahul-example",
      github: "https://github.com/shahul"
    },
    ai_summary: "Shahul is a high-achieving Full-Stack engineer with verified credentials in cloud solutions (AWS) and a proven track record in hackathons (SIH Winner). He ranks in the top 5% of his class with strong algorithmic competency."
  },
  "21IT002": {
    register_no: "21IT002",
    name: "Arun",
    title: "Algorithms specialist & DSA Practitioner",
    avatar: "https://images.unsplash.com/photo-1570295999919-56ceb5ecca61?w=150",
    about: "Deeply interested in core algorithms, complexity theory, and data structures. I enjoy competitive programming and optimizing software bottlenecks.",
    skills: ["Data Structures", "Algorithms", "C++", "Java", "Python", "Graph Theory", "Git"],
    projects: [
      {
        title: "Visualizing Graph Algorithms",
        description: "An interactive dashboard visualizing BFS, DFS, Dijkstra, and A* algorithms.",
        role: "Creator",
        tech_stack: ["HTML5", "CSS3", "JavaScript"],
        github_link: "https://github.com/arun/algo-vis",
        approval_status: "Approved"
      }
    ],
    certifications: [
      {
        title: "Data Structures and Algorithms",
        issuer: "NPTEL",
        issue_date: "2024-10-10",
        approval_status: "Approved"
      }
    ],
    achievements: [
      {
        title: "CodeChef Division 1",
        description: "Reached Division 1 (4-Star) on CodeChef.",
        date: "2025-04-12",
        approval_status: "Approved"
      }
    ],
    academic_highlights: {
      cgpa: "8.15 / 10",
      strongest_domain: "DSA (92/100)",
      weakest_domain: "DBMS (70/100)",
      overall_performance_level: "Very Good",
      class_rank: "Top 15%"
    },
    contact: {
      email: "arun@student360.com",
      linkedin: "https://linkedin.com/in/arun-example",
      github: "https://github.com/arun"
    },
    ai_summary: "Arun exhibits elite performance in competitive coding and algorithmic puzzle-solving, with secondary skills in scripting and networks."
  },
  "21IT003": {
    register_no: "21IT003",
    name: "Priya",
    title: "Database Architect & Systems Engineer",
    avatar: "https://images.unsplash.com/photo-1494790108377-be9c29b29330?w=150",
    about: "Detail-oriented computer science student specializing in backend architecture, relational database design, and cloud infrastructure.",
    skills: ["PostgreSQL", "MongoDB", "DBMS Design", "Next.js", "Prisma ORM", "GCP", "SQL Tuning", "Academic Research"],
    projects: [
      {
        title: "University Database Management System",
        description: "A secure and scalable DBMS system with role-based access for students and faculty.",
        role: "Database Architect",
        tech_stack: ["PostgreSQL", "Next.js", "Prisma"],
        github_link: "https://github.com/priya/db-project",
        approval_status: "Approved"
      }
    ],
    certifications: [
      {
        title: "Google Cloud Certified Professional Cloud Architect",
        issuer: "Google Cloud",
        issue_date: "2025-03-22",
        approval_status: "Approved"
      }
    ],
    achievements: [
      {
        title: "Department Gold Medalist",
        description: "Awarded for securing GPA of 9.8 in consecutively 4 semesters.",
        date: "2025-05-10",
        approval_status: "Approved"
      }
    ],
    academic_highlights: {
      cgpa: "9.80 / 10",
      strongest_domain: "DBMS (96/100)",
      weakest_domain: "Technical (88/100)",
      overall_performance_level: "Outstanding",
      class_rank: "1st Rank"
    },
    contact: {
      email: "priya@student360.com",
      linkedin: "https://linkedin.com/in/priya-example",
      github: "https://github.com/priya"
    },
    ai_summary: "Priya is the top academic performer (1st Rank, CGPA 9.80) with a highly strong capability in Database Systems and Google Cloud integration."
  }
};

// Fallback generator for students who don't have detailed entries in mockPortfolios
export const getPortfolioData = (registerNo) => {
  if (mockPortfolios[registerNo]) {
    return mockPortfolios[registerNo];
  }
  
  // Find basic info from mockStudents
  const student = mockStudents.find(s => s.register_no === registerNo);
  if (!student) return null;
  
  return {
    register_no: student.register_no,
    name: student.name,
    title: `${student.strongest_domain} Enthusiast | Student of IT/CS`,
    avatar: `https://images.unsplash.com/photo-${1500000000000 + parseInt(student.id) * 100000}?w=150`,
    about: `I am a student of ${student.department} currently in Year ${student.year}, Section ${student.section}. My primary interests lie in ${student.strongest_domain} and related domains.`,
    skills: [student.strongest_domain, "Java", "Python", "SQL", "Web Dev", "Problem Solving"],
    projects: student.projects || [],
    certifications: student.certifications || [],
    achievements: student.achievements || [],
    academic_highlights: {
      cgpa: "8.50 / 10",
      strongest_domain: `${student.strongest_domain} (${student.domain_scores[student.strongest_domain]}/100)`,
      weakest_domain: `${student.weakest_domain} (${student.domain_scores[student.weakest_domain]}/100)`,
      overall_performance_level: student.overall_score >= 85 ? "Excellent" : "Very Good",
      class_rank: student.overall_score >= 90 ? "Top 5%" : student.overall_score >= 80 ? "Top 15%" : "Top 30%"
    },
    contact: {
      email: student.email,
      linkedin: `https://linkedin.com/in/${student.name.toLowerCase()}-example`,
      github: `https://github.com/${student.name.toLowerCase()}`
    },
    ai_summary: `${student.name} is a hardworking student with an overall score of ${student.overall_score}%. Their primary area of excellence is ${student.strongest_domain}.`
  };
};
