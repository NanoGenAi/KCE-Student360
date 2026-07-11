import React from "react";
import { AlertCircle } from "lucide-react";

export const EmptyState = ({
  title = "No Data Available",
  description = "There are no records matching your criteria. Try adjusting your filters.",
  icon: Icon = AlertCircle,
  actionText,
  onAction
}) => {
  return (
    <div className="flex flex-col items-center justify-center text-center p-8 border-2 border-dashed border-slate-200 rounded-xl bg-white space-y-4 max-w-md mx-auto my-6 animate-fade-in">
      <div className="p-3 bg-slate-50 text-slate-400 rounded-full">
        <Icon size={36} />
      </div>
      <div>
        <h3 className="text-lg font-semibold text-slate-800">{title}</h3>
        <p className="text-sm text-slate-500 mt-1 px-4">{description}</p>
      </div>
      {actionText && onAction && (
        <button
          onClick={onAction}
          className="px-4 py-2 text-sm font-semibold text-white bg-brand-indigo-600 hover:bg-brand-indigo-700 transition-colors rounded-lg shadow-sm"
        >
          {actionText}
        </button>
      )}
    </div>
  );
};
export default EmptyState;
