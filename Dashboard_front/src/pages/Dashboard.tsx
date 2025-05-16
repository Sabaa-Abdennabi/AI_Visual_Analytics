function Dashbaord() {
  const scoreGroups = [
    [
      { label: "Total", value: 8.8 },
      { label: "Navigation", value: 8.9 },
      { label: "Accessibilité", value: 8.8 },
      { label: "Engagement", value: 5.4 },
    ],
  ];
  const stats = [
    {
      value: "8.7",
      label: "Average Time Predicted",
      color: "text-blue-600",
    },
    {
      value: "92%",
      label: "Buttons clicked",
      color: "text-green-600",
    },
    {
      value: "4.5s",
      label: "Scroll Depth",
      color: "text-orange-500",
    },
  ];
  const recommendations = [
    "Improve navigation clarity and reduce visual clutter to enhance user engagement.",
    "Consider increasing contrast for better accessibility.",
    "Optimize button placement for higher conversion.",
  ];
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
                    clip-rule="evenodd"
                    fill-rule="evenodd"
                    d="M2 4.75A.75.75 0 012.75 4h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 4.75zm0 10.5a.75.75 0 01.75-.75h7.5a.75.75 0 010 1.5h-7.5a.75.75 0 01-.75-.75zM2 10a.75.75 0 01.75-.75h14.5a.75.75 0 010 1.5H2.75A.75.75 0 012 10z"
                  ></path>
                </svg>
              </button>
              <div className="flex items-center space-x-3">
                {/* Logo avec carreaux imbriqués */}
                <div className="relative w-6 h-6">
                  <div className="absolute inset-0 bg-orange-500 rounded-sm shadow-md"></div>
                  <div className="absolute inset-1 bg-amber-300 rounded-sm"></div>
                </div>
                <span className="font-bold text-lg">AI Visual Analytic</span>
              </div>
            </div>
            <div className="flex items-center">
              <div className="flex items-center ms-3">
                <div>
                  <button
                    type="button"
                    className="text-sm md:text-base text-gray-700 hover:text-orange-500 transition-colors duration-200"
                    aria-expanded="false"
                    data-dropdown-toggle="dropdown-user"
                  >
                    <span className="sr-only">Open user menu</span>
                    <img
                      className="w-16 h-16 rounded-full"
                      src="../src/assets/profile.jpg"
                    />
                  </button>
                </div>
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
              <a
                href="#"
                className="flex items-center p-2 text-l md:text-base text-gray-700 hover:text-orange-500 transition-colors duration-200 group"
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
              </a>
            </li>
            <li>
              <a
                href="#"
                className="flex items-center p-2 text-l md:text-base text-gray-700 hover:text-orange-500 transition-colors duration-200 group"
              >
                <svg
                  className="shrink-0 w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="currentColor"
                  viewBox="0 0 18 18"
                >
                  <path d="M6.143 0H1.857A1.857 1.857 0 0 0 0 1.857v4.286C0 7.169.831 8 1.857 8h4.286A1.857 1.857 0 0 0 8 6.143V1.857A1.857 1.857 0 0 0 6.143 0Zm10 0h-4.286A1.857 1.857 0 0 0 10 1.857v4.286C10 7.169 10.831 8 11.857 8h4.286A1.857 1.857 0 0 0 18 6.143V1.857A1.857 1.857 0 0 0 16.143 0Zm-10 10H1.857A1.857 1.857 0 0 0 0 11.857v4.286C0 17.169.831 18 1.857 18h4.286A1.857 1.857 0 0 0 8 16.143v-4.286A1.857 1.857 0 0 0 6.143 10Zm10 0h-4.286A1.857 1.857 0 0 0 10 11.857v4.286c0 1.026.831 1.857 1.857 1.857h4.286A1.857 1.857 0 0 0 18 16.143v-4.286A1.857 1.857 0 0 0 16.143 10Z" />
                </svg>
                <span className="flex-1 ms-3 whitespace-nowrap">Settings</span>
              </a>
            </li>

            <li>
              <a
                href="#"
                className="flex items-center p-2 text-l md:text-base text-gray-700 hover:text-orange-500 transition-colors duration-200 group"
              >
                <svg
                  className="shrink-0 w-5 h-5 text-gray-500 transition duration-75 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white"
                  aria-hidden="true"
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 18 16"
                >
                  <path
                    stroke="currentColor"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    stroke-width="2"
                    d="M1 8h11m0 0L8 4m4 4-4 4m4-11h3a2 2 0 0 1 2 2v10a2 2 0 0 1-2 2h-3"
                  />
                </svg>
                <span className="flex-1 ms-3 whitespace-nowrap">Log Out</span>
              </a>
            </li>
            <li></li>
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
                src="../src/assets/heatmap.png"
                alt="Heatmap Prediction"
                className="object-contain h-full w-full rounded"
              />
            </div>
            <div className="col-span-1 p-4 flex flex-col items-center justify-center h-96 rounded-sm bg-gray-50 dark:bg-gray-800">
              <div className="flex items-center mb-5">
                <p className="ms-2 font-medium text-gray-900 dark:text-white">
                  Excellent
                </p>
              </div>
              <div className="gap-8 sm:grid  w-full">
                {scoreGroups.map((group, i) => (
                  <div key={i}>
                    {group.map((score) => (
                      <dl key={score.label}>
                        <dt className="text-sm font-medium text-gray-500 dark:text-gray-400">
                          {score.label}
                        </dt>
                        <dd className="flex items-center mb-3">
                          <div className="w-full bg-gray-200 rounded-sm h-2.5 dark:bg-gray-700 me-2">
                            <div
                              className="bg-blue-600 h-2.5 rounded-sm dark:bg-blue-500"
                              style={{ width: `${score.value * 10}%` }}
                            ></div>
                          </div>
                          <span className="text-sm font-medium text-gray-500 dark:text-gray-400">
                            {score.value}
                          </span>
                        </dd>
                      </dl>
                    ))}
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Stats Overview */}
          <div className="grid grid-cols-3 gap-4 mb-6">
            {stats.map((stat, idx) => (
              <div
                key={stat.label}
                className="flex flex-col items-center justify-center rounded bg-white dark:bg-gray-800 shadow p-4"
              >
                <span className={`text-3xl font-bold ${stat.color}`}>
                  {stat.value}
                </span>
                <span className="text-gray-500 dark:text-gray-400">
                  {stat.label}
                </span>
              </div>
            ))}
          </div>
          {/* Recommendation Part */}
          <div className="mb-6 p-4 rounded bg-blue-50 dark:bg-gray-900 border-l-4 border-blue-400">
            <h3 className="font-semibold text-blue-700 dark:text-blue-300 mb-2">
              Recommendations
            </h3>
            <ul className="list-disc pl-5 space-y-1">
              {recommendations.map((rec, idx) => (
                <li key={idx} className="text-gray-700 dark:text-gray-200">
                  {rec}
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashbaord;
