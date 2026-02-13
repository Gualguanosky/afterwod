import React, { useState } from 'react';
import { Search, History as HistoryIcon, ArrowUpRight, ArrowDownLeft } from 'lucide-react';
import { useStore } from '../context/StoreContext';

const HistoryView = () => {
    const { getCombinedHistory } = useStore();
    const [searchTerm, setSearchTerm] = useState('');

    const history = getCombinedHistory();
    const filteredHistory = history.filter(h =>
        h.detail.toLowerCase().includes(searchTerm.toLowerCase()) ||
        h.type.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="p-6">
            <div className="flex justify-between items-center mb-8">
                <h2 className="text-3xl font-header uppercase">Historial de Movimientos</h2>
            </div>

            <div className="militar-card h-[70vh] flex flex-col">
                {/* Search */}
                <div className="relative mb-6">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-text-secondary" size={18} />
                    <input
                        type="text"
                        placeholder="Buscar por detalle o tipo..."
                        className="militar-input pl-10"
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>

                {/* Table */}
                <div className="flex-1 overflow-auto">
                    <table className="w-full text-left border-collapse">
                        <thead className="sticky top-0 bg-card-bg border-b border-border-color">
                            <tr>
                                <th className="p-4 text-text-secondary font-semibold uppercase text-xs">Tipo</th>
                                <th className="p-4 text-text-secondary font-semibold uppercase text-xs">Detalle</th>
                                <th className="p-4 text-text-secondary font-semibold uppercase text-xs">Info/Método</th>
                                <th className="p-4 text-text-secondary font-semibold uppercase text-xs">Monto</th>
                                <th className="p-4 text-text-secondary font-semibold uppercase text-xs">Fecha</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredHistory.map(h => (
                                <tr key={`${h.type}-${h.id}`} className="border-b border-border-color hover:bg-white/5 transition-colors">
                                    <td className="p-4">
                                        <div className="flex items-center gap-2">
                                            {h.type === 'VENTA' ?
                                                <ArrowUpRight size={16} className="text-accent-color" /> :
                                                <ArrowDownLeft size={16} className="text-success-color" />
                                            }
                                            <span className={`font-bold text-xs ${h.type === 'VENTA' ? 'text-accent-color' : 'text-success-color'}`}>
                                                {h.type}
                                            </span>
                                        </div>
                                    </td>
                                    <td className="p-4 font-semibold">{h.detail}</td>
                                    <td className="p-4 text-text-secondary">{h.info}</td>
                                    <td className="p-4 font-header text-lg">${h.amount.toFixed(2)}</td>
                                    <td className="p-4 text-xs text-text-secondary">
                                        {new Date(h.date).toLocaleString()}
                                    </td>
                                </tr>
                            ))}
                            {filteredHistory.length === 0 && (
                                <tr>
                                    <td colSpan="5" className="p-10 text-center text-text-secondary">
                                        <HistoryIcon className="mx-auto mb-3 opacity-20" size={48} />
                                        No hay movimientos registrados
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
};

export default HistoryView;
