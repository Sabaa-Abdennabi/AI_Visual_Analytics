import React, { createContext, useContext, useState } from "react";

type ReportData = {
  total_elements?: number;
  percent_clicked?: number;
  percent_viewed?: number;
  avg_area?: number;
  mean_duration?: number;
  recommendations?: string;
  heatmap_path?: string;
};

const ReportContext = createContext<{
  report: ReportData | null;
  setReport: (data: ReportData) => void;
  saveReportToHistory: (report: ReportData) => void;
  getReportHistory: () => any[];
}>({
  report: null,
  setReport: () => {},
  saveReportToHistory: () => {},
  getReportHistory: () => [],
});

export const useReport = () => useContext(ReportContext);

export const ReportProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [report, setReport] = useState<ReportData | null>(null);
  function saveReportToHistory(report: any) {
    if (!report) return;
    const history = getReportHistory();
    // Avoid duplicates (by URL or another unique field)
    if (
      history.length === 0 ||
      JSON.stringify(history[0]) !== JSON.stringify(report)
    ) {
      history.unshift(report);
      localStorage.setItem(
        "reportHistory",
        JSON.stringify(history.slice(0, 10))
      ); // Keep last 10
    }
  }
  function getReportHistory(): any[] {
  const raw = localStorage.getItem("reportHistory");
  return raw ? JSON.parse(raw) : [];
}
  return (
    <ReportContext.Provider value={{ report, setReport , saveReportToHistory, getReportHistory }}>
      {children}
    </ReportContext.Provider>
  );
};
