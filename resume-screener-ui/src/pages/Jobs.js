import React from "react";
import JobRecommendations from "../components/JobRecommendations";

const Jobs = ({ screeningResult }) => {
  if (!screeningResult) return <p>Please upload a resume first.</p>;

  return (
    <div className="p-10">
      <h1 className="text-2xl font-bold mb-4">Job Recommendations</h1>
      <JobRecommendations skills={screeningResult["Extracted Skills"] || []} />
    </div>
  );
};

export default Jobs;
