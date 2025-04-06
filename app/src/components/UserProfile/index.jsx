import React from 'react';
import './UserProfile.css';

const AccountSettingsButton = () => {
    const handleButtonClick = () => {
        // Logic to handle account settings button click
        console.log('Account Settings clicked!');
    };

    return (
        <button className="account-settings-button" onClick={handleButtonClick}>
            Account Settings
        </button>
    );
};

const UserProfile = ({ profilePicture, name, username }) => {
    return (
      <div className="user-profile-container">
        <img src={profilePicture} alt={`${name}'s profile`} className="profile-image" />
        <div className="user-info">
          <h2 className="name">{name}</h2>
          <p className="username">{username}</p>
          <div className="account-settings-container">
            <AccountSettingsButton />
          </div>
        </div>
      </div>
    );
  };

export default UserProfile;