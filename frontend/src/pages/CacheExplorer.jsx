import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Search, X, Eye, Trash2 } from 'lucide-react';
import toast from 'react-hot-toast';
import KeyTable from '../components/KeyTable';
import { cacheApi } from '../api/cacheApi';

function CacheExplorer() {
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedItem, setSelectedItem] = useState(null);
  const [showDeleteConfirm, setShowDeleteConfirm] = useState(null);
  const queryClient = useQueryClient();

  const { data: items, isLoading } = useQuery({
    queryKey: ['cacheItems'],
    queryFn: cacheApi.getAllItems,
    refetchInterval: 5000,
  });

  const deleteMutation = useMutation({
    mutationFn: cacheApi.deleteItem,
    onSuccess: () => {
      queryClient.invalidateQueries(['cacheItems']);
      queryClient.invalidateQueries(['stats']);
      toast.success('Item deleted successfully');
      setShowDeleteConfirm(null);
    },
    onError: (error) => {
      toast.error(`Failed to delete: ${error.message}`);
    },
  });

  const filteredItems = items?.filter(item =>
    item.key.toLowerCase().includes(searchQuery.toLowerCase()) ||
    JSON.stringify(item.value).toLowerCase().includes(searchQuery.toLowerCase())
  ) || [];

  const handleView = (item) => {
    setSelectedItem(item);
  };

  const handleDelete = (key) => {
    setShowDeleteConfirm(key);
  };

  const confirmDelete = () => {
    if (showDeleteConfirm) {
      deleteMutation.mutate(showDeleteConfirm);
    }
  };

  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <h1 className="text-3xl font-bold text-gray-900">Cache Explorer</h1>
        <div className="text-sm text-gray-500">
          {filteredItems.length} item{filteredItems.length !== 1 ? 's' : ''} found
        </div>
      </div>

      {/* Search Bar */}
      <div className="card">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
          <input
            type="text"
            placeholder="Search by key or value..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="input-field pl-10 pr-10"
          />
          {searchQuery && (
            <button
              onClick={() => setSearchQuery('')}
              className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>
      </div>

      {/* Items Table */}
      <div className="card">
        <KeyTable
          items={filteredItems}
          onView={handleView}
          onDelete={handleDelete}
          isLoading={isLoading}
        />
      </div>

      {/* View Item Modal */}
      {selectedItem && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-2xl w-full max-h-[80vh] overflow-hidden">
            <div className="flex items-center justify-between p-6 border-b border-gray-200">
              <h2 className="text-xl font-bold text-gray-900">Item Details</h2>
              <button
                onClick={() => setSelectedItem(null)}
                className="text-gray-400 hover:text-gray-600"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            <div className="p-6 space-y-4 overflow-y-auto max-h-[calc(80vh-100px)]">
              <div>
                <label className="text-sm font-medium text-gray-700">Key</label>
                <code className="block mt-1 p-3 bg-gray-100 rounded text-sm font-mono">
                  {selectedItem.key}
                </code>
              </div>
              <div>
                <label className="text-sm font-medium text-gray-700">Value</label>
                <pre className="block mt-1 p-3 bg-gray-100 rounded text-sm font-mono overflow-x-auto">
                  {JSON.stringify(selectedItem.value, null, 2)}
                </pre>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-sm font-medium text-gray-700">Access Count</label>
                  <p className="mt-1 text-gray-900">{selectedItem.access_count}</p>
                </div>
                <div>
                  <label className="text-sm font-medium text-gray-700">Last Accessed</label>
                  <p className="mt-1 text-gray-900">
                    {new Date(selectedItem.last_accessed).toLocaleString()}
                  </p>
                </div>
                {selectedItem.expires_at && (
                  <div>
                    <label className="text-sm font-medium text-gray-700">Expires At</label>
                    <p className="mt-1 text-gray-900">
                      {new Date(selectedItem.expires_at).toLocaleString()}
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Delete Confirmation Modal */}
      {showDeleteConfirm && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <div className="flex items-center space-x-3 mb-4">
              <div className="p-3 bg-red-100 rounded-full">
                <Trash2 className="w-6 h-6 text-red-600" />
              </div>
              <h2 className="text-xl font-bold text-gray-900">Delete Item</h2>
            </div>
            <p className="text-gray-600 mb-6">
              Are you sure you want to delete the item with key <code className="bg-gray-100 px-2 py-1 rounded font-mono">{showDeleteConfirm}</code>? This action cannot be undone.
            </p>
            <div className="flex justify-end space-x-3">
              <button
                onClick={() => setShowDeleteConfirm(null)}
                className="btn-secondary"
                disabled={deleteMutation.isPending}
              >
                Cancel
              </button>
              <button
                onClick={confirmDelete}
                className="btn-danger"
                disabled={deleteMutation.isPending}
              >
                {deleteMutation.isPending ? 'Deleting...' : 'Delete'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default CacheExplorer;
