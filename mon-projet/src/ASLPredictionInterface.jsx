import React, { useState, useEffect } from 'react';
import { Activity, Hand, Brain, Settings, Maximize2, Minimize2 } from 'lucide-react';


const ASLPredictionInterface = () => {
  const [predictions, setPredictions] = useState([]);
  const [currentGesture, setCurrentGesture] = useState(null);
  const [correctedText, setCorrectedText] = useState('');
  const [gestureBuffer, setGestureBuffer] = useState([]);
  const [isConnected, setIsConnected] = useState(false);
  const [correctedText1,setCorrectedText1] = useState('');
  const [stats, setStats] = useState({
    totalGestures: 0,
    avgConfidence: 0,
    sessionTime: 0
  });
  // state for interface settings
  const [isExpanded, setIsExpanded] = useState(true);
  const [settings, setSettings] = useState({
    opacity: 0.8,
    maxPredictions: 10,
    showConfidence: true,
    autoHide: false
  });

  useEffect(() => {
    //connect to websocket server
    const socket = new WebSocket('ws://localhost:8000/ws');
    socket.onopen = () => setIsConnected(true); //sset statut green
    socket.onclose = () => setIsConnected(false); //set statut red
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'prediction') {
        const newPrediction = {
          id: Date.now(),
          gesture: data.gesture,
          confidence: data.confidence,
          timestamp: data.timestamp,
          isNew: true
        };
        // update current gesture and predictions
        setCurrentGesture(newPrediction);
        setPredictions(prev => [newPrediction, ...prev.slice(0, settings.maxPredictions - 1)]);
        setGestureBuffer(prev => [...prev, data.gesture].slice(-5));
        setStats(prev => ({
          totalGestures: prev.totalGestures + 1,
          avgConfidence: ((prev.avgConfidence * prev.totalGestures) + data.confidence) / (prev.totalGestures + 1),
          sessionTime: prev.sessionTime + 1
        }));

        // auto-hide new predictions after 2 seconds
        setTimeout(() => {
          setPredictions(prev => 
            prev.map(p => p.id === newPrediction.id ? {...p, isNew: false} : p)
          );
        }, 2000);
      } else if (data.type === 'correction') {
        setCorrectedText(data.corrected);
      }
    };
    return () => socket.close();
  }, [settings.maxPredictions]);

  //confidence color and bar styles
  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'text-green-400';
    if (confidence >= 0.6) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getConfidenceBarColor = (confidence) => {
    if (confidence >= 0.8) return 'bg-green-500';
    if (confidence >= 0.6) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  return (
    <div className="fixed inset-0 pointer-events-none z-50">
      
      <div 
        className="absolute top-4 right-4 pointer-events-auto"
        style={{ 
          backgroundColor: `rgba(0, 0, 0, ${settings.opacity})`,
          backdropFilter: 'blur(12px)',
          WebkitBackdropFilter: 'blur(12px)',
          opacity: settings.opacity
        }}
      >

        <div className="rounded-2xl border border-white/20 shadow-2xl overflow-hidden">
          <div className="bg-gradient-to-r from-blue-600/80 to-purple-600/80 p-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Hand className="w-6 h-6 text-white" />
                <div>
                  <h1 className="text-white font-bold text-lg">ASL Recognition</h1>
                  <div className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-400' : 'bg-red-400'} animate-pulse`}></div>
                    <span className="text-white/80 text-sm">
                      {isConnected ? 'Connected' : 'Disconnected'}
                    </span>
                  </div>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={() => setSettings(prev => ({ 
                    ...prev, 
                    opacity: Number((prev.opacity === 0.9 ? 0.5 : prev.opacity + 0.1).toFixed(1)) 
                  }))}
                  className="p-2 hover:bg-white/10 rounded-lg transition-colors"
                >
                  <Settings className="w-4 h-4 text-white" />
                </button>
                <button
                  onClick={() => setIsExpanded(!isExpanded)}
                  className="p-2 hover:bg-white/10 rounded-lg transition-colors"
                >
                  {isExpanded ? <Minimize2 className="w-4 h-4 text-white" /> : <Maximize2 className="w-4 h-4 text-white" />}
                </button>
              </div>
            </div>
          </div>
          {isExpanded && (
            <>
              {currentGesture && (
                <div className="p-4 border-b border-white/10">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-white/60 text-sm font-medium">Current Gesture</span>
                    <span className="text-white/40 text-xs">{currentGesture.timestamp}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-white text-xl font-bold capitalize">
                      {currentGesture.gesture}
                    </span>
                    {settings.showConfidence && (
                      <div className="flex items-center gap-2">
                        <span className={`text-sm font-bold ${getConfidenceColor(currentGesture.confidence)}`}>
                          {(currentGesture.confidence * 100).toFixed(1)}%
                        </span>
                        <div className="w-12 h-2 bg-gray-700 rounded-full overflow-hidden">
                          <div 
                            className={`h-full transition-all duration-500 ${getConfidenceBarColor(currentGesture.confidence)}`}
                            style={{ width: `${currentGesture.confidence * 100}%` }}
                          />
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}
              {correctedText && (
                <div className="p-4 border-b border-white/10 bg-gradient-to-r from-green-500/10 to-blue-500/10">
                  <div className="flex items-center gap-2 mb-2">
                    <Brain className="w-4 h-4 text-green-400" />
                    <span className="text-green-400 text-sm font-medium">AI Correction</span>
                  </div>
                  <p className="text-white text-sm italic">"{correctedText}"</p>
                </div>
              )}
              {gestureBuffer.length > 0 && (
                <div className="p-4 border-b border-white/10">
                  <span className="text-white/60 text-sm font-medium block mb-2">Recent Sequence</span>
                  <div className="flex gap-2 flex-wrap">
                    {gestureBuffer.map((gesture, index) => (
                      <span 
                        key={index}
                        className="px-2 py-1 bg-blue-500/20 text-blue-300 text-xs rounded-full border border-blue-400/20"
                      >
                        {gesture}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              <div className="max-h-64 overflow-y-auto">
                <div className="p-4">
                  <div className="flex items-center gap-2 mb-3">
                    <Activity className="w-4 h-4 text-white/60" />
                    <span className="text-white/60 text-sm font-medium">Recent Predictions</span>
                  </div>
                  {predictions.length === 0 ? (
                    <p className="text-white/40 text-sm italic">Waiting for gestures...</p>
                  ) : (
                    <div className="space-y-2">
                      {predictions.map((prediction, index) => (
                        <div 
                          key={prediction.id}
                          className={`flex items-center justify-between p-2 rounded-lg transition-all duration-300 ${
                            prediction.isNew 
                              ? 'bg-blue-500/20 border border-blue-400/30' 
                              : 'bg-white/5 border border-white/10'
                          }`}
                        >

                          <div className="flex items-center gap-3">
                            <span className="text-white/40 text-xs w-8">#{predictions.length - index}</span>
                            <span className="text-white text-sm capitalize font-medium">
                              {prediction.gesture}
                            </span>
                          </div>
                          <div className="flex items-center gap-2">
                            <span className="text-white/40 text-xs">{prediction.timestamp}</span>
                            {settings.showConfidence && (
                              <span className={`text-xs ${getConfidenceColor(prediction.confidence)}`}>
                                {(prediction.confidence * 100).toFixed(0)}%
                              </span>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </div>
        
              <div className="bg-gray-800/50 p-3 border-t border-white/10">
                <div className="grid grid-cols-3 gap-4 text-center">
                  <div>
                    <div className="text-white font-bold text-lg">{stats.totalGestures}</div>
                    <div className="text-white/60 text-xs">Total</div>
                  </div>
                  <div>
                    <div className="text-white font-bold text-lg">
                      {stats.avgConfidence > 0 ? (stats.avgConfidence * 100).toFixed(0) + '%' : '--'}
                    </div>
                    <div className="text-white/60 text-xs">Avg Confidence</div>
                  </div>
                  <div>
                    <div className="text-white font-bold text-lg">
                      {Math.floor(stats.sessionTime / 60)}:{(stats.sessionTime % 60).toString().padStart(2, '0')}
                    </div>
                    <div className="text-white/60 text-xs">Session</div>
                  </div>
                </div>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
};
//export the component
export default ASLPredictionInterface;