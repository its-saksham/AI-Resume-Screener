import React from "react";
import Profile from "../components/Profile";

const ProfilePage = ({ screeningResult }) => {
  return (
    <div className="p-10">
      <h1 className="text-2xl font-bold mb-4">Your Profile</h1>
      <Profile screeningResult={screeningResult} />
    </div>
  );
};

export default ProfilePage;
