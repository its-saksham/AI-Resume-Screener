import React, { useState } from "react";
import UploadResume from "../components/UploadResume";
import Profile from "../components/Profile";

const Home = () => {
  const [screeningResult, setScreeningResult] = useState(null);

  return (
    <div className="p-10">
      <h1 className="text-2xl font-bold mb-4">Upload Your Resume</h1>
      <UploadResume setScreeningResult={setScreeningResult} />
      {screeningResult && <Profile screeningResult={screeningResult} />}
    </div>
  );
};

export default Home;
