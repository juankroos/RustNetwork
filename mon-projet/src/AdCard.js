import React from 'react';

const AdCard = ({ ad }) => (
  <div className="bg-white shadow-sm rounded-lg p-2 mb-2 border border-gray-200 flex items-center space-x-4 text-sm">
    <div className="w-20 h-20 flex-shrink-0">
      {ad.image_url !== "Non spécifié" && (
        <img src={ad.image_url} alt={ad.title} className="w-full h-full object-cover rounded" />
      )}
    </div>
    <div className="flex-1">
      <h2 className="font-semibold text-gray-800 line-clamp-1">{ad.title || "Non spécifié"}</h2>
      <p className="text-green-600 font-medium mt-1">{ad.price || "Non spécifié"}</p>
      <p className="text-gray-600">Cat: {ad.category || "Non spécifié"}</p>
      <p className="text-gray-600">Loc: {ad.location || "Non spécifié"}</p>
      <p className="text-gray-600">Date: {ad.date || "Non spécifié"}</p>
      <p className="text-gray-600">Phone: {ad.phone_number || "Non spécifié"}</p>
      <a href={ad.url} target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline text-xs">
        Voir
      </a>
      {ad.tags.length > 0 && (
        <div className="mt-1">
          {ad.tags.map((tag, index) => (
            <span key={index} className="bg-gray-200 text-gray-800 text-xs px-1 py-0.5 rounded-full mr-1">
              {tag}
            </span>
          ))}
        </div>
      )}
      <p className="text-xs text-gray-500 mt-1">Page: {ad.page_source}</p>
    </div>
  </div>
);

export default AdCard;