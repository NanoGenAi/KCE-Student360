import React from "react";

export const StatCard = ({ title, value, icon: Icon, description, trend, trendType = "positive", onIconClick }) => {
  const trendColors = {
    positive: "text-[#15803D] bg-emerald-50 border border-emerald-100",
    negative: "text-[#B91C1C] bg-rose-50 border border-rose-100",
    neutral: "text-[#6B7280] bg-[#E5E5E5] border border-[#D1D5DB]"
  };

  return (
    <div className="bg-white p-5 rounded-none border border-[#D1D5DB] border-t-4 border-t-[#C76F2B] shadow-none flex items-start justify-between transition-all hover:border-[#C76F2B] animate-fade-in">
      <div className="space-y-1.5">
        <span className="text-[10px] font-extrabold text-[#214C55] tracking-wider uppercase block">{title}</span>
        <div className="flex items-baseline space-x-2">
          <span className="text-2xl font-black text-[#C76F2B] tracking-tight">{value}</span>
          {trend && (
            <span className={`text-[9px] px-1.5 py-0.5 rounded-none font-bold uppercase tracking-wider border ${trendColors[trendType]}`}>
              {trend}
            </span>
          )}
        </div>
        {description && (
          <p className="text-[11px] text-[#6B7280] font-semibold">{description}</p>
        )}
      </div>
      {Icon && (
        <div 
          onClick={onIconClick}
          className={`p-2.5 bg-[#F7F7F7] text-[#214C55] border border-[#D1D5DB] rounded-none flex-shrink-0 ${
            onIconClick ? "cursor-pointer hover:bg-[#E5E5E5] hover:text-[#C76F2B] transition-colors" : ""
          }`}
          title={onIconClick ? "Upload Scores" : undefined}
        >
          <Icon size={18} />
        </div>
      )}
    </div>
  );
};
export default StatCard;
