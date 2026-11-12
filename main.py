from drafter import *
from dataclasses import dataclass
import math


GRAVITY = 9.81


@dataclass
class Rocket:
    name: str
    mass: float
    thrust: float
    burn_time: float


@dataclass
class State:
    rockets: list[Rocket]
    selected_rocket: int
    sim_results: list[list[float]]
    message: str
    draft: Rocket


def initial_state() -> State:
    """Create the starting state."""
    return State([], -1, [], "", Rocket("", 0, 0, 0))


@route
def index(state: State) -> Page:
    """Display the home page."""
    return Page(state, [
        Header("Rocket Launch Simulator"),

        "Design, test, and compare your own rockets.",
        "Explore how mass, thrust, and burn time affect flight.",

        Button("Design Rocket", "design_rocket"),
        Button("View Saved Rockets", "view_rockets"),
        Button("Compare Rockets", "compare_rockets")
    ])


@route
def design_rocket(state: State) -> Page:
    """Display the rocket design input page."""
    return Page(state, [
        Header("Design a Rocket"),

        state.message,

        "Rocket Name:",
        TextBox("name", ""),

        "Mass (kg):",
        TextBox("mass", "10"),

        "Thrust (N):",
        TextBox("thrust", "200"),

        "Burn Time (s):",
        TextBox("burn_time", "5"),

        Button("Calculate Results", "calculate_results"),
        Link("Back to Home", "index")
    ])


@route
def calculate_results(state: State, name: str,
                      mass: str, thrust: str,
                      burn_time: str) -> Page:
    """Calculate and display the rocket's performance."""

    if name.strip() == "":
        state.message = "Please enter a rocket name."
        return design_rocket(state)

    try:
        rocket_mass = float(mass)
        rocket_thrust = float(thrust)
        rocket_burn_time = float(burn_time)

    except ValueError:
        state.message = "Please enter valid numbers."
        return design_rocket(state)

    if not math.isfinite(rocket_mass):
        state.message = "Please enter a finite mass."
        return design_rocket(state)

    if not math.isfinite(rocket_thrust):
        state.message = "Please enter a finite thrust."
        return design_rocket(state)

    if not math.isfinite(rocket_burn_time):
        state.message = "Please enter a finite burn time."
        return design_rocket(state)

    if rocket_mass <= 0:
        state.message = "Mass must be greater than zero."
        return design_rocket(state)

    if rocket_thrust <= 0:
        state.message = "Thrust must be greater than zero."
        return design_rocket(state)

    if rocket_burn_time <= 0:
        state.message = "Burn time must be greater than zero."
        return design_rocket(state)

    state.draft = Rocket(
        name,
        rocket_mass,
        rocket_thrust,
        rocket_burn_time
    )

    state.message = ""

    # Calculate net acceleration using Newton's second law.
    acceleration = rocket_thrust / rocket_mass - GRAVITY

    if acceleration <= 0:

        velocity = 0
        max_altitude = 0
        flight_time = 0

        status = "Insufficient thrust for liftoff."

    else:

        velocity = acceleration * rocket_burn_time

        burn_altitude = (
            0.5 * acceleration * rocket_burn_time ** 2
        )

        max_altitude = (
            burn_altitude + velocity ** 2 / (2 * GRAVITY)
        )

        flight_time = rocket_burn_time + (
            velocity + math.sqrt(
                velocity ** 2 + 2 * GRAVITY * burn_altitude
            )
        ) / GRAVITY

        status = "Successful liftoff!"

    return Page(state, [
        Header("Rocket Flight Results"),

        "Rocket: " + name,

        status,

        Header("Rocket Specifications", 2),

        "Mass: " + str(rocket_mass) + " kg",
        "Thrust: " + str(rocket_thrust) + " N",
        "Burn Time: " + str(rocket_burn_time) + " s",

        Header("Flight Performance", 2),

        "Net Acceleration: "
        + str(round(acceleration, 2)) + " m/s²",

        "Maximum Upward Velocity: "
        + str(round(velocity, 2)) + " m/s",

        "Maximum Altitude: "
        + str(round(max_altitude, 2)) + " m",

        "Total Flight Time: "
        + str(round(flight_time, 2)) + " s",

        Button("Save Rocket", "save_rocket"),
        Button("Design Another Rocket", "design_rocket"),
        Button("Back to Home", "index")
    ])


