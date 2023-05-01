import { render, queryByAttribute} from '@testing-library/react';
import React from 'react';
import App from './App';
const getById = queryByAttribute.bind(null, 'id');

test('renders learn react link', () => {
  const dom = render(<App />);
  const linkElement = getById(dom.container, 'deckgl-wrapper');
  expect(linkElement).toBeInTheDocument();
});
