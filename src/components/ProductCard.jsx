import React from 'react';
import { Wifi, Zap, Network, Layers } from 'lucide-react';

export default function ProductCard({ product }) {
    const getBadgeClass = (std) => {
        if (std === 'Wi-Fi 7') return 'badge badge-wifi7';
        if (std === 'Wi-Fi 6E') return 'badge badge-wifi6e';
        return 'badge badge-wifi6';
    };

    return (
        <div className="product-card">
            <div className="card-top">
                <span className={getBadgeClass(product.standard)}>{product.standard}</span>
                {/* Placeholder for checkbox or comparison toggle if needed later */}
            </div>

            <div className="vendor-name">{product.vendor}</div>
            <div className="product-name">{product.model}</div>

            <div className="specs-grid">
                <div className="spec-item">
                    <Zap className="spec-icon" />
                    <span>{product.throughput}</span>
                </div>
                <div className="spec-item">
                    <Layers className="spec-icon" /> {/* Using Layers for Radios/MIMO */}
                    <span>{product.radios}</span>
                </div>
                <div className="spec-item">
                    <Network className="spec-icon" />
                    <span>{product.ports}</span>
                </div>
            </div>

            <button className="view-details-btn">View Details</button>
        </div>
    );
}