@route
def save_rocket(state: State) -> Page:
    """Save the current rocket design."""

    if state.draft.name == "":
        state.message = "Please design a rocket first."
        return design_rocket(state)

    state.rockets.append(state.draft)

    state.selected_rocket = len(state.rockets) - 1

    state.message = state.draft.name + " successfully saved!"

    return view_rockets(state)


@route
def view_rockets(state: State) -> Page:
    """Display all saved rocket designs."""

    content = [
        Header("Saved Rockets"),
        state.message
    ]

    if len(state.rockets) == 0:
        content.append("No rockets have been saved yet.")

    for rocket in state.rockets:

        content.append(Header(rocket.name, 2))

        content.append(
            "Mass: " + str(rocket.mass) + " kg"
        )

        content.append(
            "Thrust: " + str(rocket.thrust) + " N"
        )

        content.append(
            "Burn Time: " + str(rocket.burn_time) + " s"
        )

        content.append("------------------------------")

    # Only display the clear button if rockets exist.
    if len(state.rockets) > 0:
        content.append(
            Button("Clear All Saved Rockets", "clear_rockets")
        )

    content.append(Button("Design Rocket", "design_rocket"))
    content.append(Button("Back to Home", "index"))

    return Page(state, content)


@route
def compare_rockets(state: State) -> Page:
    """Display a basic comparison of saved rocket designs."""

    content = [Header("Compare Rockets")]

    if len(state.rockets) < 2:

        content.append(
            "Save at least two rockets to compare them."
        )

    else:

        for rocket in state.rockets:

            content.append(Header(rocket.name, 2))

            content.append(
                "Mass: " + str(rocket.mass) + " kg"
            )

            content.append(
                "Thrust: " + str(rocket.thrust) + " N"
            )

            content.append(
                "Burn Time: " + str(rocket.burn_time) + " s"
            )

            acceleration = rocket.thrust / rocket.mass - GRAVITY

            content.append(
                "Net Acceleration: "
                + str(round(acceleration, 2)) + " m/s²"
            )

            content.append("------------------------------")

    content.append(
        "More detailed comparison features are coming soon."
    )

    content.append(Button("View Saved Rockets", "view_rockets"))
    content.append(Button("Back to Home", "index"))

    return Page(state, content)


@route
def clear_rockets(state: State) -> Page:
    """Remove all saved rocket designs."""

    state.rockets = []

    state.selected_rocket = -1

    state.message = "All saved rockets have been cleared."

    return view_rockets(state)


# --------------------------------
# Unit Tests
# --------------------------------


def run_tests() -> None:
    """Test all seven routes."""

    # Test 1: Home page
    assert_has(
        index(initial_state()),
        Header("Rocket Launch Simulator")
    )

    # Test 2: Design page
    assert_has(
        design_rocket(initial_state()),
        TextBox("mass", "10")
    )

    # Test 3: Calculate results
    state = initial_state()

    page = calculate_results(
        state, "Test Rocket", "10", "200", "5"
    )

    assert_equal(
        state.draft,
        Rocket("Test Rocket", 10, 200, 5)
    )

    assert_has(
        page,
        "Successful liftoff!"
    )

    # Test 4: Save rocket
    save_rocket(state)

    assert_equal(
        state.rockets,
        [Rocket("Test Rocket", 10, 200, 5)]
    )

    # Test 5: View saved rockets
    assert_has(
        view_rockets(state),
        Header("Test Rocket", 2)
    )

    # Test 6: Compare rockets
    assert_has(
        compare_rockets(initial_state()),
        "Save at least two rockets to compare them."
    )

    # Test 7: Clear rockets
    clear_rockets(state)

    assert_equal(state.rockets, [])


run_tests()


set_website_title("Rocket Launch Simulator")


set_site_information(
    author="Joseph Britz",
    description="Design and test rocket performance.",
    sources="Drafter documentation and ChatGPT.",
    planning=["brainstorm.pdf", "design.pdf"],
    links=[]
)


start_server(initial_state())
