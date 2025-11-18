import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Key, FileText, Clock, Code } from 'lucide-react';
import toast from 'react-hot-toast';
import { cacheApi } from '../api/cacheApi';

function AddKey() {
  const [formData, setFormData] = useState({
    key: '',
    value: '',
    ttl: '',
    valueType: 'string',
  });
  const [error, setError] = useState('');
  const queryClient = useQueryClient();

  const addMutation = useMutation({
    mutationFn: cacheApi.putItem,
    onSuccess: () => {
      queryClient.invalidateQueries(['cacheItems']);
      queryClient.invalidateQueries(['stats']);
      toast.success('Item added successfully');
      setFormData({ key: '', value: '', ttl: '', valueType: 'string' });
      setError('');
    },
    onError: (error) => {
      toast.error(`Failed to add item: ${error.message}`);
    },
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    setError('');

    if (!formData.key.trim()) {
      setError('Key is required');
      return;
    }

    if (!formData.value.trim()) {
      setError('Value is required');
      return;
    }

    let parsedValue = formData.value;

    if (formData.valueType === 'number') {
      parsedValue = parseFloat(formData.value);
      if (isNaN(parsedValue)) {
        setError('Invalid number value');
        return;
      }
    } else if (formData.valueType === 'json') {
      try {
        parsedValue = JSON.parse(formData.value);
      } catch (e) {
        setError('Invalid JSON format');
        return;
      }
    }

    const payload = {
      key: formData.key.trim(),
      value: parsedValue,
    };

    if (formData.ttl) {
      const ttlSeconds = parseInt(formData.ttl);
      if (isNaN(ttlSeconds) || ttlSeconds <= 0) {
        setError('TTL must be a positive number');
        return;
      }
      payload.ttl = ttlSeconds;
    }

    addMutation.mutate(payload);
  };

  return (
    <div className="p-6 max-w-4xl mx-auto animate-fade-in">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900">Add Cache Key</h1>
        <p className="text-gray-600 mt-2">Add a new key-value pair to the cache</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Form */}
        <div className="lg:col-span-2">
          <form onSubmit={handleSubmit} className="card space-y-6">
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                {error}
              </div>
            )}

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Key className="inline w-4 h-4 mr-1" />
                Key *
              </label>
              <input
                type="text"
                value={formData.key}
                onChange={(e) => setFormData({ ...formData, key: e.target.value })}
                placeholder="Enter cache key (e.g., user:123)"
                className="input-field"
                disabled={addMutation.isPending}
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <FileText className="inline w-4 h-4 mr-1" />
                Value Type
              </label>
              <div className="flex space-x-4">
                {['string', 'number', 'json'].map((type) => (
                  <label key={type} className="flex items-center">
                    <input
                      type="radio"
                      name="valueType"
                      value={type}
                      checked={formData.valueType === type}
                      onChange={(e) => setFormData({ ...formData, valueType: e.target.value })}
                      className="mr-2"
                      disabled={addMutation.isPending}
                    />
                    <span className="text-sm text-gray-700 capitalize">{type}</span>
                  </label>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <FileText className="inline w-4 h-4 mr-1" />
                Value *
              </label>
              {formData.valueType === 'json' ? (
                <textarea
                  value={formData.value}
                  onChange={(e) => setFormData({ ...formData, value: e.target.value })}
                  placeholder='{"name": "John", "age": 30}'
                  className="input-field font-mono"
                  rows="6"
                  disabled={addMutation.isPending}
                />
              ) : (
                <input
                  type="text"
                  value={formData.value}
                  onChange={(e) => setFormData({ ...formData, value: e.target.value })}
                  placeholder={
                    formData.valueType === 'number' 
                      ? 'Enter a number (e.g., 42)' 
                      : 'Enter a string value'
                  }
                  className="input-field"
                  disabled={addMutation.isPending}
                />
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                <Clock className="inline w-4 h-4 mr-1" />
                TTL (seconds) - Optional
              </label>
              <input
                type="number"
                value={formData.ttl}
                onChange={(e) => setFormData({ ...formData, ttl: e.target.value })}
                placeholder="Leave empty for no expiration"
                className="input-field"
                min="1"
                disabled={addMutation.isPending}
              />
              <p className="mt-1 text-sm text-gray-500">
                Time to live in seconds. If not specified, the item will not expire.
              </p>
            </div>

            <div className="flex justify-end space-x-3">
              <button
                type="button"
                onClick={() => setFormData({ key: '', value: '', ttl: '', valueType: 'string' })}
                className="btn-secondary"
                disabled={addMutation.isPending}
              >
                Clear
              </button>
              <button
                type="submit"
                className="btn-primary flex items-center space-x-2"
                disabled={addMutation.isPending}
              >
                <Plus className="w-4 h-4" />
                <span>{addMutation.isPending ? 'Adding...' : 'Add to Cache'}</span>
              </button>
            </div>
          </form>
        </div>

        {/* Example Payloads */}
        <div className="space-y-4">
          <div className="card">
            <h3 className="font-bold text-gray-900 mb-3 flex items-center">
              <Code className="w-5 h-5 mr-2" />
              Examples
            </h3>
            <div className="space-y-4 text-sm">
              <div>
                <p className="font-medium text-gray-700 mb-1">String Value:</p>
                <pre className="bg-gray-100 p-2 rounded text-xs overflow-x-auto">
{`Key: user:123
Type: string
Value: John Doe`}
                </pre>
              </div>
              <div>
                <p className="font-medium text-gray-700 mb-1">Number Value:</p>
                <pre className="bg-gray-100 p-2 rounded text-xs overflow-x-auto">
{`Key: counter
Type: number
Value: 42`}
                </pre>
              </div>
              <div>
                <p className="font-medium text-gray-700 mb-1">JSON Value:</p>
                <pre className="bg-gray-100 p-2 rounded text-xs overflow-x-auto">
{`Key: profile:456
Type: json
Value: {
  "name": "Jane",
  "age": 28
}`}
                </pre>
              </div>
              <div>
                <p className="font-medium text-gray-700 mb-1">With TTL:</p>
                <pre className="bg-gray-100 p-2 rounded text-xs overflow-x-auto">
{`Key: session:abc
Type: string
Value: active
TTL: 3600`}
                </pre>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default AddKey;
