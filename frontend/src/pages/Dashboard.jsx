import { useQuery } from '@tanstack/react-query';
import { useEffect } from 'react';
import { Target, XCircle, Zap, Clock, Database, TrendingUp } from 'lucide-react';
import StatsCard from '../components/StatsCard';
import HitMissPieChart from '../components/Charts/HitMissPieChart';
import OperationsLineChart from '../components/Charts/OperationsLineChart';
import { cacheApi } from '../api/cacheApi';
import { useCacheStore } from '../store/cacheStore';
import { formatBytes } from '../utils/helpers';

function Dashboard() {
  const { data: stats, isLoading, error } = useQuery({
    queryKey: ['stats'],
    queryFn: cacheApi.getStats,
    refetchInterval: 5000,
  });

  const { statsHistory, addStatsSnapshot } = useCacheStore();

  useEffect(() => {
    if (stats) {
      addStatsSnapshot(stats);
    }
  }, [stats, addStatsSnapshot]);

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="spinner"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="text-center">
          <XCircle className="w-16 h-16 text-red-500 mx-auto mb-4" />
          <h2 className="text-xl font-bold text-gray-900 mb-2">Failed to Load Stats</h2>
          <p className="text-gray-600">{error.message}</p>
        </div>
      </div>
    );
  }

  const hitRate = stats.total_requests > 0 
    ? ((stats.hits / stats.total_requests) * 100).toFixed(1) 
    : 0;

  const capacityUsed = stats.capacity > 0
    ? ((stats.active_keys / stats.capacity) * 100).toFixed(1)
    : 0;

  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <div className="text-sm text-gray-500">
          Auto-refreshing every 5 seconds
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
        <StatsCard
          title="Cache Hits"
          value={stats.hits.toLocaleString()}
          icon={Target}
          iconColor="bg-green-100 text-green-600"
          subtitle="Successful retrievals"
        />
        <StatsCard
          title="Cache Misses"
          value={stats.misses.toLocaleString()}
          icon={XCircle}
          iconColor="bg-red-100 text-red-600"
          subtitle="Failed retrievals"
        />
        <StatsCard
          title="Evictions"
          value={stats.evictions.toLocaleString()}
          icon={Zap}
          iconColor="bg-yellow-100 text-yellow-600"
          subtitle="LRU removals"
        />
        <StatsCard
          title="Expirations"
          value={stats.expirations.toLocaleString()}
          icon={Clock}
          iconColor="bg-purple-100 text-purple-600"
          subtitle="TTL removals"
        />
        <StatsCard
          title="Active Keys"
          value={stats.active_keys.toLocaleString()}
          icon={Database}
          iconColor="bg-blue-100 text-blue-600"
          subtitle={`${capacityUsed}% capacity used`}
        />
        <StatsCard
          title="Total Requests"
          value={stats.total_requests.toLocaleString()}
          icon={TrendingUp}
          iconColor="bg-indigo-100 text-indigo-600"
          subtitle="All operations"
        />
        <StatsCard
          title="Memory Usage"
          value={formatBytes(stats.memory_usage_bytes)}
          icon={Database}
          iconColor="bg-pink-100 text-pink-600"
          subtitle="Approximate size"
        />
        <StatsCard
          title="Hit Rate"
          value={`${hitRate}%`}
          icon={Target}
          iconColor="bg-teal-100 text-teal-600"
          subtitle="Cache efficiency"
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Hit vs Miss Ratio</h2>
          {stats.hits + stats.misses > 0 ? (
            <HitMissPieChart hits={stats.hits} misses={stats.misses} />
          ) : (
            <div className="h-[300px] flex items-center justify-center text-gray-500">
              No data available yet
            </div>
          )}
        </div>

        <div className="card">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Operations Over Time</h2>
          {statsHistory.length > 0 ? (
            <OperationsLineChart data={statsHistory} />
          ) : (
            <div className="h-[300px] flex items-center justify-center text-gray-500">
              Collecting data...
            </div>
          )}
        </div>
      </div>

      {/* Cache Health Summary */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Cache Health Summary</h2>
        <div className="space-y-4">
          <div>
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-gray-700">Hit Rate</span>
              <span className={`text-sm font-bold ${
                hitRate >= 80 ? 'text-green-600' :
                hitRate >= 50 ? 'text-yellow-600' :
                'text-red-600'
              }`}>
                {hitRate}%
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div
                className={`h-2.5 rounded-full ${
                  hitRate >= 80 ? 'bg-green-600' :
                  hitRate >= 50 ? 'bg-yellow-600' :
                  'bg-red-600'
                }`}
                style={{ width: `${hitRate}%` }}
              ></div>
            </div>
          </div>

          <div>
            <div className="flex justify-between items-center mb-2">
              <span className="text-sm font-medium text-gray-700">Capacity Utilization</span>
              <span className="text-sm font-bold text-gray-900">
                {stats.active_keys} / {stats.capacity} keys
              </span>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-2.5">
              <div
                className="bg-primary-600 h-2.5 rounded-full"
                style={{ width: `${capacityUsed}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;
