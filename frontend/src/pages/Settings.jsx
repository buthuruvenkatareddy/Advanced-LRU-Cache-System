import { useState, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Settings as SettingsIcon, Database, Trash2, Zap, Info } from 'lucide-react';
import toast from 'react-hot-toast';
import { cacheApi } from '../api/cacheApi';
import { useCacheStore } from '../store/cacheStore';

function Settings() {
  const [newCapacity, setNewCapacity] = useState('');
  const [showClearConfirm, setShowClearConfirm] = useState(false);
  const queryClient = useQueryClient();
  
  const { autoRefresh, refreshInterval, setAutoRefresh, setRefreshInterval } = useCacheStore();

  const { data: cacheInfo, isLoading } = useQuery({
    queryKey: ['cacheInfo'],
    queryFn: cacheApi.getCacheInfo,
  });

  useEffect(() => {
    if (cacheInfo) {
      setNewCapacity(cacheInfo.capacity.toString());
    }
  }, [cacheInfo]);

  const updateCapacityMutation = useMutation({
    mutationFn: cacheApi.updateCapacity,
    onSuccess: () => {
      queryClient.invalidateQueries(['cacheInfo']);
      queryClient.invalidateQueries(['stats']);
      toast.success('Capacity updated successfully');
    },
    onError: (error) => {
      toast.error(`Failed to update capacity: ${error.message}`);
    },
  });

  const clearCacheMutation = useMutation({
    mutationFn: cacheApi.clearCache,
    onSuccess: () => {
      queryClient.invalidateQueries(['cacheItems']);
      queryClient.invalidateQueries(['stats']);
      queryClient.invalidateQueries(['cacheInfo']);
      toast.success('Cache cleared successfully');
      setShowClearConfirm(false);
    },
    onError: (error) => {
      toast.error(`Failed to clear cache: ${error.message}`);
    },
  });

  const cleanupExpiredMutation = useMutation({
    mutationFn: cacheApi.cleanupExpired,
    onSuccess: (data) => {
      queryClient.invalidateQueries(['cacheItems']);
      queryClient.invalidateQueries(['stats']);
      toast.success(`Removed ${data.removed_count} expired items`);
    },
    onError: (error) => {
      toast.error(`Failed to cleanup: ${error.message}`);
    },
  });

  const handleUpdateCapacity = (e) => {
    e.preventDefault();
    const capacity = parseInt(newCapacity);
    if (isNaN(capacity) || capacity <= 0) {
      toast.error('Capacity must be a positive number');
      return;
    }
    updateCapacityMutation.mutate(capacity);
  };

  const handleClearCache = () => {
    clearCacheMutation.mutate();
  };

  const handleCleanupExpired = () => {
    cleanupExpiredMutation.mutate();
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-4xl mx-auto space-y-6 animate-fade-in">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
        <p className="text-gray-600 mt-2">Manage cache configuration and preferences</p>
      </div>

      {/* Cache Information */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <Info className="w-6 h-6 text-primary-600" />
          <h2 className="text-xl font-bold text-gray-900">Cache Information</h2>
        </div>
        <div className="grid grid-cols-2 gap-4 text-sm">
          <div>
            <p className="text-gray-600">Current Capacity</p>
            <p className="text-2xl font-bold text-gray-900">{cacheInfo?.capacity}</p>
          </div>
          <div>
            <p className="text-gray-600">Implementation</p>
            <p className="text-xl font-semibold text-gray-900">{cacheInfo?.implementation}</p>
          </div>
        </div>
      </div>

      {/* Update Capacity */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <Database className="w-6 h-6 text-primary-600" />
          <h2 className="text-xl font-bold text-gray-900">Update Cache Capacity</h2>
        </div>
        <form onSubmit={handleUpdateCapacity} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              New Capacity
            </label>
            <input
              type="number"
              value={newCapacity}
              onChange={(e) => setNewCapacity(e.target.value)}
              placeholder="Enter new capacity"
              className="input-field"
              min="1"
              disabled={updateCapacityMutation.isPending}
            />
            <p className="mt-1 text-sm text-gray-500">
              Maximum number of items the cache can hold before eviction occurs.
            </p>
          </div>
          <button
            type="submit"
            className="btn-primary"
            disabled={updateCapacityMutation.isPending}
          >
            {updateCapacityMutation.isPending ? 'Updating...' : 'Update Capacity'}
          </button>
        </form>
      </div>

      {/* Cache Operations */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <Zap className="w-6 h-6 text-yellow-600" />
          <h2 className="text-xl font-bold text-gray-900">Cache Operations</h2>
        </div>
        <div className="space-y-4">
          <div className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
            <div>
              <h3 className="font-medium text-gray-900">Cleanup Expired Items</h3>
              <p className="text-sm text-gray-600">Remove all items that have exceeded their TTL</p>
            </div>
            <button
              onClick={handleCleanupExpired}
              className="btn-secondary"
              disabled={cleanupExpiredMutation.isPending}
            >
              {cleanupExpiredMutation.isPending ? 'Cleaning...' : 'Cleanup'}
            </button>
          </div>

          <div className="flex items-center justify-between p-4 bg-red-50 rounded-lg border border-red-200">
            <div>
              <h3 className="font-medium text-red-900">Clear Entire Cache</h3>
              <p className="text-sm text-red-700">Remove all items from the cache (irreversible)</p>
            </div>
            <button
              onClick={() => setShowClearConfirm(true)}
              className="btn-danger"
            >
              Clear Cache
            </button>
          </div>
        </div>
      </div>

      {/* UI Preferences */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-4">
          <SettingsIcon className="w-6 h-6 text-primary-600" />
          <h2 className="text-xl font-bold text-gray-900">UI Preferences</h2>
        </div>
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="font-medium text-gray-900">Auto-Refresh Data</h3>
              <p className="text-sm text-gray-600">Automatically refresh statistics and cache items</p>
            </div>
            <button
              onClick={() => setAutoRefresh(!autoRefresh)}
              className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                autoRefresh ? 'bg-primary-600' : 'bg-gray-300'
              }`}
            >
              <span
                className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                  autoRefresh ? 'translate-x-6' : 'translate-x-1'
                }`}
              />
            </button>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Refresh Interval (ms)
            </label>
            <select
              value={refreshInterval}
              onChange={(e) => setRefreshInterval(parseInt(e.target.value))}
              className="input-field"
            >
              <option value="3000">3 seconds</option>
              <option value="5000">5 seconds</option>
              <option value="10000">10 seconds</option>
              <option value="30000">30 seconds</option>
            </select>
          </div>
        </div>
      </div>

      {/* Clear Cache Confirmation Modal */}
      {showClearConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="p-3 bg-red-100 rounded-full">
                <Trash2 className="w-6 h-6 text-red-600" />
              </div>
              <h2 className="text-xl font-bold text-gray-900">Clear Cache</h2>
            </div>
            <p className="text-gray-600 mb-6">
              Are you sure you want to clear the entire cache? This will remove all {cacheInfo?.active_keys} items and cannot be undone.
            </p>
            <div className="flex justify-end space-x-3">
              <button
                onClick={() => setShowClearConfirm(false)}
                className="btn-secondary"
                disabled={clearCacheMutation.isPending}
              >
                Cancel
              </button>
              <button
                onClick={handleClearCache}
                className="btn-danger"
                disabled={clearCacheMutation.isPending}
              >
                {clearCacheMutation.isPending ? 'Clearing...' : 'Clear Cache'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default Settings;
