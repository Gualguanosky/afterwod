import React, { useState } from 'react';
import { StoreProvider } from './context/StoreContext';
import {
  Calculator,
  Package,
  Users as UsersIcon,
  History,
  BarChart3,
  Menu,
  X
} from 'lucide-react';

import Dashboard from './components/Dashboard';
import InventoryView from './components/InventoryView';
import SalesView from './components/SalesView';
import UsersView from './components/UsersView';
import HistoryView from './components/HistoryView';

function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isSidebarOpen, setSidebarOpen] = useState(true);

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: BarChart3 },
    { id: 'sales', label: 'Ventas', icon: Calculator },
    { id: 'inventory', label: 'Inventario', icon: Package },
    { id: 'users', label: 'Usuarios', icon: UsersIcon },
    { id: 'history', label: 'Historial', icon: History },
  ];

  const renderView = () => {
    switch (activeTab) {
      case 'dashboard': return <Dashboard />;
      case 'inventory': return <InventoryView />;
      case 'sales': return <SalesView />;
      case 'users': return <UsersView />;
      case 'history': return <HistoryView />;
      default: return <Dashboard />;
    }
  };

  return (
    <StoreProvider>
      <div className="flex min-h-screen bg-bg-color text-text-color">
        {/* Sidebar */}
        <aside className={`${isSidebarOpen ? 'w-64' : 'w-20'} bg-sidebar-color transition-all duration-300 border-r border-border-color flex flex-col shrink-0`}>
          <div className="p-4 border-b border-border-color flex items-center justify-between">
            <div className={`flex items-center gap-3 ${!isSidebarOpen && 'hidden'}`}>
              <img src="/logo.png" alt="Militar Box" className="h-10" />
              <span className="font-header text-xl text-accent-color truncate">MILITAR BOX</span>
            </div>
            <button onClick={() => setSidebarOpen(!isSidebarOpen)} className="p-2 hover:bg-white/5 rounded text-text-secondary">
              {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
          </div>

          <nav className="flex-1 py-4 overflow-y-auto overflow-x-hidden">
            {navItems.map(item => (
              <button
                key={item.id}
                onClick={() => setActiveTab(item.id)}
                className={`w-full flex items-center gap-4 px-6 py-4 hover:bg-white/5 transition-colors whitespace-nowrap ${activeTab === item.id ? 'text-accent-color border-r-4 border-accent-color bg-accent-color/5' : 'text-text-secondary'}`}
              >
                <item.icon size={22} className="shrink-0" />
                {isSidebarOpen && <span className="font-semibold">{item.label}</span>}
              </button>
            ))}
          </nav>

          <div className="p-6 text-[10px] text-text-secondary border-t border-border-color text-center">
            {isSidebarOpen ? 'v2.0 Afterword Edition' : 'v2.0'}
          </div>
        </aside>

        {/* Content */}
        <main className="flex-1 overflow-auto">
          {renderView()}
        </main>
      </div>
    </StoreProvider>
  );
}

export default App;
