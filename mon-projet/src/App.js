import React, { useState, useEffect } from 'react';
import AdCard from './AdCard';

function App() {
  const [ads, setAds] = useState([]);

  useEffect(() => {
    fetch('/scraped_ads_final.json')
      .then((response) => response.json())
      .then((data) => setAds(data))
      .catch((error) => console.error('Erreur de chargement des annonces:', error));
  }, []);

  return (
    <div className="min-h-screen bg-gray-100">
      <header className="bg-blue-600 text-white p-4 text-center">
        <h1 className="text-2xl font-bold">Leboncoin Ads Viewer</h1>
      </header>
      <main className="container mx-auto py-6">
        <h2 className="text-xl font-semibold mb-4">Liste des annonces ({ads.length})</h2>
        {ads.length === 0 ? (
          <p className="text-center text-gray-500">Aucune annonce disponible.</p>
        ) : (
          <div className="space-y-2">
            {ads.map((ad, index) => (
              <AdCard key={index} ad={ad} />
            ))}
          </div>
        )}
      </main>
    </div>
  );
}

export default App;