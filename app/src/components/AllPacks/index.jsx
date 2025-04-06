import React from 'react';
import './AllPacks.css';

const AllPacks = () => {
    return (
        <div className="all-packs-container">
            <h2>All Packs</h2>
            <div className="card-container">
                <div className="card">
                    <h3>Pack 1</h3>
                    <p>Description of Pack 1</p>
                </div>
                <div className="card">
                    <h3>Pack 2</h3>
                    <p>Description of Pack 2</p>
                </div>
                <div className="card">
                    <h3>Pack 3</h3>
                    <p>Description of Pack 3</p>
                </div>
                <div className="card">
                    <h3>Pack 4</h3>
                    <p>Description of Pack 1</p>
                </div>
                <div className="card">
                    <h3>Pack 5</h3>
                    <p>Description of Pack 2</p>
                </div>
                <div className="card">
                    <h3>Pack 6</h3>
                    <p>Description of Pack 3</p>
                </div>
            </div>
        </div>
    );
};

export default AllPacks;