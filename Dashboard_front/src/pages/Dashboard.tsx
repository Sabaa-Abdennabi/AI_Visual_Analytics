import { useNavigate } from "react-router-dom";
import { useReport } from "../context/ReportContext";

function Dashboard() {
  const { report } = useReport();
  const navigate = useNavigate(); // Add this line

  function parseRecommendations(text: string) {
    // Split into lines and trim
    const lines = text
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean);
    const sections: any[] = [];
    let currentSection: any = { heading: "", type: "p", items: [] };

    lines.forEach((line) => {
      // Heading: line ends with ":" or is all uppercase/capitalized
      if (
        /^[A-Z][A-Za-z0-9\s]+:$/.test(line) ||
        /^[A-Z][A-Za-z0-9\s]+$/.test(line)
      ) {
        if (currentSection.items.length) sections.push(currentSection);
        currentSection = {
          heading: line.replace(/:$/, ""),
          type: "p",
          items: [],
        };
      } else if (/^\*\*(.+)\*\*$/.test(line)) {
        // Bold line, treat as subheading or important item
        if (currentSection.items.length) sections.push(currentSection);
        currentSection = {
          heading: line.replace(/^\*\*|\*\*$/g, ""),
          type: "p",
          items: [],
        };
      } else {
        currentSection.items.push(line);
      }
    });
    if (currentSection.items.length) sections.push(currentSection);
    return sections;
  }

  // Fallback if no report is loaded
  if (!report) {
    return (
      <div className="p-8">No report data. Please generate a report first.</div>
    );
  }

  // Prepare stats from backend response
  const stats = [
    {
      value: report.total_elements ?? "-",
      label: "Total Elements",
      color: "text-blue-600",
    },
    {
      value:
        report.percent_viewed !== undefined
          ? `${report.percent_viewed.toFixed(2)}%`
          : "-",
      label: "Elements Viewed",
      color: "text-green-600",
    },
    {
      value:
        report.percent_clicked !== undefined
          ? `${report.percent_clicked.toFixed(2)}%`
          : "-",
      label: "Elements Clicked",
      color: "text-orange-500",
    },
  ];

  // Split recommendations into lines or paragraphs
  const parsedRecommendations = report.recommendations
    ? parseRecommendations(report.recommendations)
    : [];

  // If you want to show the heatmap dynamically, you can use a path from the backend if available
  // For now, we use the static path as in your backend
  const heatmapPath = "/assets/heatmap.png";

  return (
    <div>
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

      <div className="p-4 sm:ml-64">
        <div className="p-4 border-2 border-gray-200 border-dashed rounded-lg dark:border-gray-700 mt-14">
          <div className="grid grid-cols-3 gap-4 m-4">
            {/* Heatmap Prediction Image (2/3 width) */}
            <div className="col-span-2 flex p-4  flex-col items-start justify-center h-96 rounded-sm bg-gray-50 dark:bg-gray-800">
              <p className="m-2 text-left font-medium text-gray-900 dark:text-white">
                Predicted Heatmap
              </p>
              <img
                src={heatmapPath}
                alt="Heatmap Prediction"
                className="object-contain h-full w-full rounded"
              />
            </div>
            <div className="col-span-1 p-4 flex flex-col items-center justify-center h-96 rounded-sm bg-gray-50 dark:bg-gray-800">
              <div className="flex items-center mb-5">
                <p className="ms-2 font-medium text-gray-900 dark:text-white">
                  Metrics
                </p>
              </div>
              <div className="gap-8 sm:grid  w-full">
                {stats.map((stat, idx) => (
                  <div key={stat.label}>
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 dark:text-gray-400">
                        {stat.label}
                      </dt>
                      <dd className="flex items-center mb-3">
                        <span className={`text-2xl font-bold ${stat.color}`}>
                          {stat.value}
                        </span>
                      </dd>
                    </dl>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Recommendation Part */}
          <div className="mb-6 p-4 rounded bg-blue-50 dark:bg-gray-900 border-l-4 border-blue-400">
            <h3 className="font-semibold py-6 text-blue-700 dark:text-blue-300 mb-2">
              Recommendations
            </h3>
            <div className="space-y-4">
              {/* Render recommendations as a styled ordered list */}
              <ol className="list-decimal pl-6 space-y-3">
                {parsedRecommendations
                  .flatMap((section) => section.items)
                  .filter((item) => /^\d+\./.test(item))
                  .map((item, idx) => (
                    <li
                      key={idx}
                      className=" dark:bg-gray-800 rounded px-4 py-2 shadow-sm border border-blue-100 dark:border-gray-700"
                    >
                      <span
                        dangerouslySetInnerHTML={{
                          __html: item
                            .replace(/^\d+\.\s*/, "")
                            .replace(/\*\*(.+?)\*\*/g, "<b>$1</b>"),
                        }}
                      />
                    </li>
                  ))}
              </ol>

              {/* Show conclusion if present */}
              {parsedRecommendations.length > 1 && (
                <div className="mt-6 text-gray-700 dark:text-gray-300 italic">
                  {parsedRecommendations
                    .flatMap((section) => section.items)
                    .filter(
                      (item) =>
                        !/^\d+\./.test(item) &&
                        item !== parsedRecommendations[0].items[0]
                    )
                    .map((item, idx) => (
                      <p>{item}</p>
                    ))}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
