const Navbar = () => {
  return (
    <nav className="bg-white p-4 shadow-sm">
      <div className="container mx-auto flex justify-between items-center">
        <div className="flex items-center space-x-3">
          {/* Logo avec carreaux imbriqués */}
          <div className="relative w-6 h-6">
            <div className="absolute inset-0 bg-orange-500 rounded-sm shadow-md"></div>
            <div className="absolute inset-1 bg-amber-300 rounded-sm"></div>
          </div>
          <span className="font-bold text-lg">AI Visual Analytic</span>
        </div>

        {/* Navigation - Toujours visible */}
        <div className="flex space-x-4 md:space-x-8 items-center">
          {/* Lien Home avec ligne orange */}
          <div className="relative">
            <a
              href="#"
              className="text-sm md:text-base text-gray-700 hover:text-orange-500 transition-colors duration-200"
            >
              Home
            </a>
            <div className="absolute bottom-[-4px] left-0 w-full h-0.5 bg-orange-500 rounded-full"></div>
          </div>
        
        </div>
      </div>
    </nav>
  );
};

export default Navbar;