import React from 'react';
import { Search, Wifi } from 'lucide-react';

export default function Header({ searchTerm, onSearchChange }) {
    return (
        <div className="header">
            <div className="logo">
                <Wifi color="#3b82f6" />
                <span>NetCompare</span>
            </div>
            <div className="search-container">
                <Search className="search-icon" size={18} />
                <input
                    type="text"
                    placeholder="Search models, brands, or specs..."
                    className="search-input"
                    value={searchTerm}
                    onChange={(e) => onSearchChange(e.target.value)}
                />
            </div>
            <div style={{ width: '100px' }}></div> {/* Spacer for balance */}
        </div>
    );
}
