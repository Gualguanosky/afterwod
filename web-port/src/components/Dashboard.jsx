import React from 'react';
import { TrendingUp, TrendingDown, Activity, Users as UsersIcon } from 'lucide-react';
import { useStore } from '../context/StoreContext';

const Dashboard = () => {
    const { getFinancialSummary } = useStore();
    const { totalSales, totalPurchases, userStats } = getFinancialSummary();

    const profit = totalSales - totalPurchases;

    return (
        <div className="p-6 space-y-8 max-w-7xl mx-auto">
            <div className="flex flex-col gap-2">
                <h2 className="text-4xl font-header uppercase tracking-tighter">Panel de Control</h2>
                <p className="text-text-secondary">Resumen consolidado de Militar Box</p>
            </div>

            {/* Stats Grid */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div className="militar-card flex items-center justify-between group hover:border-success-color transition-colors">
                    <div>
                        <p className="text-text-secondary text-sm font-bold uppercase mb-1">Ingresos de Hoy</p>
                        <p className="text-4xl font-header text-success-color">${totalSales.toFixed(2)}</p>
                    </div>
                    <div className="bg-success-color/10 p-4 rounded-full text-success-color">
                        <TrendingUp size={32} />
                    </div>
                </div>

                <div className="militar-card flex items-center justify-between group hover:border-danger-color transition-colors">
                    <div>
                        <p className="text-text-secondary text-sm font-bold uppercase mb-1">Inversión Stock</p>
                        <p className="text-4xl font-header text-danger-color">${totalPurchases.toFixed(2)}</p>
                    </div>
                    <div className="bg-danger-color/10 p-4 rounded-full text-danger-color">
                        <TrendingDown size={32} />
                    </div>
                </div>

                <div className="militar-card flex items-center justify-between group hover:border-accent-color transition-colors">
                    <div>
                        <p className="text-text-secondary text-sm font-bold uppercase mb-1">Balance Bruto</p>
                        <p className={`text-4xl font-header ${profit >= 0 ? 'text-accent-color' : 'text-danger-color'}`}>
                            ${profit.toFixed(2)}
                        </p>
                    </div>
                    <div className="bg-accent-color/10 p-4 rounded-full text-accent-color">
                        <Activity size={32} />
                    </div>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* User Stats Table */}
                <div className="militar-card">
                    <div className="flex items-center gap-2 mb-6 border-b border-border-color pb-4">
                        <UsersIcon className="text-accent-color" size={20} />
                        <h3 className="text-xl font-header uppercase">Rendimiento por Cliente</h3>
                    </div>
                    <div className="space-y-4">
                        {userStats.slice(0, 5).map(stat => (
                            <div key={stat.id} className="flex justify-between items-center p-3 rounded bg-white/5 group hover:bg-white/10 transition-colors">
                                <span className="font-semibold">{stat.name}</span>
                                <div className="text-right">
                                    <p className="font-header text-lg">${stat.totalBought.toFixed(2)}</p>
                                    <p className={`text-[10px] font-bold uppercase ${stat.balance > 0 ? 'text-danger-color' : 'text-success-color'}`}>
                                        {stat.balance > 0 ? `DEUDA: $${stat.balance.toFixed(2)}` : 'AL DÍA'}
                                    </p>
                                </div>
                            </div>
                        ))}
                        {userStats.length === 0 && (
                            <p className="p-8 text-center text-text-secondary text-sm italic">Sin datos de ventas por cliente aún</p>
                        )}
                    </div>
                </div>

                {/* Info Card */}
                <div className="militar-card flex flex-col justify-center items-center text-center p-12 bg-gradient-to-br from-card-bg to-sidebar-color">
                    <img src="/logo.png" alt="Logo" className="w-32 opacity-10 mb-6 grayscale" />
                    <h3 className="text-2xl font-header text-text-secondary opacity-50 uppercase italic tracking-widest">
                        Militar Box v2.0
                    </h3>
                    <p className="text-text-secondary text-sm mt-4">Edición Web Port · Afterword</p>
                </div>
            </div>
        </div>
    );
};

export default Dashboard;
