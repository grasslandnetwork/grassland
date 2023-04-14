import { Timepicker } from './timepicker';

describe('Timepicker', () => {
  let timepicker;
  let container;

  beforeEach(() => {
    container = document.createElement('div');
    document.body.appendChild(container);
    timepicker = new Timepicker(false, true, 10, 30, 45);
    container.appendChild(timepicker.timepicker);
  });

  afterEach(() => {
    document.body.removeChild(container);
  });

  test('should create a timepicker', () => {
    expect(timepicker).toBeDefined();
    expect(timepicker.timepicker).toBeDefined();
    expect(timepicker.clockFace).toBeDefined();
    expect(timepicker.hourHand).toBeDefined();
    expect(timepicker.minuteHand).toBeDefined();
    expect(timepicker.secondHand).toBeDefined();
  });

  test('should display the correct initial time', () => {
    expect(timepicker.selectedHours).toBe(10);
    expect(timepicker.selectedMinutes).toBe(30);
    expect(timepicker.selectedSeconds).toBe(45);
  });

  test('should update timepicker display when updating time', () => {
    // You can create a function to update the time in Timepicker.js, e.g. timepicker.updateTime(12, 34, 56);
    // Then, call the function here and check if the updated time is correctly displayed.
  });

  // Add more tests for various functionalities, like changing the hour system, updating the clock pointers, etc.
});
