# Student360 – Centralized Student Intelligence & Portfolio Platform

This repository contains the frontend implementation of **Student360**, a Centralized Student Intelligence & Portfolio Platform. This platform is designed to track student performance across coding, academics, aptitude, and key technical domains, manage mentor approvals, and build premium public developer portfolios for students.

---

## 2. Frontend Purpose

The frontend is built to provide an interactive dashboard and portfolio system for students, faculty, mentors, and administrators. 
- **Current Status:** It runs entirely on the client side using structured mock data, localized state management via **LocalStorage**, and modular service layers. 
- **Backend Readiness:** All network calls are abstracted into frontend services (`src/services/*`) with clean interfaces, making it ready to be integrated with a FastAPI and PostgreSQL backend.

---

## 3. Tech Stack Used

- **Framework:** React.js (v18+)
- **Build Tool:** Vite
- **Styling:** Tailwind CSS (Vanilla CSS & Tailwind Utility Classes)
- **UI Components:** custom shadcn-style component architectures
- **Routing:** React Router DOM (v6+)
- **HTTP Client:** Axios (configured in `api.js`)
- **Data Visualization:** Recharts (Radar, Line, Bar, and Area charts)
- **Iconography:** Lucide React Icons
- **Language:** JavaScript (ES6+)
- **Storage:** LocalStorage (for session persistence and offline edits)
- **Mock Data:** Local JS files acting as a database seed

---

## 4. Current Project Status

The frontend is fully operational as a **high-fidelity prototype** and demo application. Users can login as different roles, perform profile updates, upload score files, submit certifications/projects for approval, approve/reject submissions as mentors, customize portfolios, and ask questions to the Floating AI Assistant. All features persist state using LocalStorage so that a refresh does not clear demo data.

---

## 5. Available Demo Roles

To facilitate testing and walkthroughs, the system provides five pre-configured demo roles:

1. **Admin:**
   - Full system management.
   - Manages students, faculty, mentors, and users.
   - Assigns mentors to students and views system-wide statistics.
2. **Faculty:**
   - Performance evaluation.
   - Uploads student assessment scores via Excel templates.
   - Views overall students list, leaderboard rankings, and AI-driven placement recommendations.
3. **Mentor:**
   - Verification and approvals.
   - Monitors assigned students' academic progress.
   - Reviews and approves student-submitted projects, certifications, and achievements.
4. **Student:**
   - Career progression.
   - Views individual performance analytics, submits records for mentor validation, manages resume details, and customizes their public portfolio page.
5. **Placement Mentor:**
   - Placement intelligence.
   - Accesses targeted recommendations and filtering tools to identify high-performing students for recruiting companies.

---

## 6. Folder Structure

Below is the directory structure of the frontend:

```
frontend/
├── public/                 # Static assets
├── src/
│   ├── assets/             # Images, logos, and global styles
│   ├── components/         # Reusable UI component modules
│   │   ├── admin/          # Admin modals and configuration overlays
│   │   ├── ai/             # Floating AI Faculty Assistant components
│   │   ├── common/         # Layout essentials (Sidebar, Navbar, DataTable, Badges)
│   │   ├── dashboard/      # Role-specific dashboard widget items
│   │   └── students/       # Sub-tabs and profile management forms
│   ├── context/            # React context providers (e.g., AuthContext)
│   ├── data/               # Mock data files acting as frontend database
│   │   ├── mockApprovals.js
│   │   ├── mockLeaderboard.js
│   │   ├── mockPerformance.js
│   │   ├── mockPortfolio.js
│   │   ├── mockStudents.js
│   │   └── mockUsers.js
│   ├── hooks/              # Custom React hooks
│   ├── layouts/            # Dashboard and base layout shells
│   ├── pages/              # High-level route views (Login, Profile, Dashboards, Leaderboard, etc.)
│   ├── services/           # Service layer files abstracting API calls
│   ├── App.css             # Global stylesheet
│   ├── App.jsx             # Route definitions and application shell
│   ├── index.css           # Tailwind directives and CSS variables
│   └── main.jsx            # Application entry point
├── package.json
├── tailwind.config.js
└── vite.config.js
```

---

