import { Link } from 'react-router-dom';
import { Database, Activity } from 'lucide-react';

function Navbar() {
  return (
    <nav className="bg-white shadow-md border-b border-gray-200 sticky top-0 z-50">
      <div className="px-6 py-4">
        <div className="flex items-center justify-between">
          <Link to="/" className="flex items-center space-x-3">
            <Database className="w-8 h-8 text-primary-600" />
            <div>
              <h1 className="text-xl font-bold text-gray-900">Advanced LRU Cache</h1>
              <p className="text-xs text-gray-500">High-Performance Caching System</p>
            </div>
          </Link>
          
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-2 px-3 py-1.5 bg-green-50 text-green-700 rounded-full">
              <Activity className="w-4 h-4" />
              <span className="text-sm font-medium">Online</span>
            </div>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
