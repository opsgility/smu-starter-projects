module.exports.computePosition = ({ lat, lng, alt }) => ({
  lat: lat + (Math.random() - 0.5) * 0.0001,
  lng: lng + (Math.random() - 0.5) * 0.0001,
  alt: Math.max(0, alt - 1),
});

module.exports.computeBattery = (current) => Math.max(0, current - 0.5);
