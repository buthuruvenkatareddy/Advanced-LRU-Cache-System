import { create } from 'zustand';

export const useCacheStore = create((set) => ({
  autoRefresh: true,
  refreshInterval: 5000,
  logsEnabled: true,
  statsHistory: [],
  
  setAutoRefresh: (value) => set({ autoRefresh: value }),
  
  setRefreshInterval: (interval) => set({ refreshInterval: interval }),
  
  setLogsEnabled: (value) => set({ logsEnabled: value }),
  
  addStatsSnapshot: (stats) => set((state) => {
    const newSnapshot = {
      timestamp: Date.now(),
      hits: stats.hits,
      misses: stats.misses,
      evictions: stats.evictions,
    };
    
    const updatedHistory = [...state.statsHistory, newSnapshot].slice(-20);
    
    return { statsHistory: updatedHistory };
  }),
  
  clearStatsHistory: () => set({ statsHistory: [] }),
}));
