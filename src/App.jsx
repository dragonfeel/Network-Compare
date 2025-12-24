import React, { useState, useMemo } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import ProductCard from './components/ProductCard';
import { aps } from './data/aps';
import './styles/components.css'; // Import our styles

function App() {
  const [searchTerm, setSearchTerm] = useState('');
  const [filters, setFilters] = useState({
    vendor: ['Juniper', 'Aruba'], // Default to showing requested vendors
    standard: []
  });

  const handleFilterChange = (category, value) => {
    if (category === 'reset') {
      setFilters({ vendor: [], standard: [] });
      setSearchTerm('');
      return;
    }

    setFilters(prev => {
      const current = prev[category];
      const updated = current.includes(value)
        ? current.filter(item => item !== value)
        : [...current, value];
      return { ...prev, [category]: updated };
    });
  };

  const filteredProducts = useMemo(() => {
    return aps.filter(product => {
      // Search Filter
      const matchesSearch =
        product.model.toLowerCase().includes(searchTerm.toLowerCase()) ||
        product.vendor.toLowerCase().includes(searchTerm.toLowerCase());

      // Vendor Filter
      const matchesVendor = filters.vendor.length === 0 || filters.vendor.includes(product.vendor);

      // Standard Filter
      const matchesStandard = filters.standard.length === 0 || filters.standard.includes(product.standard);

      return matchesSearch && matchesVendor && matchesStandard;
    });
  }, [searchTerm, filters]);

  return (
    <div className="app-container">
      <Sidebar filters={filters} onFilterChange={handleFilterChange} />

      <main className="main-content">
        <Header searchTerm={searchTerm} onSearchChange={setSearchTerm} />

        <div style={{ marginBottom: '1rem', color: '#94a3b8' }}>
          <h2>Access Points</h2>
          <span style={{ fontSize: '0.9rem' }}>{filteredProducts.length} results found</span>
        </div>

        <div className="product-grids">
          {filteredProducts.map(product => (
            <ProductCard key={product.id} product={product} />
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;
