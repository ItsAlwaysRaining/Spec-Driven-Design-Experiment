# Requirements: Temperature Converter

Status: Approved

## Goal

Let a user convert a temperature between Celsius and Fahrenheit from the command line.

## User stories

- **US-1:** As a user, I want to convert Celsius to Fahrenheit so I can read US weather reports.
- **US-2:** As a user, I want to convert Fahrenheit to Celsius so I can follow US recipes.
- **US-3:** As a user, I want a clear error when I enter something invalid, so I know what to fix.

## Acceptance criteria

| ID   | Story | Given / When / Then |
|------|-------|---------------------|
| AC-1 | US-1  | Given `100` Celsius, when converted, then the result is `212` Fahrenheit. |
| AC-2 | US-1  | Given `0` Celsius, when converted, then the result is `32` Fahrenheit. |
| AC-3 | US-2  | Given `32` Fahrenheit, when converted, then the result is `0` Celsius. |
| AC-4 | US-2  | Given `-40` Fahrenheit, when converted, then the result is `-40` Celsius. |
| AC-5 | US-3  | Given a temperature below absolute zero (-273.15 °C / -459.67 °F), then an error is raised. |
| AC-6 | US-3  | Given a unit other than `C` or `F`, then an error is raised. |
| AC-7 | US-1, US-2 | The command-line output is rounded to 2 decimal places and shows the target unit, e.g. `212.00 F`. |

## Out of scope

- Kelvin and other units
- A graphical interface
