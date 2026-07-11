const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export const resolveImageUrl = (url, timestamp = null) => {
  if (!url || typeof url !== "string") return null;

  const cleanUrl = url.trim();
  if (!cleanUrl) return null;

  if (cleanUrl.startsWith("http://") || cleanUrl.startsWith("https://")) {
    if (cleanUrl.includes("/uploads/") && timestamp) {
      return cleanUrl.includes("?")
        ? `${cleanUrl}&t=${timestamp}`
        : `${cleanUrl}?t=${timestamp}`;
    }
    return cleanUrl;
  }

  if (cleanUrl.startsWith("data:image")) {
    return cleanUrl;
  }

  if (cleanUrl.startsWith("/leaderboard/")) {
    return cleanUrl;
  }

  if (cleanUrl.startsWith("leaderboard/")) {
    return `/${cleanUrl}`;
  }

  if (cleanUrl.startsWith("/uploads/")) {
    const resolved = `${API_BASE_URL}${cleanUrl}`;
    return timestamp ? `${resolved}?t=${timestamp}` : resolved;
  }

  if (cleanUrl.startsWith("uploads/")) {
    const resolved = `${API_BASE_URL}/${cleanUrl}`;
    return timestamp ? `${resolved}?t=${timestamp}` : resolved;
  }

  return cleanUrl.startsWith("/")
    ? `${API_BASE_URL}${cleanUrl}`
    : `${API_BASE_URL}/${cleanUrl}`;
};

export const getStudentImageUrl = (studentOrUser) => {
  if (!studentOrUser) return null;

  const timestamp = studentOrUser.profileImageUpdatedAt || studentOrUser.updatedAt || studentOrUser.updated_at || null;

  const rawUrl =
    studentOrUser.profileImage ||
    studentOrUser.profile_image ||
    studentOrUser.userProfile?.profileImage ||
    studentOrUser.userProfile?.profile_image ||
    studentOrUser.student?.profileImage ||
    studentOrUser.student?.profile_image ||
    studentOrUser.user?.profileImage ||
    studentOrUser.user?.profile_image ||
    studentOrUser.avatarUrl ||
    studentOrUser.avatar_url ||
    studentOrUser.imageUrl ||
    studentOrUser.image_url ||
    studentOrUser.avatar ||
    studentOrUser.image ||
    studentOrUser.photo ||
    null;

  return resolveImageUrl(rawUrl, timestamp);
};

export const getResumeUrl = (resume) => {
  const raw =
    resume?.resumeUrl ||
    resume?.resume_url ||
    resume?.filePath ||
    resume?.file_path ||
    resume?.url ||
    resume?.fileUrl ||
    resume?.file_url ||
    resume?.resume?.resumeUrl ||
    resume?.resume?.resume_url ||
    resume?.resume?.filePath ||
    resume?.resume?.file_path ||
    resume?.resume?.fileUrl ||
    resume?.resume?.file_url;

  if (!raw) return null;

  return resolveImageUrl(raw);
};

