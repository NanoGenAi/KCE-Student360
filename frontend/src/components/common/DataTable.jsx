import React, { useState, useMemo } from "react";
import { Search, ChevronDown, ChevronUp, SlidersHorizontal } from "lucide-react";
import EmptyState from "./EmptyState";

export const DataTable = ({
  columns,
  data = [],
  searchPlaceholder = "Search records...",
  searchKey, // key in the object to search (e.g. 'name' or 'register_no')
  filterConfig, // e.g. { key: 'department', label: 'Department', options: [...] }
  loading = false,
  emptyTitle = "No records found",
  emptyDescription = "No data matched the criteria or tables are currently empty."
}) => {
  const [searchTerm, setSearchTerm] = useState("");
  const [filterValue, setFilterValue] = useState("");
  const [sortConfig, setSortConfig] = useState(null);

  // Sorting handler
  const handleSort = (key, sortable) => {
    if (!sortable) return;
    let direction = "ascending";
    if (sortConfig && sortConfig.key === key && sortConfig.direction === "ascending") {
      direction = "descending";
    }
    setSortConfig({ key, direction });
  };

  // Filtered and sorted data calculation
  const processedData = useMemo(() => {
    let result = [...data];

    // 1. Apply Search Filter
    if (searchTerm.trim() !== "") {
      const searchLower = searchTerm.toLowerCase();
      result = result.filter((row) => {
        if (searchKey) {
          const value = row[searchKey];
          return value ? String(value).toLowerCase().includes(searchLower) : false;
        } else {
          return Object.values(row).some(
            (val) => val && String(val).toLowerCase().includes(searchLower)
          );
        }
      });
    }

    // 2. Apply Custom Dropdown Filter
    if (filterConfig && filterValue !== "") {
      result = result.filter((row) => {
        const val = row[filterConfig.key];
        return val ? String(val).toLowerCase() === filterValue.toLowerCase() : false;
      });
    }

    // 3. Apply Column Sorting
    if (sortConfig) {
      result.sort((a, b) => {
        let aVal = a[sortConfig.key];
        let bVal = b[sortConfig.key];

        if (!isNaN(Number(aVal)) && !isNaN(Number(bVal))) {
          aVal = Number(aVal);
          bVal = Number(bVal);
        } else {
          aVal = aVal ? String(aVal).toLowerCase() : "";
          bVal = bVal ? String(bVal).toLowerCase() : "";
        }

        if (aVal < bVal) {
          return sortConfig.direction === "ascending" ? -1 : 1;
        }
        if (aVal > bVal) {
          return sortConfig.direction === "ascending" ? 1 : -1;
        }
        return 0;
      });
    }

    return result;
  }, [data, searchTerm, searchKey, filterConfig, filterValue, sortConfig]);

  return (
    <div className="space-y-4 animate-fade-in text-[#111827]">
      {/* Controls Bar */}
      {(searchPlaceholder || filterConfig) && (
        <div className="flex flex-col sm:flex-row gap-3 items-center justify-between bg-white p-4 rounded-none border border-[#D1D5DB] shadow-none">
          {/* Search Box */}
          <div className="relative w-full sm:max-w-xs">
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-[#6B7280]" />
            <input
              type="text"
              placeholder={searchPlaceholder}
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-9 pr-4 py-2 w-full text-sm bg-white border border-[#D1D5DB] rounded-none focus:outline-none focus:border-[#C76F2B] font-semibold placeholder-[#6B7280]"
            />
          </div>

          {/* Filter Dropdown */}
          {filterConfig && (
            <div className="flex items-center space-x-2 w-full sm:w-auto">
              <SlidersHorizontal size={15} className="text-[#6B7280]" />
              <select
                value={filterValue}
                onChange={(e) => setFilterValue(e.target.value)}
                className="px-3 py-2 text-sm bg-white border border-[#D1D5DB] rounded-none focus:outline-none focus:border-[#C76F2B] font-semibold cursor-pointer w-full sm:w-auto text-[#111827]"
              >
                <option value="">All {filterConfig.label}s</option>
                {filterConfig.options.map((opt) => (
                  <option key={opt} value={opt}>
                    {opt}
                  </option>
                ))}
              </select>
            </div>
          )}
        </div>
      )}

      {/* Table Container */}
      <div className="bg-white rounded-none border border-[#D1D5DB] shadow-none overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse bg-white">
            <thead>
              <tr className="bg-[#E5E5E5] border-b border-[#D1D5DB] text-xs font-extrabold text-[#214C55] uppercase tracking-wider">
                {columns.map((col) => (
                  <th
                    key={col.key}
                    onClick={() => handleSort(col.key, col.sortable)}
                    className={`px-6 py-3 select-none ${col.sortable ? "cursor-pointer hover:bg-[#D1D5DB] hover:text-[#163941]" : ""} ${col.className || ""}`}
                  >
                    <div className="flex items-center space-x-1">
                      <span>{col.label}</span>
                      {col.sortable && sortConfig?.key === col.key && (
                        sortConfig.direction === "ascending" ? <ChevronUp size={14} /> : <ChevronDown size={14} />
                      )}
                    </div>
                  </th>
                ))}
              </tr>
            </thead>
            <tbody className="divide-y divide-[#E5E5E5] text-xs font-bold text-[#111827]">
              {loading ? (
                <tr>
                  <td colSpan={columns.length} className="px-6 py-12 text-center text-[#6B7280]">
                    <div className="flex flex-col items-center justify-center space-y-3">
                      <div className="w-6 h-6 border-2 border-slate-200 border-t-[#C76F2B] rounded-full animate-spin" />
                      <span>Loading table records...</span>
                    </div>
                  </td>
                </tr>
              ) : processedData.length === 0 ? (
                <tr>
                  <td colSpan={columns.length} className="px-6 py-12 text-center">
                    <EmptyState title={emptyTitle} description={emptyDescription} />
                  </td>
                </tr>
              ) : (
                processedData.map((row, rowIndex) => (
                  <tr
                    key={row.id || row.register_no || rowIndex}
                    className="hover:bg-[#F7F7F7] transition-colors"
                  >
                    {columns.map((col) => (
                      <td key={col.key} className={`px-6 py-3.5 whitespace-nowrap ${col.className || ""}`}>
                        {col.render ? col.render(row, rowIndex) : row[col.key] || "-"}
                      </td>
                    ))}
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
export default DataTable;
