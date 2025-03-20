import React from "react";

const Profile = ({ screeningResult }) => {
  if (!screeningResult) return <p>No screening data available.</p>;

  return (
    <div className="p-6 bg-white shadow-md rounded-lg">
      <h2 className="text-lg font-bold mb-4">Your Skills Analysis</h2>
      <p><strong>Matched Skills:</strong> {screeningResult["Matched Skills"].join(", ")}</p>
      <p><strong>Missing Skills:</strong> {screeningResult["Missing Skills"].join(", ")}</p>
      <p><strong>Match Percentage:</strong> {screeningResult["Match Percentage"]}%</p>
    </div>
  );
};

export default Profile;
