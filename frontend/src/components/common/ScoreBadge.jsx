import React from "react";
import { safePercent } from "../../utils/formatters";

export const ScoreBadge = ({ score }) => {
  if (score === undefined || score === null) return <span className="text-[#6B7280] font-medium">-</span>;

  const numericScore = Number(score);
  
  let colorClass = "bg-red-50 text-[#B91C1C] border-[#FCA5A5]";
  if (numericScore >= 90) {
    colorClass = "bg-emerald-50 text-[#15803D] border-emerald-250";
  } else if (numericScore >= 80) {
    colorClass = "bg-teal-50 text-[#214C55] border-teal-200";
  } else if (numericScore >= 70) {
    colorClass = "bg-orange-50 text-[#C76F2B] border-orange-200";
  }

  return (
    <span className={`inline-flex items-center px-2 py-0.5 text-xs font-extrabold rounded-none border ${colorClass}`}>
      {safePercent(numericScore, 1)}
    </span>
  );
};
export default ScoreBadge;
