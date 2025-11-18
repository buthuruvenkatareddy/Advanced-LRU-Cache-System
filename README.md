# 🚀 Advanced LRU Cache System

A full-stack, production-grade Least Recently Used (LRU) Cache implementation with Time-To-Live (TTL) support, thread safety, and a modern React-based monitoring interface.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![React](https://img.shields.io/badge/React-18.3-61dafb.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## 📋 Project Summary

This project implements a high-performance **LRU (Least Recently Used) Cache System** with advanced features for modern applications. The system consists of:

Live Link: https://advanced-lru-cache-system-frontend.onrender.com/

### **Backend** (Python + FastAPI)
- **O(1) Time Complexity** for get/put operations using HashMap + Doubly Linked List
- **Thread-Safe Implementation** with proper locking mechanisms
- **TTL (Time-To-Live) Support** for automatic expiration of cache entries
- **Comprehensive Logging** with structured operation tracking
- **RESTful API** with 11+ endpoints for cache management
- **Statistics & Metrics** for monitoring cache performance
- **Unit Tests** with 45+ test cases ensuring reliability

### **Frontend** (React + JavaScript)
- **Real-Time Dashboard** with live statistics and charts
- **Cache Explorer** for browsing and managing entries
- **Interactive UI** built with TailwindCSS
- **Auto-Refresh** capability for live monitoring
- **Responsive Design** for desktop and mobile devices
- **Toast Notifications** for user feedback

---

## 🛠️ Technologies Used

### **Backend**
| Technology | Purpose |
|------------|---------|
| **Python 3.8+** | Core programming language |
| **FastAPI** | Modern web framework for building APIs |
| **Uvicorn** | ASGI server for running FastAPI |
| **Pydantic** | Data validation and settings management |
| **Pytest** | Unit testing framework |
| **Threading** | Concurrency control for thread safety |

### **Frontend**
| Technology | Purpose |
|------------|---------|
| **React 18.3** | JavaScript library for building UI |
| **Vite** | Fast build tool and dev server |
| **React Router** | Client-side routing |
| **TanStack Query** | Server state management |
| **Zustand** | Global state management |
| **Axios** | HTTP client for API calls |
| **Recharts** | Data visualization library |
| **TailwindCSS** | Utility-first CSS framework |
| **Lucide React** | Beautiful icon library |
| **React Hot Toast** | Toast notifications |

### **Architecture**
- **Data Structure**: HashMap + Doubly Linked List for O(1) operations
- **Design Pattern**: Thread-safe singleton pattern
- **API Architecture**: RESTful API with JSON responses
- **State Management**: React Query for server state, Zustand for client state
- **Proxy Setup**: Vite dev server proxy for seamless API communication

---

## 📸 Application Screenshots

### 1. Dashboard - Overview
![Dashboard Screenshot 1](Advanced%20LRU%20Cache%20System%20ScreenShots/1.png)

**Features Shown:**
- **Statistics Cards**: Displays real-time metrics including:
  - Cache Hits (successful retrievals)
  - Cache Misses (failed lookups)
  - Evictions (LRU removals)
  - Active Keys count
  - Memory usage
  - Total requests
- **Auto-Refresh**: Data updates every 5 seconds automatically
- **Clean Layout**: Organized grid layout showing all key metrics at a glance

---

### 2. Dashboard - Charts & Analytics
![Dashboard Screenshot 2](Advanced%20LRU%20Cache%20System%20ScreenShots/2.png)

**Features Shown:**
- **Hit vs Miss Pie Chart**: Visual representation of cache efficiency
  - Green: Cache Hits (successful)
  - Red: Cache Misses (failed)
  - Percentage breakdown for quick analysis
- **Operations Line Chart**: Time-series graph showing:
  - Hits trend over time
  - Misses trend over time
  - Evictions trend over time
- **Cache Health Summary**: 
  - Hit Rate percentage with color-coded indicator
  - Capacity Utilization progress bar
  - Visual health status of the cache

**How It Works:**
- Charts update in real-time as you interact with the cache
- Historical data shows last 20 data points
- Color-coded for easy interpretation (green = good, red = issues)

---

### 3. Cache Explorer - Browse & Manage
![Cache Explorer Screenshot](Advanced%20LRU%20Cache%20System%20ScreenShots/3.png)

**Features Shown:**
- **Search Functionality**: Filter cache entries by key or value
- **Data Table**: Displays all cache entries with columns:
  - **Key**: Unique identifier (shown in code format)
  - **Value Preview**: First 50 characters of the value
  - **Last Accessed**: Relative time (e.g., "5m ago")
  - **TTL Remaining**: Time until expiration in seconds
  - **Access Count**: Number of times key was accessed
- **Action Buttons**:
  - 👁️ **View**: Opens modal with complete item details
  - 🗑️ **Delete**: Removes item with confirmation dialog
- **Real-Time Updates**: Table refreshes automatically every 5 seconds

**How It Works:**
1. All cache entries are displayed in an organized table
2. Use search bar to quickly find specific keys
3. Click "View" to see full details including JSON formatting
4. Click "Delete" to remove unwanted entries (with safety confirmation)
5. Watch TTL countdown in real-time for expiring keys

---

### 4. Add Key - Create Cache Entries
![Add Key Screenshot](Advanced%20LRU%20Cache%20System%20ScreenShots/4.png)

**Features Shown:**
- **Key Input**: Enter unique cache key (e.g., `user:1001`, `session:abc`)
- **Value Type Selection**: Choose from:
  - **String**: Plain text values
  - **Number**: Numeric values
  - **JSON**: Complex objects and arrays
- **Value Input**: 
  - Text field for string/number
  - Large textarea with syntax highlighting for JSON
- **TTL Configuration**: Optional expiration time in seconds
- **Example Payloads**: Right sidebar showing usage examples
- **Form Validation**: Real-time error messages for invalid inputs

**How It Works:**
1. Enter a unique key name
2. Select value type (string, number, or JSON)
3. Enter the value (JSON is validated automatically)
4. Optionally set TTL in seconds (leave empty for no expiration)
5. Click "Add to Cache" to store the entry
6. Success toast confirms addition
7. Dashboard stats update immediately

**Example Use Cases:**
- Store user sessions with TTL: `session:xyz` → expires in 3600s
- Cache API responses: `api:users:list` → JSON array
- Store counters: `page:views` → numeric value

---

### 5. Settings - Cache Configuration
![Settings Screenshot 1](Advanced%20LRU%20Cache%20System%20ScreenShots/5.png)

**Features Shown:**
- **Cache Information**: 
  - Current capacity (max items before eviction)
  - Implementation type (ThreadSafe LRU Cache with TTL)
- **Update Capacity**: 
  - Form to change maximum cache size
  - Input validation for positive numbers
  - Immediate effect after update
- **Cache Operations**:
  - **Cleanup Expired Items**: Remove all TTL-expired entries manually
  - Shows count of removed items in toast notification

**How It Works:**
1. View current cache configuration at the top
2. Change capacity to control max items (e.g., from 100 to 500)
3. When capacity is exceeded, LRU algorithm evicts least recently used items
4. Use "Cleanup" button to manually remove expired items (otherwise cleaned automatically)

---

### 6. Settings - Advanced Operations
![Settings Screenshot 2](Advanced%20LRU%20Cache%20System%20ScreenShots/6.png)

**Features Shown:**
- **Clear Entire Cache**: 
  - Danger zone with red highlighting
  - Confirmation modal before clearing
  - Irreversible operation warning
  - Shows count of items that will be deleted
- **UI Preferences**:
  - **Auto-Refresh Toggle**: Enable/disable automatic data updates
  - **Refresh Interval**: Choose update frequency (3s, 5s, 10s, 30s)
  - Settings persist across sessions

**How It Works:**
1. **Clear Cache**: 
   - Click "Clear Cache" button
   - Confirmation dialog appears showing item count
   - Confirm to delete all entries
   - All statistics reset to zero
2. **UI Preferences**:
   - Toggle auto-refresh ON for live monitoring
   - Toggle OFF to save resources
   - Adjust refresh interval based on your needs
   - Changes apply immediately

---

## 🏗️ Project Architecture

```
Advanced LRU Cache System/
│
├── backend/                      # Python FastAPI Backend
│   ├── lru/                      # Core LRU Cache Implementation
│   │   ├── __init__.py           # Package exports
│   │   ├── data_models.py        # Data classes (CacheEntry, Stats)
│   │   ├── logger.py             # Structured logging
│   │   ├── utils.py              # Utility functions
│   │   ├── lru_cache.py          # Base LRU Cache (O(1) operations)
│   │   ├── lru_cache_ttl.py      # LRU Cache with TTL support
│   │   └── lru_cache_threadsafe.py  # Thread-safe wrapper
│   │
│   ├── api/                      # REST API
│   │   └── fastapi_app.py        # FastAPI application with endpoints
│   │
│   ├── tests/                    # Unit Tests
│   │   ├── test_lru.py           # LRU core tests
│   │   ├── test_ttl.py           # TTL functionality tests
│   │   └── test_threadsafe.py    # Thread safety tests
│   │
│   ├── benchmarks/               # Performance Testing
│   │   └── benchmark.py          # Benchmark suite
│   │
│   ├── requirements.txt          # Python dependencies
│   └── README.md                 # Backend documentation
│
├── frontend/                     # React Frontend
│   ├── src/
│   │   ├── api/
│   │   │   └── cacheApi.js       # API client for backend
│   │   │
│   │   ├── components/           # Reusable Components
│   │   │   ├── Navbar.jsx        # Top navigation
│   │   │   ├── Sidebar.jsx       # Side navigation
│   │   │   ├── StatsCard.jsx     # Statistics card
│   │   │   ├── KeyTable.jsx      # Cache items table
│   │   │   └── Charts/           # Chart components
│   │   │       ├── HitMissPieChart.jsx
│   │   │       └── OperationsLineChart.jsx
│   │   │
│   │   ├── pages/                # Page Components
│   │   │   ├── Dashboard.jsx     # Main dashboard
│   │   │   ├── CacheExplorer.jsx # Browse cache
│   │   │   ├── AddKey.jsx        # Add new entries
│   │   │   └── Settings.jsx      # Configuration
│   │   │
│   │   ├── store/
│   │   │   └── cacheStore.js     # Zustand global state
│   │   │
│   │   ├── utils/
│   │   │   └── helpers.js        # Utility functions
│   │   │
│   │   ├── App.jsx               # Main app with routing
│   │   ├── main.jsx              # Entry point
│   │   └── index.css             # Global styles
│   │
│   ├── index.html                # HTML template
│   ├── package.json              # Node dependencies
│   ├── vite.config.js            # Vite configuration
│   ├── tailwind.config.js        # Tailwind configuration
│   └── README.md                 # Frontend documentation
│
├── Advanced LRU Cache System ScreenShots/  # Application screenshots
│   ├── 1.png                     # Dashboard stats
│   ├── 2.png                     # Dashboard charts
│   ├── 3.png                     # Cache Explorer
│   ├── 4.png                     # Add Key
│   ├── 5.png                     # Settings - Config
│   └── 6.png                     # Settings - Operations
│
├── .gitignore                    # Git ignore rules
└── README.md                     # This file

```

---

## 📦 Installation & Setup

### **Prerequisites**
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn package manager

### **Step 1: Clone the Repository**
```bash
git clone https://github.com/buthuruvenkatareddy/Advanced-LRU-Cache-System.git
cd Advanced-LRU-Cache-System
```

### **Step 2: Backend Setup**

```bash
# Navigate to backend directory
cd backend

# Install Python dependencies
pip install -r requirements.txt

# Run the FastAPI server
python -m uvicorn api.fastapi_app:app --reload --host 0.0.0.0 --port 8000
```

**Backend will be available at:** `http://localhost:8000`
**API Documentation:** `http://localhost:8000/docs`

### **Step 3: Frontend Setup**

Open a new terminal:

```bash
# Navigate to frontend directory
cd frontend

# Install Node dependencies
npm install

# Start the development server
npm run dev
```

**Frontend will be available at:** `http://localhost:3000`

---

## 🚀 Running the Project

### **Option 1: Manual Start (Recommended for Development)**

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn api.fastapi_app:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### **Option 2: Production Build**

**Backend:**
```bash
cd backend
python -m uvicorn api.fastapi_app:app --host 0.0.0.0 --port 8000 --workers 4
```

**Frontend:**
```bash
cd frontend
npm run build
npm run preview
```

---

## 🧪 Testing

### **Backend Tests**
```bash
cd backend

# Run all tests
pytest

# Run with coverage
pytest --cov=lru --cov-report=html

# Run specific test file
pytest tests/test_lru.py -v
```

### **Backend Benchmarks**
```bash
cd backend
python benchmarks/benchmark.py
```

### **Frontend Testing**
```bash
cd frontend

# Run tests (if configured)
npm test

# Build for production
npm run build
```

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/cache/{key}` | Get cache item by key |
| `POST` | `/cache` | Add/Update cache item |
| `DELETE` | `/cache/{key}` | Delete cache item |
| `GET` | `/all` | Get all cache items |
| `GET` | `/stats` | Get cache statistics |
| `POST` | `/clear` | Clear entire cache |
| `POST` | `/cleanup-expired` | Remove expired items |
| `PUT` | `/capacity` | Update cache capacity |
| `GET` | `/cache-info` | Get cache configuration |
| `GET` | `/health` | Health check endpoint |
| `GET` | `/docs` | Interactive API documentation |

---

## 🎯 Key Features

### **Backend Features**
✅ O(1) time complexity for get/put operations  
✅ Thread-safe implementation with locks  
✅ TTL support with automatic expiration  
✅ Comprehensive logging and statistics  
✅ RESTful API with CORS support  
✅ 45+ unit tests with high coverage  
✅ Performance benchmarks included  
✅ PEP-8 compliant code  

### **Frontend Features**
✅ Real-time dashboard with live updates  
✅ Interactive cache explorer with search  
✅ Form validation and error handling  
✅ Responsive design (mobile + desktop)  
✅ Auto-refresh with configurable intervals  
✅ Toast notifications for user feedback  
✅ Data visualization with charts  
✅ Modern UI with TailwindCSS  

---

## 🔧 Configuration

### **Backend Configuration**
Edit `backend/api/fastapi_app.py`:
```python
# Default cache capacity
cache = ThreadSafeLRUCache(capacity=100)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **Frontend Configuration**
Edit `frontend/vite.config.js`:
```javascript
export default defineConfig({
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})
```

---

## 📈 Performance Metrics

- **Get Operation**: O(1) - Constant time
- **Put Operation**: O(1) - Constant time
- **Delete Operation**: O(1) - Constant time
- **Memory Efficiency**: Minimal overhead with HashMap + Doubly Linked List
- **Thread Safety**: Lock-based synchronization with negligible contention
- **API Response Time**: < 10ms for most operations

---

## 🐛 Troubleshooting

### **Backend Issues**

**Problem:** `ModuleNotFoundError: No module named 'fastapi'`  
**Solution:**
```bash
pip install -r requirements.txt
```

**Problem:** Port 8000 already in use  
**Solution:**
```bash
# Change port in command
python -m uvicorn api.fastapi_app:app --reload --port 8001
```

### **Frontend Issues**

**Problem:** `npm install` fails  
**Solution:**
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Problem:** "Network Error" in frontend  
**Solution:**
- Ensure backend is running on port 8000
- Check CORS settings in backend
- Verify proxy configuration in `vite.config.js`

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📝 License

This project is open-source and available under the MIT License.

---

## 👤 Author

**Venkat Buthuru**

- GitHub: [@buthuruvenkatareddy](https://github.com/buthuruvenkatareddy)
- Project Link: [Advanced LRU Cache System](https://github.com/buthuruvenkatareddy/Advanced-LRU-Cache-System)

---

## 🙏 Acknowledgments

- FastAPI for the excellent web framework
- React team for the powerful UI library
- TailwindCSS for the utility-first CSS framework
- Recharts for beautiful data visualizations
- All open-source contributors who made this project possible

---

**⭐ If you find this project helpful, please give it a star on GitHub!**

---

**Built with ❤️ by Venkat Buthuru**
