import React from "react";

export const LoadingSpinner = ({ size = "md", text = "Loading data..." }) => {
  const sizeClasses = {
    sm: "w-5 h-5 border-2",
    md: "w-8 h-8 border-3",
    lg: "w-12 h-12 border-4"
  };

  return (
    <div className="flex flex-col items-center justify-center p-8 space-y-3 min-h-[200px]">
      <div
        className={`${sizeClasses[size]} border-brand-indigo-100 border-t-brand-indigo-600 rounded-full animate-spin`}
      />
      {text && <p className="text-sm font-medium text-slate-500">{text}</p>}
    </div>
  );
};
export default LoadingSpinner;
