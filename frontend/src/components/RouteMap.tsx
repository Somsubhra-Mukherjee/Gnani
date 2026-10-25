import React, { useState } from 'react';
import { RouteMapData } from '../types';
import { MapPin, Navigation, AlertTriangle, CheckCircle2, ShieldAlert } from 'lucide-react';

interface RouteMapProps {
  routeMap: RouteMapData;
}

export const RouteMap: React.FC<RouteMapProps> = ({ routeMap }) => {
  const [selectedRoute, setSelectedRoute] = useState<string | null>(null);
  const [selectedMarker, setSelectedMarker] = useState<any | null>(null);

  if (!routeMap || (routeMap.routes.length === 0 && routeMap.markers.length === 0)) {
    return null;
  }

  // Geographic bounds for Indian subcontinent projection
  // Lat: 8 to 36, Lng: 68 to 92
  const minLat = 10.0;
  const maxLat = 35.0;
  const minLng = 72.0;
  const maxLng = 88.0;

  const width = 600;
  const height = 450;
  const pad = 40;

  const projectLng = (lng: number) => {
    return pad + ((lng - minLng) / (maxLng - minLng)) * (width - pad * 2);
  };

  const projectLat = (lat: number) => {
    // Invert Y for SVG coordinates
    return height - pad - ((lat - minLat) / (maxLat - minLat)) * (height - pad * 2);
  };

  // Known city coordinates for route linking
  const cityCoords: Record<string, { lat: number; lng: number }> = {
    Delhi: { lat: 28.6139, lng: 77.209 },
    Jaipur: { lat: 26.9124, lng: 75.7873 },
    Chandigarh: { lat: 30.7333, lng: 76.7794 },
    Srinagar: { lat: 34.0837, lng: 74.7973 },
    Mumbai: { lat: 19.076, lng: 72.8777 },
    Pune: { lat: 18.5204, lng: 73.8567 },
    Bengaluru: { lat: 12.9716, lng: 77.5946 },
    Hyderabad: { lat: 17.385, lng: 78.4867 },
    Ahmedabad: { lat: 23.0225, lng: 72.5714 },
    Kolkata: { lat: 22.5726, lng: 88.3639 }
  };

  return (
    <div className="bg-slate-900/80 border border-slate-800 rounded-2xl p-5 shadow-lg my-5">
      <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <Navigation className="w-4 h-4 text-blue-400" />
          <h3 className="font-semibold text-sm text-slate-100">
            India Cold-Chain Logistics & Route Surveillance Map
          </h3>
        </div>
        <span className="text-xs text-slate-400">
          {routeMap.routes.length} Active Corridors • {routeMap.markers.length} Monitored Facilities
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 items-center">
        {/* SVG Route Visualization Map */}
        <div className="lg:col-span-2 relative bg-slate-950/60 rounded-xl border border-slate-800/80 p-3 overflow-hidden">
          <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-auto">
            {/* Background Map Grid / Contour */}
            <rect width={width} height={height} fill="#090D16" rx="8" />

            {/* Latitude / Longitude Subtle Grid */}
            {[15, 20, 25, 30].map((lat) => (
              <line
                key={lat}
                x1={pad}
                y1={projectLat(lat)}
                x2={width - pad}
                y2={projectLat(lat)}
                stroke="#1E293B"
                strokeDasharray="4 6"
              />
            ))}

            {/* Route Connecting Lines */}
            {routeMap.routes.map((rt) => {
              const orig = cityCoords[rt.origin];
              const dest = cityCoords[rt.dest];
              if (!orig || !dest) return null;

              const x1 = projectLng(orig.lng);
              const y1 = projectLat(orig.lat);
              const x2 = projectLng(dest.lng);
              const y2 = projectLat(dest.lat);

              const isDisrupted = rt.status.toLowerCase().includes('flood') || rt.status.toLowerCase().includes('delay') || rt.status.toLowerCase().includes('high cost');
              const isSelected = selectedRoute === rt.code;

              return (
                <g key={rt.code} onClick={() => setSelectedRoute(rt.code)} className="cursor-pointer group">
                  <line
                    x1={x1}
                    y1={y1}
                    x2={x2}
                    y2={y2}
                    stroke={isDisrupted ? '#EF4444' : '#3B82F6'}
                    strokeWidth={isSelected ? 4 : isDisrupted ? 2.5 : 2}
                    strokeDasharray={isDisrupted ? '6 4' : undefined}
                    className="transition-all duration-200"
                  />
                  {/* Midpoint marker for route status */}
                  <circle
                    cx={(x1 + x2) / 2}
                    cy={(y1 + y2) / 2}
                    r={isSelected ? 6 : 4}
                    fill={isDisrupted ? '#EF4444' : '#3B82F6'}
                    stroke="#0F172A"
                    strokeWidth="2"
                  />
                </g>
              );
            })}

            {/* Facility Hub Markers */}
            {routeMap.markers.map((mk, idx) => {
              const cx = projectLng(mk.longitude);
              const cy = projectLat(mk.latitude);
              const isIncident = mk.marker_type === 'incident';
              const isSelected = selectedMarker?.name === mk.name;

              return (
                <g
                  key={idx}
                  transform={`translate(${cx}, ${cy})`}
                  onClick={() => setSelectedMarker(mk)}
                  className="cursor-pointer group"
                >
                  {isIncident && (
                    <circle r="12" fill="#EF4444" opacity="0.3" className="animate-ping" />
                  )}
                  <circle
                    r={isSelected ? 8 : 6}
                    fill={isIncident ? '#EF4444' : '#10B981'}
                    stroke="#FFFFFF"
                    strokeWidth="2"
                    className="transition-all hover:scale-125"
                  />
                  <text
                    x={8}
                    y={3}
                    fill={isIncident ? '#F87171' : '#E2E8F0'}
                    fontSize="10"
                    fontWeight="600"
                    className="select-none pointer-events-none drop-shadow"
                  >
                    {mk.name.split(' ')[0]}
                  </text>
                </g>
              );
            })}
          </svg>

          {/* Quick Legend overlay */}
          <div className="absolute bottom-3 left-3 bg-slate-900/90 border border-slate-800 rounded-lg p-2 text-[10px] text-slate-300 space-y-1">
            <div className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
              <span>Operational DC Hub</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-2 h-2 rounded-full bg-red-500 animate-pulse"></span>
              <span>Active Incident / Cold-Chain Breach</span>
            </div>
            <div className="flex items-center gap-1.5">
              <span className="w-4 h-0.5 bg-red-500 border-dashed"></span>
              <span>Disrupted / High-Cost Route</span>
            </div>
          </div>
        </div>

        {/* Selected Route / Marker Detail Card */}
        <div className="bg-slate-950/70 rounded-xl border border-slate-800 p-4 space-y-3">
          <h4 className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Corridor Intelligence
          </h4>

          {selectedMarker ? (
            <div className="space-y-2 text-xs">
              <div className="flex items-center justify-between pb-1 border-b border-slate-800">
                <span className="font-bold text-slate-100">{selectedMarker.name}</span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-medium ${
                  selectedMarker.marker_type === 'incident' ? 'bg-red-500/20 text-red-400 border border-red-500/30' : 'bg-emerald-500/20 text-emerald-400'
                }`}>
                  {selectedMarker.marker_type.toUpperCase()}
                </span>
              </div>
              <p className="text-slate-300 leading-relaxed">{selectedMarker.description}</p>
              <div className="text-[11px] text-slate-500">
                Lat: {selectedMarker.latitude}°N, Lng: {selectedMarker.longitude}°E
              </div>
            </div>
          ) : (
            <div className="space-y-2">
              <p className="text-xs text-slate-400">Click any corridor or depot node on the map to inspect operational telematics.</p>
              <div className="space-y-1.5 max-h-56 overflow-y-auto pr-1">
                {routeMap.routes.map((rt) => (
                  <div
                    key={rt.code}
                    onClick={() => setSelectedRoute(rt.code)}
                    className={`p-2 rounded-lg text-xs border transition cursor-pointer ${
                      selectedRoute === rt.code
                        ? 'bg-blue-600/20 border-blue-500/50 text-blue-200'
                        : 'bg-slate-900 border-slate-800 text-slate-300 hover:bg-slate-800'
                    }`}
                  >
                    <div className="flex items-center justify-between font-medium">
                      <span>{rt.origin} → {rt.dest}</span>
                      <strong className={rt.avg_cost_km > 50 ? 'text-rose-400' : 'text-slate-200'}>
                        ₹{rt.avg_cost_km}/km
                      </strong>
                    </div>
                    <div className="flex items-center justify-between text-[11px] text-slate-400 mt-0.5">
                      <span>{rt.distance_km} km</span>
                      <span className={rt.status.includes('Optimal') ? 'text-emerald-400' : 'text-amber-400'}>
                        {rt.status}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
