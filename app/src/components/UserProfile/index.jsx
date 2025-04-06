import React from 'react';
import './UserProfile.css';

const UserProfile = ({ profilePicture, name, username }) => {
    return (
        <div className="user-profile-container">
            <img src={profilePicture} alt={`${name}'s profile`} className="profile-image" />
            <div className="user-info">
                <h2 className="name">{name}</h2>
                <p className="username">@{username}</p>
            </div>
        </div>
    );
};

export default UserProfile;