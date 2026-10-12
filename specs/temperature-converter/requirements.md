# Requirements: Temperature Converter

Status: Approved. US-1 to US-4 are implemented; US-5 is not yet implemented.

## Goal

Let a user convert a temperature between Celsius, Fahrenheit and Kelvin, from the command line
or from a simple graphical interface.

## User stories

Each story is tracked as a GitHub issue with the `user-story` label.

- **US-1** ([#1](https://github.com/ItsAlwaysRaining/Spec-Driven-Design-Experiment/issues/1)): As a user, I want to convert Celsius to Fahrenheit so I can read US weather reports.
- **US-2** ([#2](https://github.com/ItsAlwaysRaining/Spec-Driven-Design-Experiment/issues/2)): As a user, I want to convert Fahrenheit to Celsius so I can follow US recipes.
- **US-3** ([#3](https://github.com/ItsAlwaysRaining/Spec-Driven-Design-Experiment/issues/3)): As a user, I want a clear error when I enter something invalid, so I know what to fix.
- **US-4** ([#5](https://github.com/ItsAlwaysRaining/Spec-Driven-Design-Experiment/issues/5)): As a user, I want to convert between Kelvin and Celsius or Fahrenheit, so I can work with scientific temperatures.
- **US-5** ([#6](https://github.com/ItsAlwaysRaining/Spec-Driven-Design-Experiment/issues/6)): As a user, I want a simple window where I enter one temperature and see it in every other unit, so I don't need the command line.

## Acceptance criteria

| ID    | Story | Given / When / Then |
|-------|-------|---------------------|
| AC-1  | US-1  | Given `100` Celsius, when converted, then the result is `212` Fahrenheit. |
| AC-2  | US-1  | Given `0` Celsius, when converted, then the result is `32` Fahrenheit. |
| AC-3  | US-2  | Given `32` Fahrenheit, when converted, then the result is `0` Celsius. |
| AC-4  | US-2  | Given `-40` Fahrenheit, when converted, then the result is `-40` Celsius. |
| AC-5  | US-3  | Given a temperature below absolute zero (-273.15 °C / -459.67 °F / 0 K), then an error is raised. |
| AC-6  | US-3  | Given a unit other than `C`, `F` or `K`, then an error is raised. *(Changed for US-4: previously only `C` or `F` were valid.)* |
| AC-7  | US-1, US-2, US-4 | The command-line output is rounded to 2 decimal places and shows the target unit, e.g. `212.00 F`. |
| AC-8  | US-4  | Given `0` Celsius, when converted to Kelvin, then the result is `273.15` Kelvin. |
| AC-9  | US-4  | Given `32` Fahrenheit, when converted to Kelvin, then the result is `273.15` Kelvin. |
| AC-10 | US-4  | Given `0` Kelvin, when converted to Celsius, then the result is `-273.15` Celsius. |
| AC-11 | US-4  | Given `0` Kelvin, when converted to Fahrenheit, then the result is `-459.67` Fahrenheit. |
| AC-12 | US-4  | The user chooses both the source and the target unit. With three units, "the other unit" is no longer enough. |
| AC-13 | US-5  | The window has one field to enter a value and a way to choose its unit from all available units (currently `C`, `F`, `K`). |
| AC-14 | US-5  | Given `100` and unit `C`, when converted, then the window shows the result in every other unit at once: `212.00 F` and `373.15 K`. The source unit itself is not repeated. |
| AC-15 | US-5  | Results use the same format as the command line: 2 decimal places, the unit after the number, never `-0.00` (as AC-7). |
| AC-16 | US-5  | Given invalid input (empty, not a number, or below absolute zero), then the window shows an error message instead of results, and stays open. |
| AC-17 | US-5  | When a unit is added to the converter, it appears in the window automatically, as both a source unit and a result, with no changes to the window's code. |
| AC-18 | US-5  | The window opens with one command and needs nothing installed beyond Python. |

### Constraints for US-5

- Minimal formatting, as asked in #6: the system's default look, with no custom colours, fonts, images or themes.
- As simple as possible: one window, no menus, no settings.

## Out of scope

- Units other than Celsius, Fahrenheit and Kelvin (e.g. Rankine). Issue #5 asks that more units be easy to add later; that is a design concern, not a requirement of US-4.
- A web or mobile interface. US-5 is a desktop window only.
- Remembering previous conversions (history).
