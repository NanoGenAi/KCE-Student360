import React from "react";

export const DomainBadge = ({ domain }) => {
  if (!domain) return null;

  const normalizedDomain = domain.trim().toUpperCase();

  // Alternate between teal and orange shades
  const domainStyles = {
    DSA: "bg-orange-50 text-[#C76F2B] border-orange-200",
    DBMS: "bg-teal-50 text-[#214C55] border-teal-200",
    FULLSTACK: "bg-teal-50 text-[#214C55] border-teal-200",
    APTITUDE: "bg-teal-50 text-[#214C55] border-teal-200",
    CODING: "bg-orange-50 text-[#C76F2B] border-orange-200",
    ACADEMIC: "bg-teal-50 text-[#214C55] border-teal-200",
    TECHNICAL: "bg-teal-50 text-[#214C55] border-teal-200"
  };

  const style = domainStyles[normalizedDomain] || "bg-slate-50 text-slate-700 border-slate-200";

  return (
    <span className={`inline-flex items-center px-2 py-0.5 text-[10px] font-extrabold uppercase tracking-wider rounded-none border ${style}`}>
      {domain}
    </span>
  );
};
export default DomainBadge;
