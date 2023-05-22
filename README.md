# Load Balancer Simulator

This project contains a load balancer simulator implemented in Python. It includes three types of load balancers: Part1LoadBalancer, Part2LoadBalancer, and PDLoadBalancer. You can find the implementations of these load balancers in the src/load_balancers directory.

## Requirements 

The only external requirement for this project is matplotlib. You can install it by running:

`pip install -r requirements.txt`

## Running the Code

To execute the code, use the following command:

`python main.py <loadbalancer_class_name> [<input_traffic_json_path>]`

If `<input_traffic_json_path>` is not provided, the simulator will run with 'ExampleTraffic.json' as default input.

Here `<loadbalancer_class_name>` can be any one of the three available load balancer implementations:

<dl>
    <dt>Part1LoadBalancer</dt>
    <dt>Part2LoadBalancer</dt>
    <dt>PDLoadBalancer</dt>
</dl>

For example, to run the simulator with the `'Part1LoadBalancer'` and custom input traffic, use:

`python main.py Part1LoadBalancer custom_input.json`

## Running Tests

This project includes integration tests for Simulation with dummy load balancer. To run them, use:

`python -m unittest test/integration_tests/test_simulation.py`

Please ensure you run the tests from the project's root directory.