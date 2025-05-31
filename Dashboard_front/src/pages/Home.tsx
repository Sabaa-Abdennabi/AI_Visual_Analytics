import { useState } from "react";
import { useNavigate } from "react-router-dom";
import Navbar from "../components/navbar";
import { FiSearch } from "react-icons/fi";
import { useReport } from "../context/ReportContext";

function Home() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false); // <-- loading state
  const navigate = useNavigate();
  const { setReport, saveReportToHistory } = useReport();

  const handleGenerateReport = async () => {
    if (!url) {
      alert("Please enter a URL.");
      return;
    }
    setLoading(true); // Start loading
    try {
      const response = await fetch("http://127.0.0.1:5000/submit", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
      });
      const data = await response.json();
      if (response.ok) {
        setReport(data);
        saveReportToHistory(data);
        console.log("Report generated and saved to history");
        navigate("/dashboard");
      } else {
        alert(data.error || "Failed to generate report.");
      }
    } catch (error) {
      alert("Error connecting to backend.");
    } finally {
      setLoading(false); // Stop loading
    }
  };

  return (
    <div className="min-h-screen bg-jaune font-robboto flex flex-col">
      <Navbar />
      <div className="container mx-auto flex-grow flex items-center px-21">
        <div className="flex flex-col lg:flex-row gap-12 items-center w-full py-8">
          <div className="w-full lg:w-1/2">
            <h1 className="text-4xl sm:text-5xl md:text-6xl font-bold text-gray-700 mb-4">
              Optimize Your UX in 2 Minutes
            </h1>
            <p className="text-xl md:text-2xl lg:text-3xl text-gray-600 mb-8 italic">
              No code or user testing required
            </p>

            <div className="mb-4 relative">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Enter the url and generate the report"
                  className="w-full pl-12 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-orange-500 focus:border-orange-500 outline-none transition font-robboto"
                  value={url}
                  onChange={(e) => setUrl(e.target.value)}
                  disabled={loading}
                />
                <FiSearch className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 text-xl" />
              </div>
            </div>

            <div className="flex justify-end">
              <button
                className="bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 px-6 rounded-lg shadow-md transition-colors duration-200 inline-flex items-center"
                onClick={handleGenerateReport}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <svg
                      className="animate-spin h-5 w-5 mr-2 text-white"
                      viewBox="0 0 24 24"
                    >
                      <circle
                        className="opacity-25"
                        cx="12"
                        cy="12"
                        r="10"
                        stroke="currentColor"
                        strokeWidth="4"
                        fill="none"
                      />
                      <path
                        className="opacity-75"
                        fill="currentColor"
                        d="M4 12a8 8 0 018-8v4a4 4 0 00-4 4H4z"
                      />
                    </svg>
                    Generating...
                  </>
                ) : (
                  "Generate Report"
                )}
              </button>
            </div>
          </div>

          <div className="w-full lg:w-1/2 hidden md:block">
            <img
              src="../src/assets/image-2.png"
              alt="UX Analytics"
              className="w-full h-auto object-cover rounded-lg"
            />
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;
