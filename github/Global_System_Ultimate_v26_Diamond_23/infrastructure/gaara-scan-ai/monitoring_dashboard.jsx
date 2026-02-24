import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend } from 'recharts';

const MonitoringDashboard = () => {
  const [trainingData, setTrainingData] = useState([]);
  const [crawlerStats, setCrawlerStats] = useState([]);

  useEffect(() => {
    // Fetch data from API (simulated)
    const fetchData = async () => {
      // Replace with actual API calls
      setTrainingData([
        { version: 'v1', accuracy: 0.85, loss: 0.15 },
        { version: 'v2', accuracy: 0.88, loss: 0.12 },
        { version: 'v3', accuracy: 0.92, loss: 0.08 },
      ]);
      
      setCrawlerStats([
        { term: 'Tomato Blight', count: 150 },
        { term: 'Potato Blight', count: 120 },
        { term: 'Corn Rust', count: 90 },
      ]);
    };

    fetchData();
    const interval = setInterval(fetchData, 5000); // Refresh every 5s
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-8 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold mb-8 text-gray-800">ML System Monitoring</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        {/* Training Performance */}
        <Card>
          <CardHeader>
            <CardTitle>Model Training Performance</CardTitle>
          </CardHeader>
          <CardContent>
            <LineChart width={500} height={300} data={trainingData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="version" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="accuracy" stroke="#8884d8" activeDot={{ r: 8 }} />
              <Line type="monotone" dataKey="loss" stroke="#82ca9d" />
            </LineChart>
          </CardContent>
        </Card>

        {/* Crawler Stats */}
        <Card>
          <CardHeader>
            <CardTitle>Crawler Statistics</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {crawlerStats.map((stat, index) => (
                <div key={index} className="flex justify-between items-center p-4 bg-white rounded shadow">
                  <span className="font-medium">{stat.term}</span>
                  <span className="text-blue-600 font-bold">{stat.count} images</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default MonitoringDashboard;
