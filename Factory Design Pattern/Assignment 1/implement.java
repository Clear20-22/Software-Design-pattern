import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

/*
 * =========================================================
 * SMART TRANSPORTATION MANAGEMENT SYSTEM
 * =========================================================
 */

/* =========================================================
 * PRODUCT INTERFACE
 * =========================================================
 */
interface Vehicle {
    void startTrip();

    double calculateFare(double distance);

    void assignRoute(String route);

    void getVehicleInfo();

    String getVehicleType();
}

class Bus implements Vehicle {

    private final int capacity = 40;
    private final double farePerKm = 15;
    private String route;

    @Override
    public void startTrip() {
        System.out.println("Bus trip started.");
    }

    @Override
    public double calculateFare(double distance) {
        return distance * farePerKm;
    }

    @Override
    public void assignRoute(String route) {
        this.route = route;
        System.out.println("Bus assigned to route: " + route);
    }

    @Override
    public void getVehicleInfo() {
        System.out.println("Vehicle: Bus");
        System.out.println("Capacity: " + capacity);
        System.out.println("Fare per KM: " + farePerKm);
    }

    @Override
    public String getVehicleType() {
        return "Bus";
    }
}

class Taxi implements Vehicle {

    private final int capacity = 4;
    private final double farePerKm = 30;
    private String route;

    @Override
    public void startTrip() {
        System.out.println("Taxi trip started.");
    }

    @Override
    public double calculateFare(double distance) {
        return distance * farePerKm;
    }

    @Override
    public void assignRoute(String route) {
        this.route = route;
        System.out.println("Taxi assigned to route: " + route);
    }

    @Override
    public void getVehicleInfo() {
        System.out.println("Vehicle: Taxi");
        System.out.println("Capacity: " + capacity);
        System.out.println("Fare per KM: " + farePerKm);
    }

    @Override
    public String getVehicleType() {
        return "Taxi";
    }
}

class MotorcycleDelivery implements Vehicle {

    private final int capacity = 1;
    private final double farePerKm = 10;
    private String route;

    @Override
    public void startTrip() {
        System.out.println("Motorcycle delivery started.");
    }

    @Override
    public double calculateFare(double distance) {
        return distance * farePerKm;
    }

    @Override
    public void assignRoute(String route) {
        this.route = route;
        System.out.println("Motorcycle assigned to route: " + route);
    }

    @Override
    public void getVehicleInfo() {
        System.out.println("Vehicle: Motorcycle Delivery");
        System.out.println("Capacity: " + capacity);
        System.out.println("Fare per KM: " + farePerKm);
    }

    @Override
    public String getVehicleType() {
        return "Motorcycle Delivery";
    }
}

class ElectricScooter implements Vehicle {

    private final int capacity = 1;
    private final double farePerKm = 8;
    private String route;

    @Override
    public void startTrip() {
        System.out.println("Electric scooter trip started.");
    }

    @Override
    public double calculateFare(double distance) {
        return distance * farePerKm;
    }

    @Override
    public void assignRoute(String route) {
        this.route = route;
        System.out.println("Scooter assigned to route: " + route);
    }

    @Override
    public void getVehicleInfo() {
        System.out.println("Vehicle: Electric Scooter");
        System.out.println("Capacity: " + capacity);
        System.out.println("Fare per KM: " + farePerKm);
    }

    @Override
    public String getVehicleType() {
        return "Electric Scooter";
    }
}

abstract class VehicleCreator {
    public abstract Vehicle createVehicle();

    public Vehicle createAndAssign(String route) {
        Vehicle vehicle = createVehicle();
        vehicle.assignRoute(route);
        return vehicle;
    }
}

class BusCreator extends VehicleCreator {
    @Override
    public Vehicle createVehicle() {
        return new Bus();
    }
}

class TaxiCreator extends VehicleCreator {
    @Override
    public Vehicle createVehicle() {
        return new Taxi();
    }
}

class MotorcycleDeliveryCreator extends VehicleCreator {
    @Override
    public Vehicle createVehicle() {
        return new MotorcycleDelivery();
    }
}

class ElectricScooterCreator extends VehicleCreator {
    @Override
    public Vehicle createVehicle() {
        return new ElectricScooter();
    }
}

class CreatorRegistry {
    public static VehicleCreator getCreator(String type) {
        switch (type.toLowerCase()) {
            case "bus":
                return new BusCreator();
            case "taxi":
                return new TaxiCreator();
            case "motorcycle":
                return new MotorcycleDeliveryCreator();
            case "scooter":
                return new ElectricScooterCreator();
            default:
                throw new IllegalArgumentException("Unknown vehicle type: " + type);
        }
    }
}

public class implement {
    public static void main(String[] args) {
        List<Vehicle> vehicles = new ArrayList<>();
        Scanner scanner = new Scanner(System.in);

        System.out.println("Welcome to the Smart Transportation Management System!");
        System.out.println("Available vehicle types: Bus, Taxi, Motorcycle, Scooter");
        System.out.println("Enter 'exit' to stop adding vehicles.");

        while (true) {
            System.out.println("Available vehicle types: Bus, Taxi, Motorcycle, Scooter");
            System.out.print("Enter vehicle type to add: ");
            
            String input = scanner.nextLine();
            if (input.equalsIgnoreCase("exit")) {
                break;
            }
            try {
                VehicleCreator creator = CreatorRegistry.getCreator(input);
                Vehicle vehicle = creator.createAndAssign("Default Route");
                vehicles.add(vehicle);

                vehicle.startTrip();
                double fare = vehicle.calculateFare(5);
                System.out.println(input + " added to the system. Fare for 5 KM: " + fare);
            } catch (IllegalArgumentException e) {
                System.out.println(e.getMessage());
            }
        }

        System.out.println("\nVehicles in the system:");
        for (Vehicle vehicle : vehicles) {
            vehicle.getVehicleInfo();
            System.out.println();
        }

        scanner.close();
    }
}