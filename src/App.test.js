import { render, queryByAttribute} from '@testing-library/react';
import React from 'react';
import App from './App';
const getById = queryByAttribute.bind(null, 'id');


/*
In this example, we're mocking out maplibre-gl by returning a new object that contains mock 
implementations of the Map and Marker classes. We're using jest.fn() to create mock functions 
for the on, remove, and setLngLat methods, which allows us to assert that these methods were 
called with the correct arguments.
*/

jest.mock('maplibre-gl', () => {
  // Create a mock object for maplibre-gl
  return {
    // Mock any properties or methods you're using in your tests
    Map: jest.fn(() => ({
      on: jest.fn(),
      remove: jest.fn(),
    })),
    Marker: jest.fn(() => ({
      setLngLat: jest.fn(),
    })),
  };
});

test('renders learn react link', () => {
  const dom = render(<App />);
  const linkElement = getById(dom.container, 'deckgl-wrapper');
  expect(linkElement).toBeInTheDocument();
});

test('renders clock with a button that has a Pause text', () => {
  const { container } = render(<App />);
  const myElement = getById(container, 'timepicker');
  expect(myElement).toBeInTheDocument();
});
