import React, { useState } from 'react';
import { Plus, Search, Edit2, Trash2, Package } from 'lucide-react';
import { useStore } from '../context/StoreContext';
import Modal from './Modal';

const InventoryView = () => {
    const { products, addProduct, updateProduct, deleteProduct, recipes, addRecipeItem, deleteRecipe } = useStore();
    const [searchTerm, setSearchTerm] = useState('');
    const [isModalOpen, setModalOpen] = useState(false);
    const [editingProduct, setEditingProduct] = useState(null);

    // Form State
    const [formData, setFormData] = useState({
        name: '', price: '', stock: '0', category: '',
        type: 'PRODUCTO SIMPLE', unit: 'unid'
    });
    const [ingredients, setIngredients] = useState([]);

    const openModal = (product = null) => {
        if (product) {
            setEditingProduct(product);
            setFormData({
                name: product.name,
                price: product.price.toString(),
                stock: product.stock.toString(),
                category: product.category || '',
                type: product.type,
                unit: product.unit
            });
            // Load recipes for this product
            const productRecipes = recipes.filter(r => r.productId === product.id);
            setIngredients(productRecipes.map(r => ({
                ingredientId: r.ingredientId,
                quantity: r.quantity,
                name: products.find(p => p.id === r.ingredientId)?.name || '?'
            })));
        } else {
            setEditingProduct(null);
            setFormData({ name: '', price: '', stock: '0', category: '', type: 'PRODUCTO SIMPLE', unit: 'unid' });
            setIngredients([]);
        }
        setModalOpen(true);
    };

    const handleSave = (e) => {
        e.preventDefault();
        let pid;
        if (editingProduct) {
            updateProduct(editingProduct.id, formData.name, formData.price, formData.stock, formData.category, formData.type, formData.unit);
            pid = editingProduct.id;
            deleteRecipe(pid);
        } else {
            pid = addProduct(formData.name, formData.price, formData.stock, formData.category, formData.type, formData.unit);
        }

        if (formData.type === 'PRODUCTO COMPUESTO') {
            ingredients.forEach(ing => {
                addRecipeItem(pid, ing.ingredientId, ing.quantity);
            });
        }

        setModalOpen(false);
    };

    const addIngredientRow = (ing) => {
        if (!ing) return;
        setIngredients([...ingredients, { ingredientId: ing.id, name: ing.name, quantity: 1 }]);
    };

    const filteredProducts = products.filter(p =>
        p.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
        p.category?.toLowerCase().includes(searchTerm.toLowerCase())
    );

    return (
        <div className="p-6">
            <div className="flex justify-between items-center mb-8">
                <h2 className="text-3xl font-header uppercase">Inventario</h2>
                <button
                    onClick={() => openModal()}
                    className="militar-btn flex items-center gap-2"
                >
                    <Plus size={20} /> NUEVO ITEM
                </button>
            </div>

            <div className="militar-card h-[70vh] flex flex-col">
                {/* Search */}
                <div className="relative mb-6">
                    <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-text-secondary" size={18} />
                    <input
                        type="text"
                        placeholder="Buscar por nombre o categoría..."
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
                                <th className="p-4 text-text-secondary font-semibold uppercase text-xs">Nombre</th>
                                <th className="p-4 text-text-secondary font-semibold uppercase text-xs">Precio</th>
                                <th className="p-4 text-text-secondary font-semibold uppercase text-xs">Stock</th>
                                <th className="p-4 text-text-secondary font-semibold uppercase text-xs text-right">Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            {filteredProducts.map(p => (
                                <tr key={p.id} className="border-b border-border-color hover:bg-white/5 transition-colors group">
                                    <td className="p-4 text-xs font-mono">{p.id.toString().slice(-6)}</td>
                                    <td className="p-4 font-semibold">
                                        {p.name} <br />
                                        <span className="text-[10px] text-text-secondary uppercase">{p.type}</span>
                                    </td>
                                    <td className="p-4">${p.price.toFixed(2)}</td>
                                    <td className="p-4">
                                        <span className={`w-2 h-2 inline-block rounded-full mr-2 ${p.stock > 10 ? 'bg-success-color' : 'bg-danger-color'}`}></span>
                                        {p.stock} <span className="text-xs text-text-secondary">({p.unit})</span>
                                    </td>
                                    <td className="p-4 text-right">
                                        <div className="flex justify-end gap-2">
                                            <button
                                                onClick={() => openModal(p)}
                                                className="p-2 hover:bg-accent-color/20 text-accent-color rounded transition-colors"
                                            >
                                                <Edit2 size={16} />
                                            </button>
                                            <button
                                                onClick={() => deleteProduct(p.id)}
                                                className="p-2 hover:bg-danger-color/20 text-danger-color rounded transition-colors"
                                            >
                                                <Trash2 size={16} />
                                            </button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                            {filteredProducts.length === 0 && (
                                <tr>
                                    <td colSpan="5" className="p-10 text-center text-text-secondary">
                                        <Package className="mx-auto mb-3 opacity-20" size={48} />
                                        No se encontraron productos
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

            {/* Modal */}
            <Modal
                isOpen={isModalOpen}
                onClose={() => setModalOpen(false)}
                title={editingProduct ? 'Editar Producto' : 'Nuevo Producto'}
            >
                <form onSubmit={handleSave} className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div>
                            <label className="text-xs font-bold uppercase text-text-secondary mb-2 block">Nombre</label>
                            <input
                                required
                                className="militar-input"
                                value={formData.name}
                                onChange={e => setFormData({ ...formData, name: e.target.value })}
                            />
                        </div>
                        <div>
                            <label className="text-xs font-bold uppercase text-text-secondary mb-2 block">Categoría</label>
                            <input
                                className="militar-input"
                                value={formData.category}
                                onChange={e => setFormData({ ...formData, category: e.target.value })}
                            />
                        </div>
                    </div>

                    <div>
                        <label className="text-xs font-bold uppercase text-text-secondary mb-2 block">Tipo de Producto</label>
                        <select
                            className="militar-input"
                            value={formData.type}
                            onChange={e => setFormData({ ...formData, type: e.target.value })}
                        >
                            <option value="PRODUCTO SIMPLE">PRODUCTO SIMPLE</option>
                            <option value="INSUMO">INSUMO</option>
                            <option value="PRODUCTO COMPUESTO">PRODUCTO COMPUESTO (CON RECETA)</option>
                        </select>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        {formData.type !== 'INSUMO' && (
                            <div>
                                <label className="text-xs font-bold uppercase text-text-secondary mb-2 block">Precio de Venta ($)</label>
                                <input
                                    type="number" step="0.01" className="militar-input"
                                    value={formData.price}
                                    onChange={e => setFormData({ ...formData, price: e.target.value })}
                                />
                            </div>
                        )}
                        <div>
                            <label className="text-xs font-bold uppercase text-text-secondary mb-2 block">Unidad (ml, gr, unid...)</label>
                            <input
                                className="militar-input"
                                value={formData.unit}
                                onChange={e => setFormData({ ...formData, unit: e.target.value })}
                            />
                        </div>
                    </div>

                    {formData.type === 'PRODUCTO COMPUESTO' && (
                        <div className="space-y-4 pt-4 border-t border-border-color">
                            <h4 className="font-header text-accent-color uppercase italic">Receta / Composición</h4>
                            <div className="flex gap-2 mb-4">
                                <select
                                    className="militar-input flex-1"
                                    onChange={(e) => addIngredientRow(products.find(p => p.id === parseInt(e.target.value)))}
                                    value=""
                                >
                                    <option value="">+ Agregar Ingrediente/Insumo...</option>
                                    {products.filter(p => p.id !== editingProduct?.id).map(p => (
                                        <option key={p.id} value={p.id}>{p.name} ({p.unit})</option>
                                    ))}
                                </select>
                            </div>
                            <div className="space-y-2 max-h-40 overflow-auto pr-2">
                                {ingredients.map((ing, idx) => (
                                    <div key={idx} className="flex items-center gap-3 p-2 bg-white/5 rounded">
                                        <span className="flex-1 font-semibold">{ing.name}</span>
                                        <input
                                            type="number" step="0.01"
                                            className="militar-input w-24 py-1"
                                            value={ing.quantity}
                                            onChange={e => {
                                                const newIngs = [...ingredients];
                                                newIngs[idx].quantity = parseFloat(e.target.value);
                                                setIngredients(newIngs);
                                            }}
                                        />
                                        <button
                                            type="button"
                                            onClick={() => setIngredients(ingredients.filter((_, i) => i !== idx))}
                                            className="text-danger-color p-1 hover:bg-danger-color/10 rounded"
                                        >
                                            <Trash2 size={16} />
                                        </button>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    <div className="flex justify-end gap-3 pt-6 border-t border-border-color">
                        <button type="button" onClick={() => setModalOpen(false)} className="militar-btn-secondary uppercase text-xs font-bold">Cancelar</button>
                        <button type="submit" className="militar-btn uppercase font-header px-10">Guardar Item</button>
                    </div>
                </form>
            </Modal>
        </div>
    );
};

export default InventoryView;
