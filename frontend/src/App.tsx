import React, { useState } from 'react';
import { Building2, UserCircle, Users } from 'lucide-react';
import ExecutiveDashboard from './views/ExecutiveDashboard';
import OperatorDashboard from './views/OperatorDashboard';

function App() {
  const [activeView, setActiveView] = useState<'executive' | 'operator'>('executive');

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Navigation */}
      <nav className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <Building2 className="w-8 h-8 text-blue-600 mr-3" />
              <h1 className="text-xl font-bold text-gray-900">Industrial AI Platform</h1>
            </div>
            <div className="flex space-x-4">
              <button
                onClick={() => setActiveView('executive')}
                className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
                  activeView === 'executive'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                <Users className="w-4 h-4 mr-2" />
                Executive View
              </button>
              <button
                onClick={() => setActiveView('operator')}
                className={`flex items-center px-4 py-2 rounded-lg transition-colors ${
                  activeView === 'operator'
                    ? 'bg-blue-600 text-white'
                    : 'text-gray-700 hover:bg-gray-100'
                }`}
              >
                <UserCircle className="w-4 h-4 mr-2" />
                Operator View
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Content */}
      {activeView === 'executive' ? <ExecutiveDashboard /> : <OperatorDashboard />}
    </div>
  );
}

export default App;
