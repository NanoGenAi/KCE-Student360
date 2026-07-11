import React, { useState, useEffect } from "react";
import { mentorService } from "../services/mentorService";
import LoadingSpinner from "../components/common/LoadingSpinner";
import { Check, X, RefreshCw, ExternalLink, Calendar, User, ShieldCheck, Search, Filter } from "lucide-react";

const STATUS_STYLES = {
  Pending:              "bg-amber-50 text-[#D97706] border-amber-300",
  Approved:             "bg-emerald-50 text-[#15803D] border-emerald-300",
  Rejected:             "bg-red-50 text-[#B91C1C] border-red-300",
  "Correction Required": "bg-orange-50 text-[#C76F2B] border-orange-300"
};

const TYPE_STYLES = {
  Certification: "bg-blue-50 text-[#214C55] border-blue-200",
  Project:       "bg-purple-50 text-purple-700 border-purple-200",
  Achievement:   "bg-orange-50 text-[#C76F2B] border-orange-200"
};

export const MentorApprovalPage = () => {
  const [approvals, setApprovals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [processingId, setProcessingId] = useState(null);
  const [toastMsg, setToastMsg] = useState("");

  // Inline correction feedback state
  const [activeCorrectionId, setActiveCorrectionId] = useState(null);
  const [feedbackText, setFeedbackText] = useState("");

  // Inline reject reason state
  const [activeRejectId, setActiveRejectId] = useState(null);
  const [rejectNote, setRejectNote] = useState("");

  // Filter state
  const [statusFilter, setStatusFilter] = useState("All");
  const [typeFilter, setTypeFilter] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");

  const showToast = (msg) => {
    setToastMsg(msg);
    setTimeout(() => setToastMsg(""), 3000);
  };

  const fetchAll = async () => {
    try {
      setLoading(true);
      setError("");
      const data = await mentorService.getAllApprovals();
      setApprovals(data);
    } catch (err) {
      setError("Failed to retrieve submissions list.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAll();
  }, []);

  const handleReview = async (id, type, status, feedback = "") => {
    setProcessingId(`${type}-${id}`);
    try {
      await mentorService.reviewSubmission(id, status, feedback, type);
      // Update status in-place (don't remove from list)
      setApprovals(prev =>
        prev.map(item =>
          item.id === id && item.item_type === type ? { ...item, status, feedback } : item
        )
      );
      setActiveCorrectionId(null);
      setActiveRejectId(null);
      setFeedbackText("");
      setRejectNote("");

      const messages = {
        Approved:             "Submission approved successfully.",
        Rejected:             "Submission rejected.",
        "Correction Required": "Correction requested from student."
      };
      showToast(messages[status] || `Status updated to ${status}.`);
    } catch (err) {
      showToast("Error: Failed to update submission status.");
    } finally {
      setProcessingId(null);
    }
  };

  // Filtered list
  const filteredApprovals = approvals.filter(item => {
    const matchStatus = statusFilter === "All" || item.status === statusFilter;
    const matchType   = typeFilter === "All"   || item.type === typeFilter;
    const q = searchQuery.toLowerCase();
    const matchSearch = !q || [item.student_name, item.register_no, item.title]
      .some(val => val?.toLowerCase().includes(q));
    return matchStatus && matchType && matchSearch;
  });

  const counts = {
    total:   approvals.length,
    pending: approvals.filter(i => i.status === "Pending").length,
    approved: approvals.filter(i => i.status === "Approved").length,
    rejected: approvals.filter(i => i.status === "Rejected").length,
    correction: approvals.filter(i => i.status === "Correction Required").length
  };

  return (
    <div className="space-y-6 animate-fade-in text-[#111827]">
      {/* Toast notification */}
      {toastMsg && (
        <div className="fixed top-4 right-4 z-50 bg-[#163941] text-white text-xs font-bold px-5 py-3 shadow-lg border border-[#214C55] animate-fade-in uppercase tracking-wider">
          {toastMsg}
        </div>
      )}

      {/* Header */}
      <div className="bg-[#163941] p-6 rounded-none border border-[#D1D5DB] text-white shadow-none">
        <h1 className="text-xl font-extrabold uppercase tracking-wider text-white">Credentials Verification Center</h1>
        <p className="text-xs text-[#E5E5E5] font-semibold mt-1.5 leading-relaxed">
          Review achievements, projects, and certificates submitted by students. Approve, reject, or request corrections.
        </p>
      </div>

      {/* Summary stat row */}
      {!loading && !error && (
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
          {[
            { label: "Total",      value: counts.total,      style: "border-[#D1D5DB] text-[#214C55]" },
            { label: "Pending",    value: counts.pending,    style: "border-amber-300 text-[#D97706]" },
            { label: "Approved",   value: counts.approved,   style: "border-emerald-300 text-[#15803D]" },
            { label: "Rejected",   value: counts.rejected,   style: "border-red-300 text-[#B91C1C]" },
            { label: "Correction", value: counts.correction, style: "border-orange-300 text-[#C76F2B]" }
          ].map(card => (
            <div key={card.label} className={`bg-white border ${card.style} p-3 text-center rounded-none`}>
              <span className={`text-xl font-black block ${card.style.split(" ")[1]}`}>{card.value}</span>
              <span className="text-[9px] font-extrabold text-[#6B7280] uppercase tracking-wider block mt-0.5">{card.label}</span>
            </div>
          ))}
        </div>
      )}

      {/* Filters row */}
      {!loading && !error && (
        <div className="bg-white border border-[#D1D5DB] p-4 rounded-none flex flex-col md:flex-row gap-3 items-end">
          {/* Search */}
          <div className="flex-1 space-y-1">
            <label className="text-[10px] font-extrabold text-[#6B7280] uppercase tracking-wider flex items-center gap-1">
              <Search size={11} /> Search
            </label>
            <div className="relative">
              <Search size={13} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#6B7280]" />
              <input
                type="text"
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                placeholder="Student name, register no, or title..."
                className="w-full pl-8 pr-3 py-2 text-xs border border-[#D1D5DB] focus:outline-none focus:border-[#C76F2B] font-semibold rounded-none bg-white"
              />
            </div>
          </div>

          {/* Status filter */}
          <div className="w-full md:w-44 space-y-1">
            <label className="text-[10px] font-extrabold text-[#6B7280] uppercase tracking-wider flex items-center gap-1">
              <Filter size={11} /> Status
            </label>
            <select
              value={statusFilter}
              onChange={e => setStatusFilter(e.target.value)}
              className="w-full px-3 py-2 text-xs border border-[#D1D5DB] focus:outline-none focus:border-[#C76F2B] font-bold rounded-none bg-white cursor-pointer"
            >
              {["All", "Pending", "Approved", "Rejected", "Correction Required"].map(s => (
                <option key={s} value={s}>{s}</option>
              ))}
            </select>
          </div>

          {/* Type filter */}
          <div className="w-full md:w-44 space-y-1">
            <label className="text-[10px] font-extrabold text-[#6B7280] uppercase tracking-wider flex items-center gap-1">
              <Filter size={11} /> Type
            </label>
            <select
              value={typeFilter}
              onChange={e => setTypeFilter(e.target.value)}
              className="w-full px-3 py-2 text-xs border border-[#D1D5DB] focus:outline-none focus:border-[#C76F2B] font-bold rounded-none bg-white cursor-pointer"
            >
              {["All", "Project", "Certification", "Achievement"].map(t => (
                <option key={t} value={t}>{t}</option>
              ))}
            </select>
          </div>
        </div>
      )}

      {/* Main content */}
      {loading ? (
        <LoadingSpinner size="lg" text="Retrieving student submission files..." />
      ) : error ? (
        <div className="bg-red-50 border border-red-200 text-[#B91C1C] p-4 rounded-none text-center text-xs font-bold uppercase tracking-wider max-w-md mx-auto">
          {error}
        </div>
      ) : filteredApprovals.length === 0 ? (
        <div className="bg-white border border-[#D1D5DB] rounded-none p-12 text-center space-y-3">
          <ShieldCheck size={36} className="text-[#C76F2B] mx-auto" />
          <h3 className="text-sm font-extrabold text-[#214C55] uppercase tracking-wider">No Submissions Found</h3>
          <p className="text-xs text-[#6B7280] font-semibold">
            {approvals.length === 0
              ? "There are currently no student credentials awaiting verification."
              : "No submissions match the current filters."}
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-5 animate-fade-in">
          {filteredApprovals.map(item => (
            <div
              key={`${item.item_type}-${item.id}`}
              className={`bg-white rounded-none border border-[#D1D5DB] p-5 flex flex-col justify-between space-y-4 shadow-none transition-all ${
                processingId === `${item.item_type}-${item.id}` ? "opacity-60 pointer-events-none" : "hover:border-[#214C55]"
              }`}
            >
              {/* Top row: type badge + title + proof link */}
              <div className="flex justify-between items-start gap-3">
                <div className="space-y-1.5 flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className={`inline-flex items-center px-2 py-0.5 rounded-none text-[9px] font-extrabold border uppercase tracking-wider ${TYPE_STYLES[item.type] || "bg-slate-50 text-slate-700 border-slate-200"}`}>
                      {item.type}
                    </span>
                    <span className={`inline-flex items-center px-2 py-0.5 rounded-none text-[9px] font-extrabold border uppercase tracking-wider ${STATUS_STYLES[item.status] || "bg-slate-50 text-slate-700 border-slate-200"}`}>
                      {item.status}
                    </span>
                  </div>
                  <h3 className="text-sm font-extrabold text-[#214C55] uppercase tracking-wide leading-tight">{item.title}</h3>
                </div>
                {item.proof_link && (
                  <a
                    href={item.proof_link}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="flex-shrink-0 px-2 py-1 bg-white hover:bg-[#F7F7F7] text-[#C76F2B] border border-[#D1D5DB] flex items-center gap-1 transition-all"
                    title="Open proof link"
                  >
                    <span className="text-[9px] font-bold uppercase tracking-wider">Proof</span>
                    <ExternalLink size={10} />
                  </a>
                )}
              </div>

              {/* Description */}
              <p className="text-xs text-[#111827] leading-relaxed font-semibold bg-[#F7F7F7] p-3 border border-[#D1D5DB]">
                {item.description}
              </p>

              {/* Existing feedback note (correction/rejection) */}
              {item.feedback && (
                <div className="text-[10px] font-semibold text-[#D97706] bg-amber-50 border border-amber-200 px-3 py-2">
                  <span className="font-extrabold uppercase tracking-wider">Note: </span>{item.feedback}
                </div>
              )}

              {/* Student metadata footer */}
              <div className="flex items-center justify-between border-t border-[#E5E5E5] pt-3 text-[10px] text-[#6B7280] font-extrabold uppercase tracking-wider">
                <span className="flex items-center gap-1.5">
                  <User size={12} className="text-[#6B7280]" />
                  <span className="text-[#214C55]">{item.student_name}</span>
                  <span className="text-[#6B7280] font-bold">({item.register_no})</span>
                </span>
                <span className="flex items-center gap-1 text-[#6B7280]">
                  <Calendar size={12} />
                  <span>{item.submitted_date}</span>
                </span>
              </div>

              {/* Action buttons — only show if still Pending or Correction Required */}
              {(item.status === "Pending" || item.status === "Correction Required") && (
                <>
                  {activeCorrectionId === `${item.item_type}-${item.id}` ? (
                    <div className="space-y-3 bg-[#FFFBEB] p-3 border border-amber-200 animate-fade-in">
                      <p className="text-[10px] font-extrabold text-[#D97706] uppercase tracking-wider">Correction Note</p>
                      <textarea
                        placeholder="Describe what correction is required from the student..."
                        value={feedbackText}
                        onChange={e => setFeedbackText(e.target.value)}
                        className="w-full text-xs p-2 bg-white border border-[#D1D5DB] focus:outline-none focus:border-[#C76F2B] font-semibold"
                        rows={2}
                      />
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => { setActiveCorrectionId(null); setFeedbackText(""); }}
                          className="px-2.5 py-1 text-[10px] font-extrabold uppercase tracking-wider text-[#6B7280] hover:text-[#111827] bg-white border border-[#D1D5DB]"
                        >
                          Cancel
                        </button>
                        <button
                          onClick={() => handleReview(item.id, item.item_type, "Correction Required", feedbackText)}
                          disabled={!feedbackText.trim()}
                          className="px-2.5 py-1 text-[10px] font-extrabold uppercase tracking-wider text-white bg-[#D97706] hover:bg-[#B45309] disabled:opacity-50"
                        >
                          Submit Request
                        </button>
                      </div>
                    </div>
                  ) : activeRejectId === `${item.item_type}-${item.id}` ? (
                    <div className="space-y-3 bg-red-50 p-3 border border-red-200 animate-fade-in">
                      <p className="text-[10px] font-extrabold text-[#B91C1C] uppercase tracking-wider">Rejection Reason (Optional)</p>
                      <textarea
                        placeholder="State the reason for rejection (optional)..."
                        value={rejectNote}
                        onChange={e => setRejectNote(e.target.value)}
                        className="w-full text-xs p-2 bg-white border border-[#D1D5DB] focus:outline-none focus:border-[#B91C1C] font-semibold"
                        rows={2}
                      />
                      <div className="flex items-center justify-end gap-2">
                        <button
                          onClick={() => { setActiveRejectId(null); setRejectNote(""); }}
                          className="px-2.5 py-1 text-[10px] font-extrabold uppercase tracking-wider text-[#6B7280] hover:text-[#111827] bg-white border border-[#D1D5DB]"
                        >
                          Cancel
                        </button>
                        <button
                          onClick={() => handleReview(item.id, item.item_type, "Rejected", rejectNote)}
                          className="px-2.5 py-1 text-[10px] font-extrabold uppercase tracking-wider text-white bg-[#B91C1C] hover:bg-red-800"
                        >
                          Confirm Reject
                        </button>
                      </div>
                    </div>
                  ) : (
                    <div className="grid grid-cols-3 gap-2 border-t border-[#E5E5E5] pt-3">
                      <button
                        onClick={() => handleReview(item.id, item.item_type, "Approved")}
                        className="py-1.5 px-2 text-[10px] font-extrabold uppercase tracking-wider text-[#15803D] hover:text-white bg-white hover:bg-[#15803D] border border-emerald-300 flex items-center justify-center gap-1 transition-all cursor-pointer"
                      >
                        <Check size={12} />
                        <span>Approve</span>
                      </button>
                      <button
                        onClick={() => { setActiveCorrectionId(`${item.item_type}-${item.id}`); setActiveRejectId(null); }}
                        className="py-1.5 px-2 text-[10px] font-extrabold uppercase tracking-wider text-[#D97706] hover:text-white bg-white hover:bg-[#D97706] border border-amber-300 flex items-center justify-center gap-1 transition-all cursor-pointer"
                      >
                        <RefreshCw size={10} />
                        <span>Correction</span>
                      </button>
                      <button
                        onClick={() => { setActiveRejectId(`${item.item_type}-${item.id}`); setActiveCorrectionId(null); }}
                        className="py-1.5 px-2 text-[10px] font-extrabold uppercase tracking-wider text-[#B91C1C] hover:text-white bg-white hover:bg-[#B91C1C] border border-red-300 flex items-center justify-center gap-1 transition-all cursor-pointer"
                      >
                        <X size={12} />
                        <span>Reject</span>
                      </button>
                    </div>
                  )}
                </>
              )}

              {/* Already resolved — show read-only indicator */}
              {item.status === "Approved" && (
                <div className="border-t border-[#E5E5E5] pt-3 flex items-center gap-2 text-[10px] font-extrabold text-[#15803D] uppercase tracking-wider">
                  <Check size={13} />
                  <span>Verified &amp; Approved</span>
                </div>
              )}
              {item.status === "Rejected" && (
                <div className="border-t border-[#E5E5E5] pt-3 flex items-center gap-2 text-[10px] font-extrabold text-[#B91C1C] uppercase tracking-wider">
                  <X size={13} />
                  <span>Submission Rejected</span>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};
export default MentorApprovalPage;
