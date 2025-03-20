import React, { useEffect, useState } from "react";
import axios from "axios";

const JobRecommendations = ({ skills }) => {
  const [jobs, setJobs] = useState([]);

  useEffect(() => {
    const fetchJobs = async () => {
      try {
        const response = await axios.get(`https://job-api.example.com?skills=${skills.join(",")}`);
        setJobs(response.data);
      } catch (error) {
        console.error("Error fetching jobs", error);
      }
    };

    if (skills.length) fetchJobs();
  }, [skills]);

  return (
    <div className="p-6 bg-white shadow-md rounded-lg">
      <h2 className="text-lg font-bold mb-4">Recommended Jobs</h2>
      {jobs.length ? (
        <ul>
          {jobs.map((job, index) => (
            <li key={index} className="border p-2 my-2">{job.title} - {job.company}</li>
          ))}
        </ul>
      ) : (
        <p>No job recommendations found.</p>
      )}
    </div>
  );
};

export default JobRecommendations;
