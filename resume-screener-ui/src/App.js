/*import React, { useState } from "react";
import axios from "axios";

function App() {
  const [file, setFile] = useState(null);
  const [skills, setSkills] = useState([]);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file first!");
      return;
    }

    const formData = new FormData();
    formData.append("resume", file);

    try {
      const response = await axios.post("http://127.0.0.1:5000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setSkills(response.data.skills);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <div className="container">
      <h1>AI Resume Screener</h1>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload & Analyze</button>

      {skills.length > 0 && (
        <div>
          <h2>Extracted Skills:</h2>
          <ul>
            {skills.map((skill, index) => (
              <li key={index}>{skill}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
*/
import React, { useState } from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import Home from "./Pages/Home";
import Jobs from "./Pages/Jobs";
import ProfilePage from "./Pages/ProfilePage";

function App() {
  const [screeningResult, setScreeningResult] = useState(null);

  return (
    <Router>
      <nav className="p-4 bg-gray-800 text-white flex space-x-4">
        <Link to="/">Home</Link>
        <Link to="/jobs">Jobs</Link>
        <Link to="/profile">Profile</Link>
      </nav>
      <Routes>
        <Route path="/" element={<Home setScreeningResult={setScreeningResult} />} />
        <Route path="/jobs" element={<Jobs screeningResult={screeningResult} />} />
        <Route path="/profile" element={<ProfilePage screeningResult={screeningResult} />} />
      </Routes>
    </Router>
  );
}

export default App;
