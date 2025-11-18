import { Eye, Trash2, Clock } from 'lucide-react';
import { formatDistanceToNow } from '../utils/helpers';

function KeyTable({ items, onView, onDelete, isLoading }) {
  if (isLoading) {
    return (
      <div className="flex justify-center items-center py-12">
        <div className="spinner"></div>
      </div>
    );
  }

  if (!items || items.length === 0) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">No cache items found</p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="w-full">
        <thead className="bg-gray-50 border-b border-gray-200">
          <tr>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Key
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Value Preview
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Last Accessed
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              TTL
            </th>
            <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
              Access Count
            </th>
            <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">
              Actions
            </th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {items.map((item) => {
            const valuePreview = typeof item.value === 'string' 
              ? item.value.substring(0, 50) + (item.value.length > 50 ? '...' : '')
              : JSON.stringify(item.value).substring(0, 50) + '...';
            
            const ttlRemaining = item.expires_at 
              ? Math.max(0, Math.floor((new Date(item.expires_at).getTime() - Date.now()) / 1000))
              : null;

            return (
              <tr key={item.key} className="hover:bg-gray-50 transition-colors">
                <td className="px-6 py-4 whitespace-nowrap">
                  <code className="text-sm font-mono bg-gray-100 px-2 py-1 rounded">
                    {item.key}
                  </code>
                </td>
                <td className="px-6 py-4">
                  <span className="text-sm text-gray-700">{valuePreview}</span>
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                  {formatDistanceToNow(new Date(item.last_accessed))}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm">
                  {ttlRemaining !== null ? (
                    <div className="flex items-center space-x-1 text-gray-700">
                      <Clock className="w-4 h-4" />
                      <span>{ttlRemaining}s</span>
                    </div>
                  ) : (
                    <span className="text-gray-400">None</span>
                  )}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-700">
                  {item.access_count}
                </td>
                <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                  <div className="flex justify-end space-x-2">
                    <button
                      onClick={() => onView(item)}
                      className="text-primary-600 hover:text-primary-900 p-1 rounded hover:bg-primary-50 transition-colors"
                      title="View Details"
                    >
                      <Eye className="w-4 h-4" />
                    </button>
                    <button
                      onClick={() => onDelete(item.key)}
                      className="text-red-600 hover:text-red-900 p-1 rounded hover:bg-red-50 transition-colors"
                      title="Delete"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

export default KeyTable;