## 7. How to Run the Frontend

Ensure you have [Node.js](https://nodejs.org/) installed (v18+ recommended).

1. **Navigate to the frontend folder:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm run dev
   ```

4. **Build the production bundle:**
   ```bash
   npm run build
   ```

5. **Preview the production build locally:**
   ```bash
   npm run preview
   ```

---

## 8. Login System

The **Login Page** (`src/pages/LoginPage.jsx`) features a modern, clean interface with a credentials login form. For development and demo purposes, it includes a **Quick Demo Login** section that allows teammates to log in with a single click as any of the roles:
- **Admin**
- **Faculty**
- **Mentor**
- **Student**
- **Placement Mentor**

The system authenticates the user locally via `authService.js` and stores the active session in `localStorage` under the key `student360_user`.

---

## 9. Role-Based Dashboard System

Upon login, users are routed through a dynamic layout switcher. The system evaluates the active user's role and displays the corresponding dashboard interface. Dashboards are customized with widgets, KPI cards, and custom data streams relevant only to that role.

---

## 10. Sidebar Navigation

The navigation menu adapts dynamically to the logged-in user's role:

* **Admin Sidebar:**
  - Dashboard
  - Manage Students
  - Manage Faculty
  - Manage Mentors
  - Assign Mentor
  - Manage Users
  - System Overview

* **Faculty Sidebar:**
  - Dashboard
  - Students
  - Leaderboard
  - Recommendations
  - Upload Scores

* **Mentor Sidebar:**
  - Dashboard
  - Students
  - Mentor Approvals
  - Leaderboard

* **Student Sidebar:**
  - Dashboard
  - Leaderboard
  - My Performance
  - My Projects
  - My Certifications
  - My Achievements
  - My Resume
  - My Portfolio

* **Placement Mentor Sidebar:**
  - Dashboard
  - Students
  - Leaderboard
  - Recommendations

> [!IMPORTANT]
> **My Profile** and **Logout** actions are accessible exclusively from the top-right avatar dropdown, keeping the sidebar navigation focused and clean.

---

## 11. Top-Right Avatar Dropdown

The navigation bar features a top-right avatar dropdown available to all roles.
- **Options Included:** `My Profile` and `Logout`.
- **Avatar Rendering Logic:**
  - If a user has uploaded a custom profile picture, it renders the custom image.
  - If no custom image is found, it dynamically renders the user's initials (e.g., "S" or "JD") over a colored background.
  - Built-in error boundaries prevent broken image icons by checking the image file path before rendering.

---

## 12. Admin Dashboard

Provides overall student and user analytics:
- **KPI Metrics:** Total Students, Active Faculty, Assigned Mentors, Total Users.
- **Manage Modules:** Includes interactive modal overlays (`AdminModals.jsx`) to create, update, or remove student profiles, faculty members, and mentors.
- **Mentor Assignment Tool:** Enables admins to pair students with specific mentors.

---

## 13. Faculty Dashboard

Tailored to help teachers monitor their students:
- **Overview Metrics:** Average Batch Score, Placement Readiness Rate, Pending Submissions.
- **Searchable Students Table:** Search, filter, and view student lists by department, section, and overall performance.
- **Quick Links:** Quick access to the Score Upload tool and Recommendation engine.

---

## 14. Mentor Dashboard

Designed for academic guidance:
- **My Students Grid:** Shows students assigned to the mentor with their overall performance indicators.
- **Approvals Summary Widget:** Alerts the mentor on pending projects, certifications, and achievements submissions.
- **Quick Navigation:** Jump straight to review student request details.

---

## 15. Student Dashboard

Focuses on student progression and career metrics:
- **Overall Grade Card:** Visualizes CGPA/Score, strong/weak areas, and placement readiness.
- **Radar Performance Chart:** Renders the student's score across 7 domains (DSA, DBMS, FullStack, Aptitude, Coding, Academic, Technical).
- **Submissions Tracker:** Shows status updates (Pending, Approved, Rejected, Revision) for certifications and projects.

---

## 16. Upload Scores Page

Located at `/upload-scores`, this page allows Faculty to upload student scores.
- **Expected Excel Template Headers:**
  `Register No | Student Name | Assessment Name | Category | Score | Max Marks | Date`
- **Supported Score Categories:**
  `DSA`, `DBMS`, `FullStack`, `Aptitude`, `Coding`, `Academic`, `Technical`
- **Mock Implementation:** The page parses dummy text files or mock inputs and saves them into the local state.
- **Planned Backend Endpoint:** `POST /scores/upload`

---

## 17. Leaderboard Page

A centralized, responsive leaderboard for the entire batch.
- **Filters:** `Overall Batch`, `DSA`, `DBMS`, `FullStack`, `Aptitude`, `Coding`, `Academic`, `Technical`
- **Top 3 Podium:** Highlights the top three students with a custom visual (Rank 1 in center, Rank 2 on the left, Rank 3 on the right).
- **Table View:** Displays rankings, avatar/initials, register numbers, department, specific domain scores, and overall scores.
- **Actions:** View Student Details or view their Public Portfolio directly.
- **Planned Backend Endpoints:**
  - `GET /leaderboard/overall`
  - `GET /leaderboard/domain/{domain}`

---

## 18. Recommendation Page

Allows Faculty and Placement Mentors to generate lists of students ready for job descriptions.
- **Inputs:**
  - Domain selector (e.g., DSA, DBMS, FullStack)
  - Limit input (e.g., 5, 10, 20)
  - Generate button
- **Use Cases:** Generate "Top 10 DSA Students", "Top 5 DBMS Students", etc.
- **Planned Backend Endpoint:** `GET /students/recommend?domain={domain}&limit={limit}`

---

## 19. Student Profile Page

A robust tabbed profile interface containing detailed student portfolios.
- **Navigation Tabs:** Overview, About Me, Performance, Projects, Certifications, Achievements, Resume.

---

## 20. About Me Tab

Displays the student's personal details.
- **Default Profile Headline:** `AI & DS Student | Java Full Stack Developer | Aspiring AI Engineer`
- **Default Biography (About Me):**
  > I am Shahul, an Artificial Intelligence and Data Science student at Karpagam College of Engineering. I am passionate about building useful software solutions that combine AI, full stack development, and real-world problem solving.
  >
  > I have experience working on projects related to student performance tracking, AI-based systems, portfolio generation, deepfake detection, and offline AI applications. I enjoy learning new technologies and applying them to create practical projects that can help students, institutions, and users in real life.
  >
  > My goal is to become a skilled AI Engineer and Java Full Stack Developer by continuously improving my programming, problem-solving, and project development skills.
- **Default Career Objective:**
  > To build a strong career as an AI Engineer and Java Full Stack Developer by using my knowledge in Artificial Intelligence, Data Science, and software development to create innovative, practical, and impactful solutions. I aim to continuously improve my technical skills, work on real-world projects, and contribute effectively to organizations through problem-solving, teamwork, and continuous learning.
- **Skills Summary tags:**
  `AI & Data Science`, `Java`, `React`, `Full Stack Development`, `Python`, `DSA`, `DBMS`, `FastAPI`, `PostgreSQL`

---

## 21. Performance Tab

This tab displays comprehensive performance analytics:
- **Performance Summary Cards:** Overall rating, strong and weak areas, and CGPA.
- **Domain Performance Overview:** Skill levels mapping the 7 performance domains.
- **Assessment Progress Trend:** Interactive line charts mapping performance over time.
- **Domain Breakdown Table:** Detailed granular list of scores.
- **Complete Assessment History:** Historic records of internal/external coding evaluations.
- **Strength and Weakness Analysis:** Identifies subjects requiring focus.
- **Placement Readiness Analysis:**
  - `85 and above` = **Placement Ready**
  - `70 to 84` = **Almost Ready**
  - `Below 70` = **Needs Training**
- **Recommended Improvement Plan:** Auto-generated action items based on scores.
- **AI Performance Summary:** Text synthesis explaining student capabilities.
- **Faculty/Mentor Notes Preview:** Section showing comments left by teachers or mentors.

### Performance Grading Scale
- **90 and above:** `Excellent`
- **80 to 89:** `Good`
- **70 to 79:** `Needs Improvement`
- **Below 70:** `Critical`

---

## 22. Projects Tab

Lists the projects submitted by the student, showing:
- Project Name, Role, Technologies Used, GitHub URL, and Live Link.
- Status badge reflecting verification status.

---

## 23. Certifications Tab

Displays technical course verifications:
- Certificate Title, Issuing Organization, Date Issued, Credential ID, and credential URL link.

---

## 24. Achievements Tab

Contains awards, competitive programming achievements, hackathons won, and key extra-curricular awards with verification links.

---

## 25. Resume Tab

Allows students to manage their job application files, preferred career role, social links (GitHub, LinkedIn), and decide if their resume link should be shown publicly.

---

## 26. Student Submissions

Students can submit new **Projects**, **Certifications**, and **Achievements** via submission forms. 
- Submissions default to a `Pending` status.
- Once submitted, they appear in their assigned Mentor's Dashboard for review.

---

## 27. Mentor Approval Flow

Mentors can navigate to the "Mentor Approvals" page to view pending requests:
- **Action Buttons:** The mentor can review details and mark submissions as:
  - `Approved`
  - `Rejected`
  - `Correction Required` (or `Revision Requested`)
- Actions instantly update the student's dashboard logs via local state persistence.

---

## 28. Resume Feature

The Resume manager (`resumeService.js`) handles portfolio resume configs.
- **Supported Fields:** Resume file (PDF link/file upload), Resume Title, Preferred Role, Career Objective, Key Skills list, GitHub/LinkedIn/Portfolio URLs, and "Use in portfolio" toggle.
- **Navigation Safety:** The resume button is designed to avoid broken `/portfolio/{resumeFileName}` file routing issues by utilizing local storage/mock state URLs directly.

---

## 29. My Profile Feature

Accessible via the top-right avatar dropdown, this feature opens a settings panel:
- **Supported roles:** Student, Faculty, Mentor, Admin, Placement Mentor.
- **Fields:** Full Name, Email, Phone, Role, Department, Location, Profile Image, and Role-specific details.
- **Profile Image Priority Order:**
  1. Profile image saved in LocalStorage.
  2. `currentUser.profileImage`
  3. `currentUser.profile_image`
  4. `student.profileImage`
  5. `student.profile_image`
  6. Initials fallback avatar.

---

## 30. Public Portfolio Page

Route: `/portfolio/:registerNo`

The public portfolio features a **premium dark developer-style theme** that showcases students to potential recruiters.
- **Theme Design:** Dark starry background, purple glow effects, and modern typography.
- **Sections Included:**
  - **Hero Section:** Large student name with an animated typing cursor effect.
  - **Profile Card:** Shows avatar (with initials fallback), CGPA badge, and personal details.
  - **Tech Stack Strip:** Scrolling/grid view of core programming skills.
  - **About:** Displays student headline and biography details.
  - **Performance:** Interactive charts and breakdown of the 7 performance domains.
  - **Resume:** Easy-download resume CTA.
  - **Projects & Certifications:** Carousel/grid displaying verified submissions.
  - **Achievements:** Timeline of awards.
  - **Contact Section:** Recruiter-focused Call to Action (CTA) and contact form.
- **Security:** Renders only verified or mentor-approved data.

---

## 31. Portfolio Customization

Students can customize their public portfolio style:
- Toggle sections (e.g., hide/show Achievements).
- Select active accent colors (e.g., Purple, Blue, Emerald).
- Change their layout theme configuration via `portfolioCustomizationService.js`.

---

## 32. Floating AI Faculty Assistant

A floating chatbot assistant located in the bottom-right corner of the screen.
- **Availability:** Visible for Faculty, Mentor, Admin, and Placement Mentors. It is automatically hidden on Student pages, Login pages, and Public Portfolios.
- **Supported Queries:**
  - *"Top 10 DSA students"*
  - *"Top 10 FullStack students"*
  - *"Top 10 DBMS students"*
  - *"Overall toppers"*
  - *"Students for placement"*
- Uses simulated Natural Language Processing via `facultyAssistantService.js` to return charts, tables, and listings of relevant students from mock data.
- **Planned Backend Endpoint:** `POST /ai/faculty-query`

---

## 33. Mock Data

To enable runtime interaction, the project includes these structured datasets under `src/data/`:
- `mockStudents.js`: Detailed records of student profiles, departments, sections, and general info.
- `mockPerformance.js`: Historical scores, category grades, and progress over time.
- `mockUsers.js`: Predefined login accounts and password matches for demo roles.
- `mockApprovals.js`: Default approval requests from students to seed the Mentor view.
- `mockLeaderboard.js`: Aggregate records used to build top-3 podiums and tables.

---

## 34. LocalStorage Usage

LocalStorage is utilized to persist demo inputs across page refreshes.
* **Key Keys Used:**
  - `student360_user`: Stores the current authenticated user session.
  - `student360_profile_${role}_${userId}`: Custom profile settings.
  - `student360_resume_${registerNo}`: Resume details.
  - `student360_about_profile_${registerNo}`: Custom About Me headline and text.
  - `student360_portfolio_customization_${registerNo}`: Portfolio show/hide layouts.

---

## 35. Frontend Services

Modular service scripts in `src/services/` wrap application logic and return Promises, simplifying API substitution later:
- `api.js`: Axios client configuration.
- `authService.js`: Sign-in, session storage, and logout.
- `studentService.js`: Resolves student records and profile attributes.
- `leaderboardService.js`: Pulls ranking lists filtered by domain.
- `recommendationService.js`: Resolves placement matching results.
- `uploadService.js`: Handles document and score uploads.
- `mentorService.js`: Manages assigned student and review lists.
- `profileService.js`: Saves edits to user and student details.
- `resumeService.js`: Updates resume link fields and configs.
- `portfolioService.js`: Resolves details for the public portfolio route.
- `portfolioCustomizationService.js`: Saves public portfolio layouts.
- `studentSubmissionService.js`: Processes submissions for validation.
- `facultyAssistantService.js`: Processes AI chat prompts.

---

## 36. Backend API Contract Prepared

The frontend services are mapped to work with the following planned backend endpoints:

### Authentication
* `POST /auth/login` - Authenticate users.
* `GET /auth/me` - Retrieve active session profiles.

### Students & Academics
* `GET /students` - List all students.
* `GET /students/{id}` - Details of a student.
* `GET /students/{id}/performance` - Performance history and domain scores.
* `POST /scores/upload` - File upload for evaluation sheets.

### Leaderboard & Recommendations
* `GET /leaderboard/overall` - Get overall rankings.
* `GET /leaderboard/domain/{domain}` - Get domain rankings.
* `GET /students/recommend?domain={domain}&limit={limit}` - Query top students.

### Submissions & Approvals
* `GET /mentor/pending` - Fetch pending approvals.
* `PUT /mentor/review` - Approve or reject specific requests.
* `POST /student/projects` - Submit new project.
* `POST /student/certifications` - Submit new certification.
* `POST /student/achievements` - Submit new achievement.

### Profiles & Resumes
* `GET /users/me/profile` - Fetch profile metadata.
* `PUT /users/me/profile` - Save edited profile fields.
* `POST /users/me/profile-image` - File upload for profile avatar.
* `GET /students/{register_no}/resume` - Retrieve student resume data.
* `POST /students/{register_no}/resume` - Upload resume.
* `PUT /students/{register_no}/resume` - Edit resume properties.

### Portfolio & Customization
* `GET /portfolio/{register_no}` - Retrieve public portfolio details.
* `GET /portfolio/customization/{registerNo}` - Retrieve layout parameters.
* `PUT /portfolio/customization/{registerNo}` - Edit active sections.

### AI Assistant
* `POST /ai/faculty-query` - Send chat prompt to the AI agent.
* `POST /ai/generate-summary` - Synthesize student profile metrics.

---

## 37. Important Frontend Decisions

1. **Avatar Resilience:** To prevent broken image tags, we implemented an absolute priority lookup that falls back gracefully to user initials.
2. **LocalStorage Fallback:** Ensures immediate feedback for form actions (submitting projects, customizing portfolios) without requiring an active API connection.
3. **Typing and Purple Aesthetic:** The public portfolio page utilizes custom dark CSS layers and neon accents to provide an attractive recruiter interface.
4. **Service Abstraction:** By importing services instead of inline Axios queries, backend development can be performed with zero modifications to React UI files.

---

## 38. Current Completed Frontend Modules

| Module | Status |
| :--- | :--- |
| Login Page | Completed |
| Demo Role Login | Completed |
| Role-Based Dashboard | Completed |
| Admin Dashboard | Completed |
| Faculty Dashboard | Completed |
| Mentor Dashboard | Completed |
| Student Dashboard | Completed |
| Placement Mentor Dashboard | Completed |
| Upload Scores Page | Completed |
| Leaderboard Page | Completed |
| Top 3 Podium | Completed |
| Recommendation Page | Completed |
| Student Profile Tabs | Completed |
| About Me Tab | Completed |
| Performance Tab | Enhanced / In Progress |
| Projects Tab | Completed |
| Certifications Tab | Completed |
| Achievements Tab | Completed |
| Resume Tab | Completed |
| Student Submissions | Completed |
| Mentor Approval Flow | Completed |
| My Profile | Completed |
| Avatar Dropdown | Completed |
| Floating AI Assistant | Completed |
| Public Portfolio | Completed |
| Portfolio Profile Image | Completed |
| Resume Integration | Completed / Mock |
| Backend Integration | Pending |

---

## 39. Pending Frontend Improvements

- Final polish of the **Performance** tab charts.
- More responsive design testing across tablet interfaces.
- Expanding mock files with more diverse student profiles.
- Implementing empty state placeholders for new students without submissions.
- Adding additional developer portfolio themes.
- Enhancing file upload previews (images, PDF documents) for student submissions.
- Code cleanup and removal of leftover test console logs.

---

## 40. Recommended Next Steps for Team

1. **Bug Fixing:** Review and complete any pending frontend styling adjustments.
2. **Layout Audit:** Ensure all sidebars load cleaner views on smaller screens.
3. **Role Validation:** Test all pre-configured credentials in the Quick Login dropdown.
4. **Sort Ordering:** Check that changing sorting tabs on the leaderboard triggers immediate rerenders.
5. **Route Check:** Verify `/portfolio/:registerNo` handles edge cases where details are incomplete.
6. **API Verification:** Compare frontend Axios structures with backend routing contracts.
7. **FastAPI Setup:** Initialize the Python backend directory structure.
8. **DB Integration:** Configure PostgreSQL schema mapping student, score, and submission structures.
9. **Endpoint Migration:** Step-by-step update of frontend services to route actual REST calls instead of LocalStorage variables.

---

## 41. Frontend Demo Flow

Use this step-by-step flow to present the app during sprint reviews:

1. **Login Page:** Launch `npm run dev`, open the browser, and display the dropdown credentials.
2. **Student Dashboard:** Log in as **Student** (e.g., Shahul). Show the Radar skill charts.
3. **Performance & Tabs:** Click on "My Performance", "My Projects", "My Certifications", and "My Achievements".
4. **Resume Manager:** Open the "My Resume" tab and toggle portfolio visibility options.
5. **Public Portfolio:** Click the "My Portfolio" sidebar link to view the dark theme view under `/portfolio/12345`.
6. **Log out:** Use the top-right avatar dropdown menu to log out.
7. **Faculty Dashboard:** Log in as **Faculty**. View student lists, the overall performance widgets, and open **Upload Scores**.
8. **Leaderboard:** Access the "Leaderboard" tab, toggle between *Overall*, *DSA*, or *FullStack* to watch the top 3 podium change position dynamically.
9. **Recommendations:** Enter "FullStack" with a limit of "10" and click generate to query elite candidates.
10. **Log out:** Log out via the avatar dropdown.
11. **Mentor Dashboard:** Log in as **Mentor**. Open the "Mentor Approvals" page. Find the pending student submission and click **Approve**.
12. **Log out & Admin Check:** Log in as **Admin** to show system overview charts and assignment interfaces.

---

## 42. Project Summary

Student360 is currently a production-ready client interface. By abstracting data access through clean service definitions, we have structured the workspace so that back-end developers can easily connect actual database tables without disrupting the premium visual style of the application.
