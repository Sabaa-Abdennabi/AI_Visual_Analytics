import { useReport } from "../context/ReportContext";
import { useNavigate } from "react-router-dom";

function History() {
  const { setReport, getReportHistory } = useReport();
  const navigate = useNavigate();

  const history = getReportHistory();

  return (
    <div >
      <nav className="fixed top-0 z-50 w-full bg-white border-b border-gray-200 dark:bg-gray-800 dark:border-gray-700">
        <div className="px-3 py-3 lg:px-5 lg:pl-3">
          <div className="flex items-center justify-between">
            <div className="flex items-center justify-start rtl:justify-end">
              <button
                data-drawer-target="logo-sidebar"
                data-drawer-toggle="logo-sidebar"
                aria-controls="logo-sidebar"
                type="button"
                className="inline-flex items-center p-2 text-sm text-gray-500 rounded-lg sm:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600"
              >
                <span className="sr-only">Open sidebar</span>
                <svg
                  className="w-6 h-6"
                  aria-hidden="true"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                  xmlns="http://www.w3.org/2000/svg"
                >
                  <path
                    clipRule="evenodd"
                    fillRule="evenodd"
                    d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zm0 10.5a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5a.75.75 0 01-.75-.75zM2 10a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 10z"
                  ></path>
                </svg>
              </button>
              <div className="flex items-center space-x-3">
                <div className="relative w-6 h-6">
                  <div className="absolute inset-0 bg-orange-500 rounded-sm shadow-md"></div>
                  <div className="absolute inset-1 bg-amber-300 rounded-sm"></div>
                </div>
                <span className="font-bold text-lg">AI Visual Analytic</span>
              </div>
            </div>

          </div>
        </div>
      </nav>

      <aside
        id="logo-sidebar"
        className="fixed  top-0 left-0 z-40 w-64 h-screen pt-20 transition-transform -translate-x-full bg-white border-r border-gray-200 sm:translate-x-0 dark:bg-gray-800 dark:border-gray-700"
        aria-label="Sidebar"
      >
        <div className="h-full my-5  px-3 pb-4 overflow-y-auto bg-white dark:bg-gray-800 ">
          <ul className="space-y-2 font-medium">
            <li>
              <a
                href="#"
                className="flex items-center p-2 text-l md:text-base text-gray-700 hover:text-orange-500 transition-colors duration-200 group"
              >
                <svg
                  className="w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="currentColor"
                  viewBox="0 0 22 21"
                >
                  <path d="M16.975 11H10V4.025a1 1 0 0 0-1.066-.998 8.5 8.5 0 1 0 9.039 9.039.999.999 0 0 0-1-1.066h.002Z" />
                  <path d="M12.5 0c-.157 0-.311.01-.565.027A1 1 0 0 0 11 1.02V10h8.975a1 1 0 0 0 1-.935c.013-.188.028-.374.028-.565A8.51 8.51 0 0 0 12.5 0Z" />
                </svg>
                <span className="ms-3">Dashboard</span>
              </a>
            </li>
            <li>
              <button
                onClick={() => navigate("/history")}
                className="flex items-center p-2 text-l md:text-base text-gray-700 hover:text-orange-500 transition-colors duration-200 group w-full text-left"
              >
                <svg
                  className="shrink-0 w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="currentColor"
                  viewBox="0 0 20 20"
                >
                  <path d="M10 2a8 8 0 1 0 8 8h-1.5a6.5 6.5 0 1 1-2.1-4.6l-1.4 1.4V4h4.5l-1.4 1.4A8 8 0 0 0 10 2zm1 5v4l3 1" />
                </svg>
                <span className="flex-1 ms-3 whitespace-nowrap">History</span>
              </button>
            </li>
          </ul>
        </div>
      </aside>
      <h1 className="text-3xl font-bold mb-6 text-gray-800 dark:text-gray-100">
        Report History
      </h1>
      {history.length === 0 ? (
        <div className="text-gray-500">No history yet.</div>
      ) : (
        <ul className="space-y-4 max-w-2xl mx-auto">
          {history.map((item, idx) => (
            <li
              key={idx}
              className="p-4 bg-white dark:bg-gray-800 rounded shadow flex justify-between items-center"
            >
              <div>
                <div className="font-semibold text-gray-700 dark:text-gray-200">
                  {item.url || "Report"}
                </div>
                <div className="text-xs text-gray-500">
                  {item.created_at || ""}
                </div>
              </div>
              <button
                className="text-orange-500 hover:underline text-sm"
                onClick={() => {
                  setReport(item);
                  navigate("/dashboard");
                }}
              >
                View
              </button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default History;
