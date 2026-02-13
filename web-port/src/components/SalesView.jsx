import React, { useState } from 'react';
import { ShoppingCart, User, CreditCard, Banknote, Trash2, Search } from 'lucide-react';
import { useStore } from '../context/StoreContext';

const SalesView = () => {
    const { products, users, recordSale } = useStore();
    const [searchTerm, setSearchTerm] = useState('');
    const [cart, setCart] = useState([]);
    const [selectedUser, setSelectedUser] = useState(null);
    const [paymentMethod, setPaymentMethod] = useState('Efectivo');

    // Only sellable products
    const sellableProducts = products.filter(p =>
        p.type !== 'INSUMO' &&
        p.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const addToCart = (product) => {
        const existing = cart.find(item => item.id === product.id);
        if (existing) {
            setCart(cart.map(item => item.id === product.id ? { ...item, qty: item.qty + 1 } : item));
        } else {
            setCart([...cart, { ...product, qty: 1 }]);
        }
    };

    const removeFromCart = (id) => {
        setCart(cart.filter(item => item.id !== id));
    };

    const cartTotal = cart.reduce((acc, item) => acc + (item.price * item.qty), 0);

    const handleFinishSale = () => {
        if (cart.length === 0) return;

        // In this simple version, we record each item as a sale
        cart.forEach(item => {
            recordSale(item.id, item.qty, item.price * item.qty, selectedUser?.id, paymentMethod);
        });

        setCart([]);
        setSelectedUser(null);
        alert('Venta registrada con éxito');
    };

    return (
        <div className="p-6 grid grid-cols-1 lg:grid-cols-3 gap-6 h-[90vh]">
            {/* Product Selection */}
            <div className="lg:col-span-2 flex flex-col gap-6 overflow-hidden">
                <div className="militar-card flex-1 flex flex-col overflow-hidden">
                    <div className="flex justify-between items-center mb-6">
                        <h3 className="text-xl font-header uppercase">Productos / Combos</h3>
                        <div className="relative w-64">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-text-secondary" size={16} />
                            <input
                                type="text"
                                placeholder="Buscar producto..."
                                className="militar-input py-2 pl-10"
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                            />
                        </div>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-3 gap-4 overflow-auto pb-4">
                        {sellableProducts.map(p => (
                            <button
                                key={p.id}
                                onClick={() => addToCart(p)}
                                className="militar-card hover:border-accent-color p-4 text-left transition-all active:scale-95 group relative overflow-hidden"
                            >
                                <div className="absolute top-0 right-0 p-2 bg-accent-color/10 text-accent-color text-[10px] font-bold">
                                    {p.type.split(' ')[1] || 'SIMPLE'}
                                </div>
                                <p className="font-semibold mb-1 truncate pr-8">{p.name}</p>
                                <p className="text-lg font-header text-accent-color">${p.price.toFixed(2)}</p>
                                <p className="text-xs text-text-secondary">Stock: {p.stock}</p>
                            </button>
                        ))}
                    </div>
                </div>
            </div>

            {/* Cart & Checkout */}
            <div className="militar-card flex flex-col h-full bg-sidebar-color">
                <div className="flex items-center gap-2 mb-6 border-b border-border-color pb-4">
                    <ShoppingCart className="text-accent-color" size={24} />
                    <h3 className="text-xl font-header uppercase">Carrito de Venta</h3>
                </div>

                <div className="flex-1 overflow-auto mb-6">
                    {cart.map(item => (
                        <div key={item.id} className="flex justify-between items-center mb-4 p-2 bg-white/5 rounded">
                            <div>
                                <p className="font-semibold text-sm">{item.name}</p>
                                <p className="text-xs text-text-secondary">{item.qty} x ${item.price.toFixed(2)}</p>
                            </div>
                            <div className="flex items-center gap-3">
                                <span className="font-header text-accent-color">${(item.price * item.qty).toFixed(2)}</span>
                                <button
                                    onClick={() => removeFromCart(item.id)}
                                    className="text-danger-color p-1 hover:bg-danger-color/10 rounded"
                                >
                                    <Trash2 size={16} />
                                </button>
                            </div>
                        </div>
                    ))}
                    {cart.length === 0 && (
                        <div className="h-full flex flex-col items-center justify-center opacity-20">
                            <ShoppingCart size={48} className="mb-2" />
                            <p>El carrito está vacío</p>
                        </div>
                    )}
                </div>

                <div className="mt-auto space-y-4 pt-4 border-t border-border-color">
                    {/* User selector */}
                    <div>
                        <label className="text-xs text-text-secondary uppercase mb-2 block font-bold">Cliente (Opcional)</label>
                        <select
                            className="militar-input text-sm p-3"
                            onChange={(e) => setSelectedUser(users.find(u => u.id === parseInt(e.target.value)))}
                            value={selectedUser?.id || ""}
                        >
                            <option value="">Venta al Público (Contado)</option>
                            {users.map(u => (
                                <option key={u.id} value={u.id}>{u.name} (Saldo: ${u.balance.toFixed(2)})</option>
                            ))}
                        </select>
                    </div>

                    <div className="flex justify-between items-center">
                        <span className="text-text-secondary font-bold uppercase text-xs">Total</span>
                        <span className="text-3xl font-header text-accent-color">${cartTotal.toFixed(2)}</span>
                    </div>

                    <button
                        onClick={handleFinishSale}
                        className="militar-btn w-full py-4 text-lg font-header flex items-center justify-center gap-2"
                    >
                        {selectedUser ? <CreditCard size={20} /> : <Banknote size={20} />}
                        FINALIZAR {selectedUser ? 'FIADO' : 'COBRO'}
                    </button>
                </div>
            </div>
        </div>
    );
};

export default SalesView;
