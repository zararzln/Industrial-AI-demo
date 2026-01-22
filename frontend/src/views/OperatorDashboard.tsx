import React, { useEffect, useState } from 'react';
import { AlertTriangle, Wrench, MessageSquare, Send } from 'lucide-react';
import { equipmentAPI, dashboardAPI, aiAPI, Equipment, Alert, QueryResponse } from '../services/api';

const OperatorDashboard: React.FC = () => {
  const [equipment, setEquipment] = useState<Equipment[]>([]);
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [selectedEquipment, setSelectedEquipment] = useState<Equipment | null>(null);
  const [query, setQuery] = useState('');
  const [aiResponse, setAiResponse] = useState<QueryResponse | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [equipmentRes, alertsRes] = await Promise.all([
        equipmentAPI.getAll(),
        dashboardAPI.getAllAlerts(false),
      ]);
      setEquipment(equipmentRes.data);
      setAlerts(alertsRes.data);
    } catch (error) {
      console.error('Error loading data:', error);
    }
  };

  const handleAskAI = async () => {
    if (!query.trim()) return;

    setLoading(true);
    try {
      const response = await aiAPI.query(query, selectedEquipment?.id);
      setAiResponse(response.data);
    } catch (error) {
      console.error('Error querying AI:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'operational':
        return 'bg-green-100 text-green-800';
      case 'warning':
        return 'bg-yellow-100 text-yellow-800';
      case 'critical':
        return 'bg-red-100 text-red-800';
      case 'maintenance':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical':
        return 'bg-red-500';
      case 'high':
        return 'bg-orange-500';
      case 'medium':
        return 'bg-yellow-500';
      case 'low':
        return 'bg-blue-500';
      default:
        return 'bg-gray-500';
    }
  };

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Operator Dashboard</h1>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Equipment List */}
          <div className="lg:col-span-2">
            <div className="bg-white rounded-lg shadow">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-xl font-semibold flex items-center">
                  <Wrench className="w-5 h-5 mr-2" />
                  Equipment Status
                </h2>
              </div>
              <div className="p-6">
                <div className="space-y-4">
                  {equipment.map((eq) => (
                    <div
                      key={eq.id}
                      className={`border rounded-lg p-4 cursor-pointer transition-all ${
                        selectedEquipment?.id === eq.id
                          ? 'border-blue-500 bg-blue-50'
                          : 'border-gray-200 hover:border-gray-300'
                      }`}
                      onClick={() => setSelectedEquipment(eq)}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <div className="flex items-center">
                            <h3 className="font-semibold text-gray-900">{eq.name}</h3>
                            <span
                              className={`ml-3 px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(
                                eq.status
                              )}`}
                            >
                              {eq.status.toUpperCase()}
                            </span>
                          </div>
                          <p className="text-sm text-gray-600 mt-1">
                            {eq.type} • {eq.location}
                          </p>
                          <div className="mt-3 grid grid-cols-3 gap-4 text-sm">
                            <div>
                              <span className="text-gray-500">Temp:</span>{' '}
                              <span className="font-medium">{eq.metrics.temperature.toFixed(1)}°F</span>
                            </div>
                            <div>
                              <span className="text-gray-500">Pressure:</span>{' '}
                              <span className="font-medium">{eq.metrics.pressure.toFixed(1)} PSI</span>
                            </div>
                            <div>
                              <span className="text-gray-500">Vibration:</span>{' '}
                              <span className="font-medium">{eq.metrics.vibration.toFixed(1)} mm/s</span>
                            </div>
                          </div>
                        </div>
                        <div className="text-right ml-4">
                          <div className="text-2xl font-bold text-gray-900">{eq.health_score}%</div>
                          <div className="text-xs text-gray-500">Health</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          </div>

          {/* Alerts Sidebar */}
          <div>
            <div className="bg-white rounded-lg shadow">
              <div className="p-6 border-b border-gray-200">
                <h2 className="text-xl font-semibold flex items-center">
                  <AlertTriangle className="w-5 h-5 mr-2" />
                  Active Alerts
                </h2>
              </div>
              <div className="p-6">
                <div className="space-y-3">
                  {alerts.length === 0 ? (
                    <p className="text-gray-500 text-sm">No active alerts</p>
                  ) : (
                    alerts.slice(0, 5).map((alert) => (
                      <div key={alert.id} className="border border-gray-200 rounded-lg p-3">
                        <div className="flex items-start">
                          <div className={`w-2 h-2 rounded-full ${getSeverityColor(alert.severity)} mt-2 mr-2`}></div>
                          <div className="flex-1">
                            <div className="font-medium text-sm text-gray-900">{alert.type}</div>
                            <div className="text-xs text-gray-600 mt-1">{alert.message}</div>
                            <div className="text-xs text-gray-500 mt-2">
                              {new Date(alert.timestamp).toLocaleString()}
                            </div>
                          </div>
                        </div>
                      </div>
                    ))
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* AI Assistant */}
        <div className="mt-6 bg-white rounded-lg shadow">
          <div className="p-6 border-b border-gray-200">
            <h2 className="text-xl font-semibold flex items-center">
              <MessageSquare className="w-5 h-5 mr-2" />
              AI Assistant
            </h2>
            {selectedEquipment && (
              <p className="text-sm text-gray-600 mt-1">
                Context: {selectedEquipment.name} ({selectedEquipment.id})
              </p>
            )}
          </div>
          <div className="p-6">
            <div className="flex gap-3 mb-4">
              <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleAskAI()}
                placeholder="Ask about equipment issues, procedures, or maintenance..."
                className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
              <button
                onClick={handleAskAI}
                disabled={loading || !query.trim()}
                className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center"
              >
                {loading ? (
                  <>Loading...</>
                ) : (
                  <>
                    <Send className="w-4 h-4 mr-2" />
                    Ask
                  </>
                )}
              </button>
            </div>

            {/* Quick Query Buttons */}
            <div className="flex flex-wrap gap-2 mb-4">
              {[
                "What's causing the temperature spike?",
                'Show maintenance history',
                'Recommended actions for high vibration',
              ].map((quickQuery) => (
                <button
                  key={quickQuery}
                  onClick={() => {
                    setQuery(quickQuery);
                    setTimeout(() => handleAskAI(), 100);
                  }}
                  className="px-3 py-1 text-sm bg-gray-100 hover:bg-gray-200 rounded-full text-gray-700"
                >
                  {quickQuery}
                </button>
              ))}
            </div>

            {aiResponse && (
              <div className="bg-blue-50 rounded-lg p-6">
                <div className="prose max-w-none">
                  <h3 className="text-lg font-semibold text-gray-900 mb-3">Response</h3>
                  <p className="text-gray-700 whitespace-pre-wrap">{aiResponse.answer}</p>

                  {aiResponse.recommendations.length > 0 && (
                    <div className="mt-4">
                      <h4 className="font-semibold text-gray-900 mb-2">Recommendations:</h4>
                      <ul className="list-disc list-inside space-y-1">
                        {aiResponse.recommendations.map((rec, idx) => (
                          <li key={idx} className="text-gray-700">
                            {rec}
                          </li>
                        ))}
                      </ul>
                    </div>
                  )}

                  {aiResponse.sources.length > 0 && (
                    <div className="mt-4 pt-4 border-t border-blue-200">
                      <h4 className="font-semibold text-gray-900 text-sm mb-2">Sources:</h4>
                      <div className="flex flex-wrap gap-2">
                        {aiResponse.sources.map((source, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-1 bg-white text-xs rounded border border-blue-200 text-gray-600"
                          >
                            {source}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  <div className="mt-4 text-xs text-gray-500">
                    Confidence: {(aiResponse.confidence * 100).toFixed(0)}%
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default OperatorDashboard;
