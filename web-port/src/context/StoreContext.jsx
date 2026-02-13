import React, { createContext, useContext, useState, useEffect } from 'react';

const StoreContext = createContext();

export const StoreProvider = ({ children }) => {
  const getInitial = (key, defaultValue) => {
    const saved = localStorage.getItem(key);
    if (saved && saved !== '[]') return JSON.parse(saved);
    return defaultValue;
  };

  const [products, setProducts] = useState(() => getInitial('products', [
    { id: 1, name: 'Creatina Monohidratada', price: 0, stock: 1000, category: 'Insumos', type: 'INSUMO', unit: 'gr' },
    { id: 2, name: 'Whey Protein Vainilla', price: 95000, stock: 10, category: 'Proteínas', type: 'PRODUCTO SIMPLE', unit: 'unid' },
    { id: 3, name: 'Batido Energético', price: 12000, stock: 0, category: 'Combos', type: 'PRODUCTO COMPUESTO', unit: 'unid' }
  ]));
  const [users, setUsers] = useState(() => getInitial('users', [
    { id: 101, name: 'Baki Hanma', phone: '3001234567', balance: 0 },
    { id: 102, name: 'Goku Son', phone: '3119876543', balance: 50000 }
  ]));
  const [sales, setSales] = useState(() => getInitial('sales', []));
  const [purchases, setPurchases] = useState(() => getInitial('purchases', []));
  const [payments, setPayments] = useState(() => getInitial('payments', []));
  const [recipes, setRecipes] = useState(() => getInitial('recipes', [
    { id: 501, productId: 3, ingredientId: 1, quantity: 5 }
  ]));

  // Save to localStorage whenever state changes
  useEffect(() => {
    localStorage.setItem('products', JSON.stringify(products));
    localStorage.setItem('users', JSON.stringify(users));
    localStorage.setItem('sales', JSON.stringify(sales));
    localStorage.setItem('purchases', JSON.stringify(purchases));
    localStorage.setItem('payments', JSON.stringify(payments));
    localStorage.setItem('recipes', JSON.stringify(recipes));
  }, [products, users, sales, purchases, payments, recipes]);

  // --- Product Logic ---
  const addProduct = (name, price, stock, category = "", type = "PRODUCTO SIMPLE", unit = "unid") => {
    const newProduct = {
      id: Date.now(),
      name,
      price: parseFloat(price) || 0,
      stock: parseFloat(stock) || 0,
      category,
      type,
      unit
    };
    setProducts([...products, newProduct]);
    return newProduct.id;
  };

  const updateProduct = (id, name, price, stock, category = "", type = "PRODUCTO SIMPLE", unit = "unid") => {
    setProducts(products.map(p => p.id === id ? { ...p, name, price: parseFloat(price), stock: parseFloat(stock), category, type, unit } : p));
  };

  const deleteProduct = (id) => {
    setProducts(products.filter(p => p.id !== id));
    setRecipes(recipes.filter(r => r.productId !== id));
  };

  // --- User Logic ---
  const addUser = (name, phone) => {
    const newUser = { id: Date.now(), name, phone, balance: 0 };
    setUsers([...users, newUser]);
  };

  const deleteUser = (id) => {
    setUsers(users.filter(u => u.id !== id));
  };

  // --- Recipe Logic ---
  const addRecipeItem = (productId, ingredientId, quantity) => {
    const newItem = { id: Date.now(), productId, ingredientId, quantity: parseFloat(quantity) };
    setRecipes([...recipes, newItem]);
  };

  const deleteRecipe = (productId) => {
    setRecipes(recipes.filter(r => r.productId !== productId));
  };

  // --- Purchase Logic ---
  const recordPurchase = (productId, quantity, costPrice) => {
    const qty = parseFloat(quantity);
    const cost = parseFloat(costPrice);

    // Update Stock
    setProducts(prev => prev.map(p => p.id === productId ? { ...p, stock: p.stock + qty } : p));

    // Record Purchase
    const newPurchase = { id: Date.now(), productId, quantity: qty, costPrice: cost, date: new Date().toISOString() };
    setPurchases([...purchases, newPurchase]);

    // If it's an INSUMO, update its "price" (unit cost)
    const product = products.find(p => p.id === productId);
    if (product?.type === "INSUMO") {
      updateIngredientUnitCost(productId, cost, qty);
    }
  };

  const updateIngredientUnitCost = (id, totalCost, quantity) => {
    if (quantity <= 0) return;
    const unitCost = totalCost / quantity;
    setProducts(prev => prev.map(p => p.id === id ? { ...p, price: unitCost } : p));
  };

  // --- Sale Logic ---
  const recordSale = (productId, quantity, totalPrice, userId = null, method = "Efectivo") => {
    const qty = parseFloat(quantity);
    const total = parseFloat(totalPrice);

    // Deduct Stock (including nested recipes)
    deductStockRecursive(productId, qty);

    // Record Sale
    const newSale = {
      id: Date.now(),
      productId,
      quantity: qty,
      totalPrice: total,
      userId,
      method,
      saleDate: new Date().toISOString()
    };
    setSales([...sales, newSale]);

    // Update User Balance if applicable
    if (userId) {
      setUsers(prev => prev.map(u => u.id === userId ? { ...u, balance: u.balance + total } : u));
    }
  };

  const deductStockRecursive = (productId, qty) => {
    // Basic deduction
    setProducts(prev => prev.map(p => p.id === productId ? { ...p, stock: p.stock - qty } : p));

    // Check for recipe
    const productRecipe = recipes.filter(r => r.productId === productId);
    productRecipe.forEach(item => {
      deductStockRecursive(item.ingredientId, item.quantity * qty);
    });
  };

  // --- Payment Logic ---
  const recordPayment = (userId, amount, method) => {
    const val = parseFloat(amount);
    setUsers(prev => prev.map(u => u.id === userId ? { ...u, balance: u.balance - val } : u));

    const newPayment = {
      id: Date.now(),
      userId,
      amount: val,
      method,
      paymentDate: new Date().toISOString()
    };
    setPayments([...payments, newPayment]);
  };

  // --- Aggregate Logic ---
  const getFinancialSummary = () => {
    const totalSales = sales.reduce((acc, s) => acc + s.totalPrice, 0);
    const totalPurchases = purchases.reduce((acc, p) => acc + p.costPrice, 0);

    const userStats = users.map(u => {
      const userSales = sales.filter(s => s.userId === u.id).reduce((acc, s) => acc + s.totalPrice, 0);
      return { id: u.id, name: u.name, totalBought: userSales, balance: u.balance };
    });

    return { totalSales, totalPurchases, userStats };
  };

  const getCombinedHistory = () => {
    const sMapped = sales.map(s => ({
      id: s.id,
      type: 'VENTA',
      detail: products.find(p => p.id === s.productId)?.name || 'Desconocido',
      info: s.quantity.toString(),
      amount: s.totalPrice,
      date: s.saleDate
    }));

    const pMapped = payments.map(p => ({
      id: p.id,
      type: 'PAGO',
      detail: users.find(u => u.id === p.userId)?.name || 'Desconocido',
      info: p.method,
      amount: p.amount,
      date: p.paymentDate
    }));

    return [...sMapped, ...pMapped].sort((a, b) => new Date(b.date) - new Date(a.date));
  };

  return (
    <StoreContext.Provider value={{
      products, addProduct, updateProduct, deleteProduct,
      users, addUser, deleteUser,
      recipes, addRecipeItem, deleteRecipe,
      sales, recordSale,
      purchases, recordPurchase,
      payments, recordPayment,
      getFinancialSummary, getCombinedHistory
    }}>
      {children}
    </StoreContext.Provider>
  );
};

export const useStore = () => useContext(StoreContext);
