import React, { useState, useEffect } from "react";
import { Outlet, Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";
import Sidebar from "../components/common/Sidebar";
import Navbar from "../components/common/Navbar";
import LoadingSpinner from "../components/common/LoadingSpinner";
import FacultyChatbot from "../components/ai/FacultyChatbot";
import { KCE_LOGO_URL, KCE_LOGO_ALT } from "../config/branding";

export const DashboardLayout = () => {
  const { user, loading, isAuthenticated } = useAuth();
  const location = useLocation();
  const [dateTimeStr, setDateTimeStr] = useState("");

  // Update date/time dynamically every second
  useEffect(() => {
    const tick = () => {
      const now = new Date();
      setDateTimeStr(
        now.toLocaleDateString("en-US", {
          weekday: "short",
          month: "short",
          day: "numeric",
          year: "numeric"
        }) + " " + now.toLocaleTimeString("en-US", {
          hour: "2-digit",
          minute: "2-digit",
          hour12: true
        })
      );
    };
    tick();
    const interval = setInterval(tick, 60000); // 1-minute is sufficient and clean for layout ticker
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="h-screen w-screen flex items-center justify-center bg-[#F7F7F7]">
        <LoadingSpinner size="lg" text="Authenticating session..." />
      </div>
    );
  }

  // Redirect to login if not authenticated
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // Set navbar title based on route location
  const getPageTitle = (pathname) => {
    if (pathname.includes("/students/") || pathname.includes("/student/")) return "Student Details";
    if (pathname === "/students") return "Student Intelligence Directory";
    if (pathname === "/leaderboard") return "Student Leaderboard";
    if (pathname === "/recommendations") return "Talent Domain Recommendations";
    if (pathname === "/upload-scores") return "Excel Score Ingestion";
    if (pathname === "/mentor/approvals") return "Achievements Verification Center";
    if (pathname.includes("/portfolio/")) return "Verified Portfolio Profile";
    return "Institutional Analytics Dashboard";
  };

  return (
    <div className="min-h-screen bg-[#F7F7F7] flex flex-col font-sans text-[#111827]">
      {/* Top Institutional Header */}
      <header className="bg-white border-t-[4px] border-[#C76F2B] border-b border-[#D1D5DB] px-6 py-2.5 flex items-center justify-between z-30 shadow-none">
        {/* Left: KCE Banner Image / Text Fallback */}
        <div className="flex items-center">
          <img
            src={KCE_LOGO_URL}
            alt={KCE_LOGO_ALT}
            className="kce-header-logo"
            onError={(e) => {
              console.error("KCE Header Logo failed to load:", KCE_LOGO_URL);
              e.currentTarget.style.display = "none";
              const fallback = e.currentTarget.nextElementSibling;
              if (fallback) fallback.style.display = "block";
            }}
          />
          <div style={{ display: "none" }} className="border-l-4 border-[#C76F2B] pl-3">
            <h1 className="text-sm font-black tracking-wide text-[#214C55] leading-none uppercase">
              Karpagam College of Engineering
            </h1>
            <p className="text-[10px] font-bold text-[#6B7280] tracking-wider uppercase mt-1 leading-none">
              Student360 Internal Portal
            </p>
          </div>
        </div>

        {/* Right: Role & Ticker */}
        <div className="flex items-center space-x-6">
          <div className="text-right">
            <span className="text-[10px] font-extrabold text-[#214C55] uppercase tracking-wider block">
              Logged as: <span className="text-[#C76F2B] font-black">{user?.role?.replace("_", " ")}</span>
            </span>
            <span className="text-[10px] text-[#6B7280] font-bold block">{user?.name}</span>
          </div>
          <div className="text-xs font-bold text-[#214C55] border-l border-[#D1D5DB] pl-6 hidden md:block select-none">
            {dateTimeStr}
          </div>
        </div>
      </header>

      {/* Main Layout Body wrapper */}
      <div className="flex-1 flex min-h-0">
        {/* Sidebar Navigation */}
        <Sidebar />

        {/* Content Area */}
        <div className="flex-1 flex flex-col min-w-0 bg-[#F7F7F7]">
          {/* Subpage Header Navbar */}
          <Navbar title={getPageTitle(location.pathname)} />

          {/* Dashboard Pages Content */}
          <main className="p-6 md:p-8 flex-1 overflow-y-auto bg-[#F7F7F7]">
            <Outlet />
          </main>
        </div>
      </div>
      {/* Floating assistant chatbot */}
      {user?.role !== "student" && <FacultyChatbot />}
    </div>
  );
};
export default DashboardLayout;
