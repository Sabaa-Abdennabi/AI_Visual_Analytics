import Navbar from './navbar';
import { FiSearch } from 'react-icons/fi';

function App() {
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
                />
                <FiSearch className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 text-xl" />
              </div>
            </div>
            
            <div className="flex justify-end">
              <button className="bg-orange-500 hover:bg-orange-600 text-white font-bold py-3 px-6 rounded-lg shadow-md transition-colors duration-200 inline-flex items-center">
                Generate Report
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

export default App;