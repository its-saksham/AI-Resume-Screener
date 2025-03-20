import React, { useState } from "react";
import axios from "axios";

const UploadResume = ({ setScreeningResult }) => {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return alert("Please select a file first!");
    
    setLoading(true);
    const formData = new FormData();
    formData.append("resume", file);

    try {
      const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setScreeningResult(response.data);
    } catch (error) {
      alert("Error uploading resume");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="p-6 bg-white shadow-md rounded-lg">
      <input type="file" onChange={handleFileChange} className="mb-2" />
      <button
        onClick={handleUpload}
        disabled={loading}
        className="px-4 py-2 bg-blue-600 text-white rounded-lg"
      >
        {loading ? "Uploading..." : "Upload Resume"}
      </button>
    </div>
  );
};

export default UploadResume;
