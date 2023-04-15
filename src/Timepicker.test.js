import { JSDOM } from 'jsdom';
import { Timepicker } from './timepicker';

// ...other imports if needed


describe('Timepicker', () => {
  let timepicker;
  let dom;
  let container;

  beforeEach(() => {
    dom = new JSDOM('<!DOCTYPE html><html><head></head><body></body></html>');
    global.document = dom.window.document;
    global.window = dom.window;

    container = document.createElement('div');
    timepicker = new Timepicker(/* your parameters here */);
    container.appendChild(timepicker.timepickerElement); // Append the Timepicker instance to the container div
  });

  afterEach(() => {
    // Clean up after each test
    timepicker = null;
    container = null;
    global.document = undefined;
    global.window = undefined;
  });

  // Your tests go here
  test('should rotate hour hand based on selectedHours', () => {
    const selectedHours = 6;
    const expectedHourRotation = (selectedHours % 12) * 30;
    timepicker = new Timepicker(false, true, selectedHours, 0, 0);
    container.appendChild(timepicker.timepicker);
    
    const hourHand = container.querySelector('.hour-hand');
    const transformStyle = hourHand.style.transform || hourHand.style[Timepicker.getSupportedTransformProp()];
    
    // Extract the rotation angle from the transform style string
    const rotationAngle = parseFloat(transformStyle.match(/rotate\((-?\d+(?:\.\d+)?)deg\)/)[1]);
    
    expect(rotationAngle).toBe(expectedHourRotation);
  });
  

  // ...more tests
});
