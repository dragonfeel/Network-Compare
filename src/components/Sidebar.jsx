import React from 'react';

export default function Sidebar({ filters, onFilterChange }) {
    const vendors = ['Aruba', 'Juniper', 'Cisco', 'Meraki', 'Extreme'];
    const standards = ['Wi-Fi 7', 'Wi-Fi 6E', 'Wi-Fi 6', 'Wi-Fi 5'];

    const handleCheckboxChange = (category, value) => {
        onFilterChange(category, value);
    };

    return (
        <aside className="sidebar">
            <div className="sidebar-header">
                <h3>Filters</h3>
                <span
                    style={{ fontSize: '0.8rem', color: '#3b82f6', cursor: 'pointer' }}
                    onClick={() => onFilterChange('reset')}
                >
                    Reset
                </span>
            </div>

            <div className="filter-group">
                <div className="filter-title">VENDOR</div>
                {vendors.map((vendor) => (
                    <label key={vendor} className="filter-item">
                        <input
                            type="checkbox"
                            checked={filters.vendor.includes(vendor)}
                            onChange={() => handleCheckboxChange('vendor', vendor)}
                        />
                        {vendor}
                    </label>
                ))}
            </div>

            <div className="filter-group">
                <div className="filter-title">WI-FI STANDARD</div>
                {standards.map((std) => (
                    <label key={std} className="filter-item">
                        <input
                            type="checkbox"
                            checked={filters.standard.includes(std)}
                            onChange={() => handleCheckboxChange('standard', std)}
                        />
                        {std}
                    </label>
                ))}
            </div>
        </aside>
    );
}
