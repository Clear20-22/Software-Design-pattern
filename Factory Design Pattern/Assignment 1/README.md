# Smart Transportation Management System (Factory Method)

## Problem in the prototype

The original prototype mixed object creation logic with client code. When new vehicle types are added, client code must be edited repeatedly.

## Why Factory Method here

Factory Method moves creation responsibility into creator classes.

Instead of client code doing:

- new Bus()
- new Taxi()
- new MotorcycleDelivery()
- new ElectricScooter()

Client code now asks a creator to build a vehicle.

## Pattern roles in this assignment

### Product

- `Vehicle` interface

### Concrete Products

- `Bus`
- `Taxi`
- `MotorcycleDelivery`
- `ElectricScooter`

### Creator (Factory Method owner)

- `VehicleCreator`
- Factory Method: `createVehicle()`

### Concrete Creators

- `BusCreator`
- `TaxiCreator`
- `MotorcycleDeliveryCreator`
- `ElectricScooterCreator`

### Helper for runtime selection

- `CreatorRegistry`

## Flow of control

1. User enters a vehicle type.
2. Client asks `CreatorRegistry` for the correct `VehicleCreator`.
3. Client calls creator method (`createAndAssign` / `createVehicle`).
4. Creator returns a `Vehicle` object.
5. Client uses only `Vehicle` abstraction for trip, fare, info.

## Benefits achieved

- Better maintainability: creation code is centralized and separated.
- Better scalability: new vehicle type usually needs only new Product + new Creator + one registry entry.
- Better readability: client logic focuses on business flow, not construction details.
- Better testability: creators can be tested independently.

## How to run

From this folder:

```bash
javac implement.java
java implement
```

Then provide input like:

- `bus`
- `taxi`
- `motorcycle`
- `scooter`
- `exit`

## Viva-ready tricky questions and answers

1. What is the key difference between Simple Factory and Factory Method?

- Simple Factory usually uses one class with conditional creation logic.
- Factory Method defines a creation method in a creator hierarchy and delegates actual creation to subclasses.

2. Is `CreatorRegistry` itself Factory Method?

- No. The Factory Method part is in `VehicleCreator.createVehicle()` and concrete creator subclasses.
- `CreatorRegistry` is only a runtime selector helper.

3. Why not instantiate vehicles directly in `main`?

- That couples the client with concrete classes and violates Open/Closed thinking.

4. Does this implementation fully satisfy OCP?

- Partially. Adding a new type still requires one entry in `CreatorRegistry`.
- For stronger OCP, registration can be dynamic (map-based registration).

5. Where is polymorphism used?

- Client handles all objects as `Vehicle` and all creators as `VehicleCreator`.

6. Can `VehicleCreator` contain business logic?

- Yes, shared creation workflow can live there (here: `createAndAssign`).

7. Why keep `createVehicle()` abstract?

- To force each concrete creator to define exact product construction.

8. If all creators are one-line return statements, is Factory Method still useful?

- Yes. It preserves extensibility boundaries and decouples client from concrete product classes.

9. Could Abstract Factory be better?

- If you need families of related objects (e.g., vehicle + ticket + route strategy), Abstract Factory may fit better.

10. What if fare logic becomes dynamic by traffic/time?

- Keep creation in Factory Method and move fare policy to Strategy pattern.

11. Is switch-case in `CreatorRegistry` a design smell?

- It is acceptable for small systems.
- For larger systems, replace with configuration or dependency injection registration.

12. What is the main test you should write for Factory Method?

- Verify each creator returns correct concrete product implementing `Vehicle`.

13. Can creators cache and reuse vehicles?

- They can, but then behavior shifts toward object pooling or singleton-like reuse and must match domain rules.

14. How does this reduce ripple effect?

- Client code remains stable when creation details change inside creator classes.

15. One-liner viva answer: Why Factory Method in this project?

- Because vehicle types will grow, and this pattern isolates object creation from operational client code for safer extension.
