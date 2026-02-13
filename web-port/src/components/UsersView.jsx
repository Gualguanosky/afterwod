import React, { useState } from 'react';
import { UserPlus, Search, Trash2, Wallet, ExternalLink, Phone } from 'lucide-react';
import { useStore } from '../context/StoreContext';
import Modal from './Modal';

const UsersView = () => {
    const { users, addUser, deleteUser, recordPayment } = useStore();
    const [searchTerm, setSearchTerm] = useState('');
    const [isUserModalOpen, setUserModalOpen] = useState(false);
    const [isPaymentModalOpen, setPaymentModalOpen] = useState(false);
    const [selectedUser, setSelectedUser] = useState(null);

    // Form States
    const [userFormData, setUserFormData] = useState({ name: '', phone: '' });
    const [paymentData, setPaymentData] = useState({ amount: '', method: 'Efectivo' });

    const handleAddUser = (e) => {
        e.preventDefault();
        addUser(userFormData.name, userFormData.phone);
        setUserModalOpen(false);
        setUserFormData({ name: '', phone: '' });
    };

    const handlePayment = (e) => {
        e.preventDefault();
        if (!selectedUser) return;
        recordPayment(selectedUser.id, paymentData.amount, paymentData.method);
        setPaymentModalOpen(false);
        setPaymentData({ amount: '', method: 'Efectivo' });
        alert(`Abono de $${paymentData.amount} registrado para ${selectedUser.name}`);
    };

    const filteredUsers = users.filter(u =>
        u.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        u.phone?.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="p-6">
            <div className="flex justify-between items-center mb-8">
                <h2 className="text-3xl font-header uppercase">Usuarios y Cartera</h2>
                <button
                    onClick={() => setUserModalOpen(true)}
                    className="militar-btn flex items-center gap-2"
                >
                    <UserPlus size={20} /> NUEVO CLIENTE
                </button>
            </div>

            <div className="militar-card h-[70vh] flex flex-col">
                {/* Search */}
                <div className="relative mb-6">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-text-secondary" size={18} />
                    <input
                        type="text"
                        placeholder="Buscar por nombre o teléfono..."
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
                                <th className="p-4 text-text-secondary font-semibold uppercase text-xs">ID</th>
                                <th className="p-4 text-text-secondary font-semibold uppercase text-xs">Nombre / Contacto</th>
                                <th className="p-4 text-text-secondary font-semibold uppercase text-xs">Saldo (Cartera)</th>
                                <th className="p-4 text-text-secondary font-semibold uppercase text-xs text-right">Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredUsers.map(u => (
                                <tr key={u.id} className="border-b border-border-color hover:bg-white/5 transition-colors group">
                                    <td className="p-4 text-xs font-mono text-text-secondary">{u.id.toString().slice(-6)}</td>
                                    <td className="p-4">
                                        <p className="font-semibold">{u.name}</p>
                                        <p className="text-xs text-text-secondary flex items-center gap-1">
                                            <Phone size={10} /> {u.phone || '-'}
                                        </p>
                                    </td>
                                    <td className={`p-4 font-header text-2xl ${u.balance > 0 ? 'text-accent-color' : 'text-success-color'}`}>
                                        ${u.balance.toFixed(2)}
                                    </td>
                                    <td className="p-4 text-right">
                                        <div className="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                                            <button
                                                title="Registrar Abono"
                                                onClick={() => { setSelectedUser(u); setPaymentModalOpen(true); }}
                                                className="p-3 bg-success-color text-black rounded font-bold hover:scale-105 transition-transform flex items-center gap-2"
                                            >
                                                <Wallet size={16} /> ABONAR
                                            </button>
                                            <button
                                                onClick={() => deleteUser(u.id)}
                                                className="p-3 hover:bg-danger-color/20 text-danger-color rounded transition-colors"
                                            >
                                                <Trash2 size={16} />
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                            {filteredUsers.length === 0 && (
                                <tr>
                                    <td colSpan="4" className="p-10 text-center text-text-secondary italic">
                                        No se encontraron usuarios registrados
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* User Modal */}
            <Modal isOpen={isUserModalOpen} onClose={() => setUserModalOpen(false)} title="Nuevo Cliente">
                <form onSubmit={handleAddUser} className="space-y-6">
                    <div>
                        <label className="text-xs font-bold uppercase text-text-secondary mb-2 block">Nombre Completo</label>
                        <input
                            required
                            className="militar-input text-lg"
                            value={userFormData.name}
                            onChange={e => setUserFormData({ ...userFormData, name: e.target.value })}
                            autoFocus
                        />
                    </div>
                    <div>
                        <label className="text-xs font-bold uppercase text-text-secondary mb-2 block">Teléfono / WhatsApp</label>
                        <input
                            className="militar-input"
                            value={userFormData.phone}
                            onChange={e => setUserFormData({ ...userFormData, phone: e.target.value })}
                        />
                    </div>
                    <div className="flex justify-end gap-3 pt-6 border-t border-border-color">
                        <button type="button" onClick={() => setUserModalOpen(false)} className="militar-btn-secondary uppercase text-xs font-bold">Cancelar</button>
                        <button type="submit" className="militar-btn uppercase font-header px-10">Registrar Cliente</button>
                    </div>
                </form>
            </Modal>

            {/* Payment Modal */}
            <Modal
                isOpen={isPaymentModalOpen}
                onClose={() => setPaymentModalOpen(false)}
                title={`Abonar a: ${selectedUser?.name}`}
            >
                <form onSubmit={handlePayment} className="space-y-6 text-center">
                    <div className="mb-8">
                        <p className="text-text-secondary uppercase text-xs font-bold mb-2">Deuda Actual</p>
                        <p className="text-5xl font-header text-accent-color">${selectedUser?.balance.toFixed(2)}</p>
                    </div>

                    <div className="text-left space-y-4">
                        <div>
                            <label className="text-xs font-bold uppercase text-text-secondary mb-2 block">Monto del Abono ($)</label>
                            <input
                                type="number" step="0.01" required
                                className="militar-input text-2xl text-center"
                                value={paymentData.amount}
                                onChange={e => setPaymentData({ ...paymentData, amount: e.target.value })}
                                autoFocus
                            />
                        </div>
                        <div>
                            <label className="text-xs font-bold uppercase text-text-secondary mb-2 block">Método de Pago</label>
                            <div className="grid grid-cols-2 gap-4">
                                {['Efectivo', 'Nequi'].map(m => (
                                    <button
                                        key={m}
                                        type="button"
                                        onClick={() => setPaymentData({ ...paymentData, method: m })}
                                        className={`p-4 rounded border font-header uppercase tracking-widest ${paymentData.method === m ? 'bg-accent-color text-black border-accent-color' : 'border-border-color hover:bg-white/5'}`}
                                    >
                                        {m}
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>

                    <div className="flex justify-end gap-3 pt-10 border-t border-border-color">
                        <button type="button" onClick={() => setPaymentModalOpen(false)} className="militar-btn-secondary uppercase text-xs font-bold">Cancelar</button>
                        <button type="submit" className="militar-btn uppercase font-header px-10">Confirmar Abono</button>
                    </div>
                </form>
            </Modal>
        </div>
    );
};

export default UsersView;
