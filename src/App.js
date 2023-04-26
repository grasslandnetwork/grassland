/* eslint-disable */
import React, {useState, useEffect, useRef} from 'react';
import {Map} from 'react-map-gl';
import maplibregl from 'maplibre-gl';
import {AmbientLight, PointLight, LightingEffect} from '@deck.gl/core';
import DeckGL from '@deck.gl/react';
import {PolygonLayer} from '@deck.gl/layers';
import {TripsLayer} from '@deck.gl/geo-layers';
import {COORDINATE_SYSTEM} from '@deck.gl/core';
import {LineLayer} from '@deck.gl/layers';
import {Matrix4} from 'math.gl';
import { invoke } from '@tauri-apps/api';
const timer = require('./timepicker.js');
let timepicker;
let startTime = Date.now();
let lastRAFTimestamp = 0;
let intervalId;
// Source data CSV
const DATA_URL = {
  BUILDINGS:
    '/buildings.json', // eslint-disable-line
  TRIPS: '/trips-real-timestamps.json' // eslint-disable-line
};

const ambientLight = new AmbientLight({
  color: [255, 255, 255],
  intensity: 1.0
});

const pointLight = new PointLight({
  color: [255, 255, 255],
  intensity: 2.0,
  position: [-74.05, 40.7, 8000]
});

const lightingEffect = new LightingEffect({ambientLight, pointLight});

const material = {
  ambient: 0.1,
  diffuse: 0.6,
  shininess: 32,
  specularColor: [60, 64, 70]
};

const DEFAULT_THEME = {
  buildingColor: [74, 80, 87],
  trailColor0: [253, 128, 93],
  trailColor1: [23, 184, 190],
  material,
  effects: [lightingEffect]
};

const INITIAL_VIEW_STATE = {
  longitude: -73.97465012857278,
  latitude: 40.69877933033733,
    zoom: 19,
    maxZoom: 25,
  pitch: 45,
  bearing: 0
};

const MAP_STYLE = 'https://basemaps.cartocdn.com/gl/dark-matter-nolabels-gl-style/style.json';

const landCover = [
  [
    [-74.0, 40.7],
    [-74.02, 40.7],
    [-74.02, 40.72],
    [-74.0, 40.72]
  ]
];


// Pose Keypoints and Connections
// Define connections between keypoints
const connections = [
    [15, 21], [16, 20], [18, 20], [3, 7], [14, 16], [23, 25], [28, 30], [11, 23], [27, 31], [6, 8], [15, 17], [24, 26], [16, 22], [4, 5], [5, 6], [29, 31], [12, 24], [23, 24], [0, 1], [9, 10], [1, 2], [0, 4], [11, 13], [30, 32], [28, 32], [15, 19], [16, 18], [25, 27], [26, 28], [12, 14], [17, 19], [2, 3], [11, 12], [27, 29], [13, 15]
];


// Create a transformation matrix that rotates the poses 90 degrees around the X-axis and 180 degrees around the Z-axis
// By applying this transformation, the poses' X, Y, and Z coordinates will be correctly oriented according to Deck.gl's coordinate system
const transformationMatrix = new Matrix4().rotateX(Math.PI / 2).rotateZ(Math.PI);

const thisLineLayer = new LineLayer({
    id: 'pose-connections',
    coordinateSystem: COORDINATE_SYSTEM.METER_OFFSETS,
    coordinateOrigin: [-73.97466922549505, 40.698810743664666, 2],
    modelMatrix: transformationMatrix,
    data: "poses.json",    
    getSourcePosition: d => [d.start.x, d.start.y, d.start.z],
    getTargetPosition: (d, info) => {
        return [d.end.x, d.end.y, d.end.z];
    },
    getColor: [0, 255, 0, 255],
    getWidth: 0.4
});

// this assume that poses.json is in the following format. With 'start' and 'end' representing two connected keypoints
// [
//     {
//         "start": {"x": 0.058136872947216034, "y": 0.0024060863070189953, "z": 1.3565037250518799},
//         "end": {"x": 0.03100830502808094, "y": -0.026282524690032005, "z": 1.3559198379516602}
//     },
//     {
//         "start": {"x": -0.09797123074531555, "y": -0.0001541937090223655, "z": 1.47249436378479},
//         "end": {"x": -0.07531852275133133, "y": -0.03375338762998581, "z": 1.441045880317688}
//     }
//     ...
// ]
 
export default function App({
  buildings = DATA_URL.BUILDINGS,
  trips = DATA_URL.TRIPS,
  trailLength = 180,
  initialViewState = INITIAL_VIEW_STATE,
  mapStyle = MAP_STYLE,
  theme = DEFAULT_THEME,
  loopLength = 251510, // unit corresponds to the timestamp in source data
  animationSpeed = 1
}) {

  const domElementRef = useRef(null);
  // now we can call our Command!
  // Right-click the application background and open the developer tools.
  // You will see "Hello, World!" printed in the console!
  // invoke('greet', { name: 'World' })
  // // `invoke` returns a Promise
  // .then((response) => console.log(response))


  const [time, setTime] = useState(0);
  const [animation] = useState({});
  const lastRAFTimestamp = useRef(0);

  // console.log("time", time);
    
  useEffect(() => {

    if (domElementRef.current) {
      // Your code to execute when the DOM element is available
      if(!timepicker) {
        timepicker = timer.Timepicker();
        document.getElementById('timepicker').appendChild(timepicker.getElement());
        timepicker.show();
      }

    }

    const animate = (rAFTimestamp=0) => {
      setTime(t => (t + animationSpeed) % loopLength);
        if (timepicker) {
            var elapsedMilliseconds = rAFTimestamp - lastRAFTimestamp.current;
            timepicker.moveClockDateForward(elapsedMilliseconds);
        }
        lastRAFTimestamp.current = rAFTimestamp;
        animation.id = window.requestAnimationFrame(animate);
    };

    animation.id = window.requestAnimationFrame(animate);
    return () => {
      window.cancelAnimationFrame(animation.id);
      clearInterval(intervalId);
    };
  }, [animation, animationSpeed, loopLength, domElementRef.current]);

    const world_time_starting_point = 1668521196000;

   

     
  const layers = [
    // This is only needed when using shadow effects
    new PolygonLayer({
      id: 'ground',
      data: landCover,
      getPolygon: f => f,
      stroked: false,
      getFillColor: [0, 0, 0, 0]
    }),
    thisLineLayer
      
    // new TripsLayer({
    //   id: 'trips',
    //   data: trips,
    //   getPath: d => d.path,
    //     getTimestamps: d => d.timestamps.map(p => {
    //         return p - world_time_starting_point;}),
    //   getColor: d => (d.vendor === 0 ? theme.trailColor0 : theme.trailColor1),
    //   opacity: 0.3,
    //   widthMinPixels: 2,
    //   rounded: true,
    //   trailLength,
    //   currentTime: time,

    //   shadowEnabled: false
    // }),
      
      // Create a custom mesh for rendering cylinders

  ];

  return (
    <DeckGL
      layers={layers}
      effects={theme.effects}
      initialViewState={initialViewState}
      controller={true}
    >
      <Map reuseMaps mapLib={maplibregl} mapStyle={mapStyle} preventStyleDiffing={true} />
      <div ref={domElementRef} id="timepicker"></div>
    </DeckGL>
    
  );
}
