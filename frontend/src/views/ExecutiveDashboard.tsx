import React, { useEffect, useState } from 'react';
import { Activity, AlertTriangle, TrendingUp, DollarSign } from 'lucide-react';
import { dashboardAPI, DashboardMetrics } from '../services/api';

const ExecutiveDashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadMetrics();
  }, []);

  const loadMetrics = async () => {
    try {
      const response = await dashboardAPI.getExecutive();
      setMetrics(response.data);
    } catch (error) {
      console.error('Error loading metrics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-lg">Loading dashboard...</div>
      </div>
    );
  }

  if (!metrics) {
    return <div className="p-8">Error loading dashboard data</div>;
  }

  const getHealthColor = (score: number) => {
    if (score >= 80) return 'text-green-600';
    if (score >= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  return (
    <div className="p-8 bg-gray-50 min-h-screen">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-900 mb-8">Executive Dashboard</h1>

        {/* Key Metrics Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <MetricCard
            title="Total Equipment"
            value={metrics.total_equipment}
            icon={<Activity className="w-6 h-6" />}
            color="blue"
          />
          <MetricCard
            title="Average Health"
            value={`${metrics.average_health_score}%`}
            icon={<TrendingUp className="w-6 h-6" />}
            color="green"
          />
          <MetricCard
            title="Active Alerts"
            value={metrics.unresolved_alerts}
            icon={<AlertTriangle className="w-6 h-6" />}
            color="red"
          />
          <MetricCard
            title="MTD Maintenance Cost"
            value={`$${metrics.maintenance_cost_mtd.toLocaleString()}`}
            icon={<DollarSign className="w-6 h-6" />}
            color="purple"
          />
        </div>

        {/* Equipment Status Overview */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-semibold mb-4">Equipment Status Overview</h2>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <StatusCard
              label="Operational"
              count={metrics.operational_count}
              total={metrics.total_equipment}
              color="green"
            />
            <StatusCard
              label="Warning"
              count={metrics.warning_count}
              total={metrics.total_equipment}
              color="yellow"
            />
            <StatusCard
              label="Critical"
              count={metrics.critical_count}
              total={metrics.total_equipment}
              color="red"
            />
            <StatusCard
              label="Energy Efficiency"
              count={metrics.energy_efficiency}
              total={100}
              color="blue"
              suffix="%"
            />
          </div>
        </div>

        {/* Predicted Failures */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-semibold mb-4">Predicted Equipment Failures</h2>
          <div className="space-y-4">
            {metrics.predicted_failures.map((failure, index) => (
              <div
                key={index}
                className="border border-gray-200 rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900">{failure.equipment_name}</h3>
                    <p className="text-sm text-gray-600 mt-1">{failure.reason}</p>
                  </div>
                  <div className="text-right ml-4">
                    <div className="text-2xl font-bold text-red-600">
                      {(failure.failure_probability * 100).toFixed(0)}%
                    </div>
                    <div className="text-sm text-gray-500">Risk</div>
                  </div>
                </div>
                <div className="mt-3 flex items-center justify-between">
                  <span className="text-sm text-gray-500">ID: {failure.equipment_id}</span>
                  <span className="text-sm font-medium text-orange-600">
                    ~{failure.estimated_days} days until failure
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* AI Insights Section */}
        <div className="bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg shadow p-6 mt-8">
          <h2 className="text-xl font-semibold mb-3">AI-Powered Insights</h2>
          <div className="space-y-2 text-gray-700">
            <p className="flex items-start">
              <span className="mr-2">💡</span>
              <span>
                Predictive models indicate PUMP-007 requires immediate attention due to elevated vibration
                levels and bearing degradation.
              </span>
            </p>
            <p className="flex items-start">
              <span className="mr-2">📊</span>
              <span>
                Overall equipment efficiency has improved by 2.3% this month through optimized maintenance
                scheduling.
              </span>
            </p>
            <p className="flex items-start">
              <span className="mr-2">⚡</span>
              <span>
                Energy consumption pattern analysis suggests potential 8% cost reduction through load
                balancing adjustments.
              </span>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

interface MetricCardProps {
  title: string;
  value: string | number;
  icon: React.ReactNode;
  color: 'blue' | 'green' | 'red' | 'purple';
}

const MetricCard: React.FC<MetricCardProps> = ({ title, value, icon, color }) => {
  const colorClasses = {
    blue: 'bg-blue-100 text-blue-600',
    green: 'bg-green-100 text-green-600',
    red: 'bg-red-100 text-red-600',
    purple: 'bg-purple-100 text-purple-600',
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <div className="flex items-center justify-between mb-4">
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>{icon}</div>
      </div>
      <h3 className="text-gray-600 text-sm font-medium">{title}</h3>
      <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
    </div>
  );
};

interface StatusCardProps {
  label: string;
  count: number;
  total: number;
  color: 'green' | 'yellow' | 'red' | 'blue';
  suffix?: string;
}

const StatusCard: React.FC<StatusCardProps> = ({ label, count, total, color, suffix = '' }) => {
  const percentage = Math.round((count / total) * 100);

  const colorClasses = {
    green: 'bg-green-500',
    yellow: 'bg-yellow-500',
    red: 'bg-red-500',
    blue: 'bg-blue-500',
  };

  return (
    <div className="text-center">
      <div className="text-2xl font-bold text-gray-900">
        {count}
        {suffix}
      </div>
      <div className="text-sm text-gray-600 mb-2">{label}</div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className={`h-2 rounded-full ${colorClasses[color]}`}
          style={{ width: `${percentage}%` }}
        ></div>
      </div>
      <div className="text-xs text-gray-500 mt-1">{percentage}%</div>
    </div>
  );
};

export default ExecutiveDashboard;
