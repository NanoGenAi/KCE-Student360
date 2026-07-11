export const safeNumber = (value, fallback = 0) => {
  const num = Number(value);
  return Number.isFinite(num) ? num : fallback;
};

export const safeFixed = (value, digits = 1, fallback = "0.0") => {
  const num = Number(value);
  return Number.isFinite(num) ? num.toFixed(digits) : fallback;
};

export const safePercent = (value, digits = 1, fallback = "N/A") => {
  const num = Number(value);
  return Number.isFinite(num) ? `${num.toFixed(digits)}%` : fallback;
};
